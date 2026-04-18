# /mnt/g/ai/projects/neurocore/tools/system/recent_logins.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class RecentLogins(BaseTool):

    name = "recent_logins"
    description = "Retrieve recent user login history"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        return

    def execute(self, request: Dict[str, Dict]) -> Dict[str, str]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="tool_invoked",
            context=ctx,
            component="recent_logins"
        )

        result = CommandRunner.run(["last", "-n", "10"])

        output = ["Recent Login History\n"]
        output.extend(result["stdout"].splitlines())

        return self.build_result(
            status="success",
            message="\n".join(output)
        )