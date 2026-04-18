# /mnt/g/ai/projects/neurocore/tools/execution_engine.py

from __future__ import annotations

from typing import Any, Dict

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import ToolValidationError, ToolExecutionError
from tools.tool_registry import registry


class ExecutionEngine:
    def __init__(self) -> None:
        self.registry = registry

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="execution_started",
            context=ctx,
            component="execution_engine",
            details={"request_keys": list(request.keys())}
        )

        try:
            if "tool" not in request:
                raise ToolValidationError("Missing tool field")

            if "input" not in request:
                raise ToolValidationError("Missing input field")

            tool_name = request["tool"]

            trace_event(
                event="tool_lookup_started",
                context=ctx,
                component="execution_engine",
                details={"tool": tool_name}
            )

            tool = self.registry.get(tool_name)

            if not tool:
                trace_event(
                    event="tool_lookup_failed",
                    context=ctx,
                    component="execution_engine",
                    status="error",
                    details={"tool": tool_name}
                )
                return {
                    "status": "error",
                    "error_type": "tool_not_found",
                    "message": f"Tool '{tool_name}' not found",
                }

            trace_event(
                event="tool_lookup_completed",
                context=ctx,
                component="execution_engine",
                status="success",
                details={"tool": tool.name}
            )

            tool.validate_request(request)

            trace_event(
                event="tool_validation_completed",
                context=ctx,
                component="execution_engine",
                status="success"
            )

            trace_event(
                event="tool_execution_started",
                context=ctx,
                component="execution_engine",
                details={"tool": tool.name}
            )

            # 🔥 PASS FULL REQUEST (FIX)
            result = tool.execute(request)

            if not isinstance(result, dict):
                raise ToolExecutionError("Invalid result format")

            trace_event(
                event="tool_execution_completed",
                context=ctx,
                component="execution_engine",
                status="success",
                details={"tool": tool.name, "result_status": result.get("status")}
            )

            return result

        except ToolValidationError as e:
            return {
                "status": "error",
                "error_type": "validation_error",
                "message": str(e),
            }

        except ToolExecutionError as e:
            return {
                "status": "error",
                "error_type": "execution_error",
                "message": str(e),
            }

        except Exception as e:
            return {
                "status": "error",
                "error_type": "internal_error",
                "message": str(e),
            }