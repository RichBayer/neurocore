# /mnt/g/ai/projects/neurocore/tools/system/disk_layout.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class DiskLayout(BaseTool):

    name = "disk_layout"
    description = "Retrieve disk and partition layout"
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
            component="disk_layout",
            details={"input": tool_input}
        )

        trace_event(
            event="disk_layout_collection_started",
            context=ctx,
            component="disk_layout"
        )

        result = CommandRunner.run(["lsblk"])

        output = ["Disk Layout\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="disk_layout_execution_completed",
            context=ctx,
            component="disk_layout",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )