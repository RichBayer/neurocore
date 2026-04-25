# /mnt/g/ai/projects/neurocore/tools/system/users_sessions.py

from __future__ import annotations
from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class UsersSessions(BaseTool):

    name = "users_sessions"
    description = "Retrieve active user sessions"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        r = CommandRunner.run(["who"])

        data = {
            "raw": {
                "stdout": r.get("stdout", ""),
                "stderr": r.get("stderr", ""),
                "returncode": r.get("returncode"),
            }
        }

        return self.build_result(
            status="success",
            message="User sessions collected",
            data=data
        )