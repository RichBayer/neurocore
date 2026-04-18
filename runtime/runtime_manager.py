# /mnt/g/ai/projects/neurocore/runtime/runtime_manager.py

from __future__ import annotations

from typing import Any, Dict

from runtime.control_plane import ControlPlane
from runtime.tracing import trace_event, trace_context_from_request


class RuntimeManager:
    def __init__(self) -> None:
        self.control_plane = ControlPlane()

    # -------------------------
    # STREAM ENTRY (FIXED)
    # -------------------------

    def handle_stream_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Entry point used by daemon for CLI streaming mode.
        """
        ctx = trace_context_from_request(request)

        trace_event(
            event="stream_request_received",
            context=ctx,
            component="runtime_manager",
        )

        try:
            result = self.process(request)

            status = result.get("status", "error")

            # Explicit response handling
            if status == "success":
                response = result.get("output", "")
                error = None

            elif status == "confirmation_required":
                response = result.get("output", "")
                error = None

            elif status == "pass_through":
                response = result.get("query", "")
                error = None

            else:
                response = None
                error = result.get("message", "Unknown error")

            trace_event(
                event="stream_response_built",
                context=ctx,
                component="runtime_manager",
                details={"status": status}
            )

            return {
                "status": status,
                "response": response,
                "error": error,
            }

        except Exception as e:
            trace_event(
                event="stream_request_failed",
                context=ctx,
                component="runtime_manager",
                status="error",
                details={"error": str(e)}
            )

            return {
                "status": "error",
                "response": None,
                "error": str(e),
            }

    # -------------------------
    # CORE PROCESSING
    # -------------------------

    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="runtime_manager_started",
            context=ctx,
            component="runtime_manager",
        )

        raw_input = request.get("data", {}).get("input", "").strip()

        trace_event(
            event="input_received",
            context=ctx,
            component="runtime_manager",
            details={"input": raw_input}
        )

        if not raw_input:
            return {
                "status": "error",
                "message": "Empty input",
            }

        request["query"] = raw_input

        # Check execution path first
        if self.control_plane._is_execution_request(request):
            trace_event(
                event="execution_path_selected",
                context=ctx,
                component="runtime_manager"
            )

            result = self.control_plane.process(request)

            return self._format_execution_result(result)

        # Otherwise, pass through (reasoning path)
        trace_event(
            event="reasoning_path_selected",
            context=ctx,
            component="runtime_manager"
        )

        return {
            "status": "pass_through",
            "query": raw_input,
        }

    # -------------------------
    # FORMAT EXECUTION RESULT
    # -------------------------

    def _format_execution_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        status = result.get("status")

        if status == "confirmation_required":
            confirm_cmd = result.get("data", {}).get("confirm_command", "")
            return {
                "status": "confirmation_required",
                "output": f"[CONFIRM] {result.get('message')}\nRun: {confirm_cmd}"
            }

        if status == "error":
            return {
                "status": "error",
                "message": result.get("message", "Execution failed"),
            }

        if status == "policy_denied":
            return {
                "status": "error",
                "message": result.get("message", "Denied"),
            }

        # SUCCESS CASE
        message = result.get("message", "")
        data = result.get("data", {})

        action = data.get("action")
        service = data.get("service")

        if action and service:
            return {
                "status": "success",
                "output": f"[OK] {action.upper()} '{service}' → {message}"
            }

        return {
            "status": "success",
            "output": f"[OK] {message}"
        }