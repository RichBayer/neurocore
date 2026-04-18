# /mnt/g/ai/projects/neurocore/tools/system/network_connections.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class NetworkConnections(BaseTool):

    name = "network_connections"
    description = "Retrieve active network connections and listening ports"
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
            component="network_connections",
            details={"input": tool_input}
        )

        trace_event(
            event="network_connections_collection_started",
            context=ctx,
            component="network_connections"
        )

        result = CommandRunner.run(["ss", "-tulnp"])

        output = ["Network Connections\n"]
        output.extend(result["stdout"].splitlines())

        trace_event(
            event="network_connections_execution_completed",
            context=ctx,
            component="network_connections",
            status="success"
        )

        return self.build_result(
            status="success",
            message="\n".join(output)
        )