#!/usr/bin/env python3

import sys
import json
import socket
import uuid

SOCKET_PATH = "/tmp/neurocore.sock"


def build_trace(source: str) -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "source": source,
        "metadata": {}
    }


# -------------------------
# ARGUS FORMATTER
# -------------------------

def format_argus_output(output, data):
    severity = data.get("severity", "UNKNOWN")
    findings = data.get("findings", [])
    recommendations = data.get("recommendations", [])
    raw = data.get("raw", {})

    # Clean title
    title = output or ""
    if title.startswith("[OK] "):
        title = title.replace("[OK] ", "", 1)

    if "[" in title:
        title = title.split("[")[0].strip()

    print(f"=== {title} ===\n")
    print(f"Severity: {severity} (Scale: OK < INFO < WARN < CRITICAL)\n")

    # Findings
    if findings:
        print("Findings:")
        for f in findings:
            if isinstance(f, dict):
                msg = f.get("message", str(f))
            else:
                msg = str(f)
            print(f"- {msg}")
        print()

    # Recommendations
    print("Recommendations:")
    if recommendations:
        for r in recommendations:
            print(f"- {r}")
    else:
        print("- None")
    print()

    # RAW OUTPUT (FIXED)
    if isinstance(raw, dict) and raw:
        print("--- RAW OUTPUT ---")

        for section, value in raw.items():
            print(f"\n[{section.upper()}]")

            if isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    print(sub_val)
            else:
                print(value)


# -------------------------
# REQUEST HANDLING
# -------------------------

def send_request(payload):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    client.sendall(json.dumps(payload).encode())
    client.shutdown(socket.SHUT_WR)

    buffer = ""

    while True:
        chunk = client.recv(4096)
        if not chunk:
            break

        buffer += chunk.decode()

    client.close()

    try:
        response = json.loads(buffer)

        status = response.get("status")
        output = response.get("response")
        error = response.get("error")
        data = response.get("data", {})

        if status == "success":

            if isinstance(data, dict) and "severity" in data:
                format_argus_output(output, data)
            else:
                print(output)

        elif status == "confirmation_required":
            print(output)

        elif status == "error":
            print(f"[ERROR] {error}")

        else:
            print(buffer)

    except json.JSONDecodeError:
        print(buffer, end="")


def is_pipe():
    return not sys.stdin.isatty()


def main():
    if is_pipe():
        piped_input = sys.stdin.read()

        payload = {
            "data": {
                "input": piped_input
            },
            "mode": "pipe",
            "source": "cli_pipe",
            "stream": True,
            "trace": build_trace("cli_pipe")
        }

        send_request(payload)
        return

    if len(sys.argv) < 2:
        print("Usage: ai \"your query\"")
        return

    user_input = " ".join(sys.argv[1:])

    payload = {
        "data": {
            "input": user_input
        },
        "mode": "cli",
        "source": "cli_direct",
        "stream": True,
        "trace": build_trace("cli_direct")
    }

    send_request(payload)


if __name__ == "__main__":
    main()