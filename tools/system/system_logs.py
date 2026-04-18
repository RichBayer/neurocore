# /mnt/g/ai/projects/neurocore/tools/system/system_logs.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class SystemLogs(BaseTool):

    name = "system_logs"
    description = "Retrieve recent system logs"
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
            component="system_logs",
            details={"input": tool_input}
        )

        trace_event(
            event="system_logs_collection_started",
            context=ctx,
            component="system_logs"
        )

        result = CommandRunner.run(["journalctl", "-n", "50", "--no-pager"])

        output = ["Recent System Logs\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="system_logs_execution_completed",
            context=ctx,
            component="system_logs",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )