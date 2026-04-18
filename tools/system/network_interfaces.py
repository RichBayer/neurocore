# /mnt/g/ai/projects/neurocore/tools/system/network_interfaces.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class NetworkInterfaces(BaseTool):

    name = "network_interfaces"
    description = "Retrieve network interfaces and IP addresses"
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
            component="network_interfaces",
            details={"input": tool_input}
        )

        trace_event(
            event="network_interfaces_collection_started",
            context=ctx,
            component="network_interfaces"
        )

        result = CommandRunner.run(["ip", "addr"])

        output = ["Network Interfaces\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="network_interfaces_execution_completed",
            context=ctx,
            component="network_interfaces",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )