# /mnt/g/ai/projects/neurocore/tools/system/memory_usage.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class MemoryUsage(BaseTool):

    name = "memory_usage"
    description = "Retrieve system memory usage"
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
            component="memory_usage",
            details={"input": tool_input}
        )

        trace_event(
            event="memory_usage_collection_started",
            context=ctx,
            component="memory_usage"
        )

        result = CommandRunner.run(["free", "-h"])

        output = ["Memory Usage\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="memory_usage_execution_completed",
            context=ctx,
            component="memory_usage",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )