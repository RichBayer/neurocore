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

    # Try to parse JSON response
    try:
        response = json.loads(buffer)

        status = response.get("status")
        output = response.get("response")
        error = response.get("error")

        if status == "success":
            print(output)

        elif status == "confirmation_required":
            print(output)

        elif status == "error":
            print(f"[ERROR] {error}")

        else:
            print(buffer)

    except json.JSONDecodeError:
        # fallback for reasoning / non-JSON responses
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