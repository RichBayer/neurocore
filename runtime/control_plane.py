# /mnt/g/ai/projects/neurocore/runtime/control_plane.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from tools.execution_engine import ExecutionEngine
from tools.tool_registry import registry
from runtime.tracing import trace_event, trace_context_from_request


@dataclass
class AuthorizedRequest:
    normalized_input: str
    session_memory_allowed: bool = True
    external_input_present: bool = False

    class RequestClass:
        value = "reasoning"

    request_class = RequestClass()


class ControlPlane:

    EXECUTION_KEYWORDS = {"start", "stop", "restart", "status"}
    CONFIRM_PREFIX = "confirm "

    def __init__(self) -> None:
        self.execution_engine = ExecutionEngine()

    # -------------------------
    # REASONING COMPATIBILITY
    # -------------------------

    def authorize(self, request: Dict[str, Any]) -> AuthorizedRequest:
        ctx = trace_context_from_request(request)
        text = request.get("data", {}).get("input", "")

        trace_event(
            event="authorize_called",
            context=ctx,
            component="control_plane",
            details={"input": text}
        )

        authorized = AuthorizedRequest(normalized_input=text)

        trace_event(
            event="authorize_completed",
            context=ctx,
            component="control_plane",
            status="success"
        )

        return authorized

    # -------------------------
    # MAIN ENTRY
    # -------------------------

    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)
        query = request.get("query", "").strip()

        trace_event(
            event="process_started",
            context=ctx,
            component="control_plane",
            details={"query": query}
        )

        if not self._is_execution_request(request):
            trace_event(
                event="reasoning_detected",
                context=ctx,
                component="control_plane"
            )
            return {
                "status": "pass_through",
                "message": "Not execution",
            }

        trace_event(
            event="execution_detected",
            context=ctx,
            component="control_plane"
        )

        confirmed = self._is_confirmed(query)
        cleaned_query = self._strip_confirm(query)

        trace_event(
            event="execution_confirmation_checked",
            context=ctx,
            component="control_plane",
            details={"confirmed": confirmed, "cleaned_query": cleaned_query}
        )

        structured = self._build_execution_request({"query": cleaned_query})

        # 🔥 CRITICAL: propagate trace context into execution layer
        if "trace" in request:
            structured["trace"] = request["trace"]

        trace_event(
            event="execution_request_built",
            context=ctx,
            component="control_plane",
            details={"tool": structured.get("tool"), "input": structured.get("input", {})}
        )

        tool = registry.get(structured["tool"])

        if not tool:
            trace_event(
                event="tool_not_found",
                context=ctx,
                component="control_plane",
                status="error",
                details={"tool": structured["tool"]}
            )
            return {
                "status": "error",
                "error_type": "tool_not_found",
                "message": f"Tool '{structured['tool']}' not found",
            }

        trace_event(
            event="tool_resolved",
            context=ctx,
            component="control_plane",
            status="success",
            details={"tool": tool.name, "execution_mode": tool.execution_mode}
        )

        mode = tool.execution_mode

        if mode == "manual" and not confirmed:
            trace_event(
                event="confirmation_required",
                context=ctx,
                component="control_plane",
                status="blocked",
                details={"tool": tool.name, "query": cleaned_query}
            )
            return {
                "status": "confirmation_required",
                "tool": tool.name,
                "message": f"Tool '{tool.name}' requires confirmation",
                "data": {
                    "confirm_command": f'ai "confirm {cleaned_query}"'
                },
            }

        if mode == "dry-run":
            trace_event(
                event="policy_denied_dry_run",
                context=ctx,
                component="control_plane",
                status="blocked",
                details={"tool": tool.name}
            )
            return {
                "status": "policy_denied",
                "message": "Tool is dry-run only",
            }

        trace_event(
            event="execution_forwarded",
            context=ctx,
            component="control_plane",
            details={"tool": structured.get("tool")}
        )

        result = self.execution_engine.execute(structured)

        trace_event(
            event="execution_completed",
            context=ctx,
            component="control_plane",
            details={"result_status": result.get("status")}
        )

        return result

    # -------------------------
    # HELPERS
    # -------------------------

    def _is_execution_request(self, request: Dict[str, Any]) -> bool:
        ctx = trace_context_from_request(request)
        text = request.get("query", "").lower().strip()

        trace_event(
            event="execution_check_started",
            context=ctx,
            component="control_plane",
            details={"query": text}
        )

        if not text:
            trace_event(
                event="execution_check_empty",
                context=ctx,
                component="control_plane"
            )
            return False

        text = self._strip_confirm(text)
        words = text.split()

        if not words:
            trace_event(
                event="execution_check_no_words",
                context=ctx,
                component="control_plane"
            )
            return False

        is_execution = words[0] in self.EXECUTION_KEYWORDS

        trace_event(
            event="execution_check_completed",
            context=ctx,
            component="control_plane",
            details={"first_word": words[0], "is_execution": is_execution}
        )

        return is_execution

    def _is_confirmed(self, query: str) -> bool:
        return query.lower().startswith(self.CONFIRM_PREFIX)

    def _strip_confirm(self, query: str) -> str:
        if query.lower().startswith(self.CONFIRM_PREFIX):
            return query[len(self.CONFIRM_PREFIX):].strip()
        return query

    def _build_execution_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        words = request.get("query", "").lower().split()

        action = words[0] if len(words) > 0 else ""
        service = words[1] if len(words) > 1 else ""

        return {
            "tool": "service_manager",
            "input": {
                "action": action,
                "service": service,
            },
        }