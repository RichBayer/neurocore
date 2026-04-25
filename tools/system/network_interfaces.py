# /mnt/g/ai/projects/neurocore/tools/system/network_interfaces.py

from __future__ import annotations
from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class NetworkInterfaces(BaseTool):

    name = "network_interfaces"
    description = "Retrieve network interface information"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="network_interfaces_collection_started",
            context=ctx,
            component="network_interfaces"
        )

        r = CommandRunner.run(["ip", "a"])

        data = {
            "raw": {
                "stdout": r.get("stdout", ""),
                "stderr": r.get("stderr", ""),
                "returncode": r.get("returncode"),
            }
        }

        return self.build_result(
            status="success",
            message="Network interfaces collected",
            data=data
        )