# /mnt/g/ai/projects/neurocore/tools/system/users_sessions.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class UsersSessions(BaseTool):

    name = "users_sessions"
    description = "Retrieve currently logged-in users"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        return

    def execute(self, request: Dict[str, Dict]) -> Dict[str, str]:
        ctx = trace_context_from_request(request)
        tool_input = request["input"]

        trace_event(
            event="tool_invoked",
            context=ctx,
            component="users_sessions",
            details={"input": tool_input}
        )

        trace_event(
            event="users_sessions_collection_started",
            context=ctx,
            component="users_sessions"
        )

        result = CommandRunner.run(["who"])

        output = ["Active User Sessions\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="users_sessions_execution_completed",
            context=ctx,
            component="users_sessions",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )