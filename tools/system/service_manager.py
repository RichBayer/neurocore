# /mnt/g/ai/projects/neurocore/tools/system/service_manager.py

from __future__ import annotations

from typing import Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError


class ServiceManager(BaseTool):

    name = "service_manager"
    description = "Manage system services (start, stop, restart, status)"
    execution_mode = "manual"

    input_schema = {
        "required": ["action", "service"]
    }

    VALID_ACTIONS = {"start", "stop", "restart", "status"}

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        action = tool_input.get("action")
        service = tool_input.get("service")

        if action not in self.VALID_ACTIONS:
            raise ToolValidationError(
                f"Invalid action '{action}'. Valid actions: {self.VALID_ACTIONS}"
            )

        if not isinstance(service, str) or not service.strip():
            raise ToolValidationError("Service name must be a non-empty string")

    def execute(self, request: Dict[str, Dict]) -> Dict[str, str]:
        ctx = trace_context_from_request(request)

        tool_input = request["input"]

        trace_event(
            event="tool_invoked",
            context=ctx,
            component="service_manager",
            details={"input": tool_input}
        )

        action = tool_input["action"]
        service = tool_input["service"]

        trace_event(
            event="tool_action_prepared",
            context=ctx,
            component="service_manager",
            details={"action": action, "service": service}
        )

        message = f"[SIMULATED] {action} executed on service '{service}'"

        trace_event(
            event="tool_execution_simulated",
            context=ctx,
            component="service_manager",
            status="success"
        )

        result = self.build_result(
            status="success",
            message=message,
            data={
                "action": action,
                "service": service,
                "mode": "simulation"
            }
        )

        trace_event(
            event="tool_result_built",
            context=ctx,
            component="service_manager",
            status="success"
        )

        return result