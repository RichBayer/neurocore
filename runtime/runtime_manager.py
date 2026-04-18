# /mnt/g/ai/projects/neurocore/runtime/runtime_manager.py

from scripts.jarvis_router import run_authorized_query, run_authorized_stream_query
from runtime.control_plane import ControlPlane
from runtime.tracing import trace_event, trace_context_from_request
import re


def is_ambiguous(query: str) -> bool:
    q = query.lower().strip()
    q = re.sub(r"[^\w\s]", "", q)

    words = q.split()

    vague_words = {"what", "does", "that", "mean", "it", "this", "explain"}

    return len(words) <= 5 and all(w in vague_words for w in words)


def no_context_response() -> str:
    return (
        "I do not have enough context to know what you're referring to. "
        "Please include the specific command output, error message, or topic you want explained."
    )


def format_execution_result(result: dict) -> str:
    status = result.get("status")
    message = result.get("message", "")
    data = result.get("data", {})

    if status == "success":
        action = data.get("action", "")
        service = data.get("service", "")
        return f"[OK] {action.upper()} '{service}' → {message}"

    if status == "confirmation_required":
        return (
            f"[CONFIRMATION REQUIRED] {message}\n"
            f"Run: {data.get('confirm_command')}"
        )

    if status == "policy_denied":
        return f"[BLOCKED] {message}"

    if status == "error":
        return f"[ERROR] {message}"

    return str(result)


class RuntimeManager:
    def __init__(self):
        print("Initializing NeuroCore Runtime Manager...")
        self.control_plane = ControlPlane()

    def _prepare_request(self, request):
        """
        Ensure request has 'query' field for control plane compatibility.
        """
        raw_input = request.get("data", {}).get("input", "")
        request["query"] = raw_input
        return request, raw_input

    def handle_request(self, request):
        ctx = trace_context_from_request(request)
        request, raw_input = self._prepare_request(request)

        trace_event(
            event="request_received",
            context=ctx,
            component="runtime_manager",
            details={"input": raw_input}
        )

        if is_ambiguous(raw_input):
            trace_event(
                event="ambiguous_request_blocked",
                context=ctx,
                component="runtime_manager",
                status="blocked"
            )
            return no_context_response()

        if self.control_plane._is_execution_request(request):
            trace_event(
                event="execution_path_detected",
                context=ctx,
                component="runtime_manager"
            )

            result = self.control_plane.process(request)

            trace_event(
                event="execution_result_returned",
                context=ctx,
                component="runtime_manager",
                details={"status": result.get("status")}
            )

            return format_execution_result(result)

        trace_event(
            event="reasoning_path_detected",
            context=ctx,
            component="runtime_manager"
        )

        authorized = self.control_plane.authorize(request)

        response = run_authorized_query(authorized)

        trace_event(
            event="reasoning_response_returned",
            context=ctx,
            component="runtime_manager"
        )

        return response

    def handle_stream_request(self, request):
        ctx = trace_context_from_request(request)
        request, raw_input = self._prepare_request(request)

        trace_event(
            event="stream_request_received",
            context=ctx,
            component="runtime_manager",
            details={"input": raw_input}
        )

        if is_ambiguous(raw_input):
            trace_event(
                event="ambiguous_stream_blocked",
                context=ctx,
                component="runtime_manager",
                status="blocked"
            )
            yield no_context_response()
            return

        if self.control_plane._is_execution_request(request):
            trace_event(
                event="stream_execution_path_detected",
                context=ctx,
                component="runtime_manager"
            )

            result = self.control_plane.process(request)

            trace_event(
                event="stream_execution_result_returned",
                context=ctx,
                component="runtime_manager",
                details={"status": result.get("status")}
            )

            yield format_execution_result(result) + "\n"
            return

        trace_event(
            event="stream_reasoning_path_detected",
            context=ctx,
            component="runtime_manager"
        )

        authorized = self.control_plane.authorize(request)

        for chunk in run_authorized_stream_query(authorized):
            yield chunk

        trace_event(
            event="stream_reasoning_completed",
            context=ctx,
            component="runtime_manager"
        )