# /mnt/g/ai/projects/neurocore/tools/system/uptime_load.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class UptimeLoad(BaseTool):

    name = "uptime_load"
    description = "Retrieve system uptime and load averages"
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
            component="uptime_load",
            details={"input": tool_input}
        )

        trace_event(
            event="uptime_load_collection_started",
            context=ctx,
            component="uptime_load"
        )

        result = CommandRunner.run(["uptime"])

        output = ["System Uptime and Load\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="uptime_load_execution_completed",
            context=ctx,
            component="uptime_load",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )