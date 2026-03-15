#!/usr/bin/env python3

"""
Jarvis Logic Router - Initial Prototype

This script represents the first component of the Jarvis Logic Layer.

Responsibilities:
- Accept a user request
- Perform simple intent detection
- Route knowledge queries to the knowledge retrieval tool
"""

import argparse
import subprocess


def detect_intent(user_request: str) -> str:
    """
    Very simple rule-based intent detection.

    For the initial version almost everything will route to
    the knowledge tool.
    """

    request = user_request.lower()

    knowledge_triggers = [
        "what",
        "how",
        "explain",
        "tell me",
        "find",
        "search"
    ]

    for trigger in knowledge_triggers:
        if trigger in request:
            return "knowledge"

    return "knowledge"


def run_knowledge_tool(query: str) -> str:

    command = [
        "python",
        "scripts/query_knowledge.py",
        query
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


def main():

    parser = argparse.ArgumentParser(description="Jarvis Logic Router")
    parser.add_argument("request", help="User request")

    args = parser.parse_args()

    intent = detect_intent(args.request)

    if intent == "knowledge":
        output = run_knowledge_tool(args.request)

        print("\n--- Jarvis Knowledge Context ---\n")
        print(output)


if __name__ == "__main__":
    main()
