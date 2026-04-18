from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class ProcessTop(BaseTool):

    name = "process_top"
    description = "Retrieve top CPU and memory consuming processes"
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
            component="process_top",
            details={"input": tool_input}
        )

        trace_event(
            event="process_top_collection_started",
            context=ctx,
            component="process_top"
        )

        cpu_result = CommandRunner.run(["ps", "aux", "--sort=-%cpu"])
        mem_result = CommandRunner.run(["ps", "aux", "--sort=-%mem"])

        cpu_lines = cpu_result["stdout"].splitlines()[:6]
        mem_lines = mem_result["stdout"].splitlines()[:6]

        output = ["Top Processes\n"]

        output.append("Top CPU Processes:\n")
        output.extend(cpu_lines)

        output.append("\nTop Memory Processes:\n")
        output.extend(mem_lines)

        trace_event(
            event="process_top_execution_completed",
            context=ctx,
            component="process_top",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )