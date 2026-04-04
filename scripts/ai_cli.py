#!/usr/bin/env python3

import sys
import socket
import json

SOCKET_PATH = "/tmp/neurocore.sock"
BUFFER_SIZE = 4096
TIMEOUT = 60


def read_stdin():
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return data
    return None


def classify_input(data):
    lower = data.lower()

    if any(word in lower for word in ["error", "failed", "exception", "traceback"]):
        return "logs"

    if "filesystem" in lower or "mounted on" in lower:
        return "system_output"

    if any(sym in data for sym in ["{", "}", "=", ":"]):
        return "config"

    if len(data.split()) < 10:
        return "query"

    return "generic"


def build_contextual_prompt(data, input_type):
    """
    Strong, directive prompt framing with structured reasoning.
    """

    if input_type == "logs":
        return f"""You are a systems diagnostic assistant.

You are analyzing raw system logs.

Rules:
- Do NOT assume this is about Linux permissions
- Do NOT rely on prior context
- Focus ONLY on the provided input
- Do NOT invent causes that are not supported by the input
- If the input is too limited to determine root cause with confidence, say so clearly

Reasoning process:
1. Extract the key facts directly visible in the input
2. Interpret what those facts mean
3. Identify the most likely issue or failure condition
4. Suggest the safest and most relevant next diagnostic or corrective step

Output format:
- Key Facts
- Interpretation
- Likely Issue
- Recommended Next Step

Logs:
{data}
"""

    if input_type == "system_output":
        return f"""You are a Linux systems analyst.

You are analyzing command output from a Linux system.

Rules:
- Do NOT assume a question was asked
- Do NOT inject unrelated topics
- Focus ONLY on interpreting the output
- Do NOT claim an issue unless the output supports it
- If something is uncertain, label it as uncertain

Reasoning process:
1. Extract the important facts shown in the output
2. Explain what each important fact means
3. Identify any confirmed issues, risks, or unusual conditions
4. Recommend next checks only if they are justified by the output

Output format:
- Key Facts
- Interpretation
- Confirmed or Possible Issues
- Recommended Next Checks

Command Output:
{data}
"""

    if input_type == "config":
        return f"""You are a systems configuration expert.

You are analyzing configuration or structured system data.

Rules:
- Do NOT assume prior context
- Focus ONLY on the provided content
- Do NOT infer settings that are not present
- Distinguish clearly between what is explicit and what is inferred

Reasoning process:
1. Extract the major settings, fields, or structures present
2. Explain what they do
3. Identify any important implications, risks, or noteworthy details
4. Suggest any relevant review points if justified by the content

Output format:
- Key Settings or Structure
- What It Does
- Important Details or Risks
- Recommended Review Points

Configuration:
{data}
"""

    if input_type == "query":
        return data

    return f"""You are a technical analysis assistant.

Rules:
- Focus only on the provided input
- Do not assume missing context
- Do not invent facts not present in the input
- State uncertainty clearly when needed

Reasoning process:
1. Extract the important facts from the input
2. Explain what they mean
3. Identify any supported issues or implications
4. Suggest the most relevant next step if appropriate

Output format:
- Key Facts
- Interpretation
- Issues or Implications
- Recommended Next Step

Input:
{data}
"""


def send_request(request, stream=False):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(TIMEOUT)

    try:
        client.connect(SOCKET_PATH)

        client.sendall(json.dumps(request).encode("utf-8"))
        client.shutdown(socket.SHUT_WR)

        if stream:
            while True:
                chunk = client.recv(BUFFER_SIZE)
                if not chunk:
                    break

                print(chunk.decode("utf-8"), end="", flush=True)

            print()
            return None

        chunks = []
        while True:
            chunk = client.recv(BUFFER_SIZE)
            if not chunk:
                break
            chunks.append(chunk)

        response_data = b"".join(chunks).decode("utf-8")
        return json.loads(response_data)

    finally:
        client.close()


def build_request(user_input):
    return {
        "type": "query",
        "user": "richard",
        "mode": "cli",
        "stream": True,
        "data": {
            "input": user_input
        }
    }


def interactive_mode():
    print("\nNeuroCore Interactive Mode")
    print("Type 'exit' or 'quit' to leave\n")

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting NeuroCore...")
                break

            request = build_request(user_input)
            send_request(request, stream=True)

        except KeyboardInterrupt:
            print("\nExiting NeuroCore...")
            break

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)


def main():
    stdin_data = read_stdin()

    if stdin_data:
        input_type = classify_input(stdin_data)
        framed_input = build_contextual_prompt(stdin_data, input_type)

        request = build_request(framed_input)

        try:
            send_request(request, stream=True)

        except socket.timeout:
            print("Error: NeuroCore is initializing. Try again.", file=sys.stderr)
            sys.exit(1)

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)
            sys.exit(1)

        return

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        request = build_request(user_input)

        try:
            send_request(request, stream=True)

        except socket.timeout:
            print("Error: NeuroCore is initializing. Try again.", file=sys.stderr)
            sys.exit(1)

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        interactive_mode()


if __name__ == "__main__":
    main()