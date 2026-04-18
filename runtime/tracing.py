# /mnt/g/ai/projects/neurocore/runtime/tracing.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import json
import threading
import uuid


TRACE_LOG_PATH = Path("/mnt/g/ai/logs/neurocore_trace.log")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TraceContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


class TraceEmitter:
    """
    Lightweight structured tracing for NeuroCore Phase 5H support.

    Purpose:
    - provide end-to-end request visibility
    - remain simple and architecture-safe
    - avoid overbuilding full observability too early
    """

    def __init__(self, log_path: Path = TRACE_LOG_PATH, enabled: bool = True) -> None:
        self.log_path = log_path
        self.enabled = enabled
        self._lock = threading.Lock()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(
        self,
        event: str,
        context: TraceContext,
        component: str,
        status: str = "info",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not self.enabled:
            return

        payload = {
            "timestamp": utc_now_iso(),
            "request_id": context.request_id,
            "source": context.source,
            "component": component,
            "event": event,
            "status": status,
            "details": details or {},
            "metadata": context.metadata,
        }

        self._print_line(payload)
        self._append_jsonl(payload)

    def _print_line(self, payload: Dict[str, Any]) -> None:
        ts = payload["timestamp"]
        request_id = payload["request_id"]
        component = payload["component"]
        event = payload["event"]
        status = payload["status"]
        details = payload["details"]

        detail_str = ""
        if details:
            serialized = ", ".join(f"{k}={v!r}" for k, v in details.items())
            detail_str = f" | {serialized}"

        print(
            f"[TRACE] {ts} | request_id={request_id} | "
            f"component={component} | event={event} | status={status}{detail_str}"
        )

    def _append_jsonl(self, payload: Dict[str, Any]) -> None:
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


_default_emitter = TraceEmitter()


def get_trace_context(
    source: str = "unknown",
    metadata: Optional[Dict[str, Any]] = None,
) -> TraceContext:
    return TraceContext(source=source, metadata=metadata or {})


def trace_event(
    event: str,
    context: TraceContext,
    component: str,
    status: str = "info",
    details: Optional[Dict[str, Any]] = None,
) -> None:
    _default_emitter.emit(
        event=event,
        context=context,
        component=component,
        status=status,
        details=details,
    )


def trace_context_from_request(request: Dict[str, Any]) -> TraceContext:
    """
    Build a TraceContext from an incoming request payload if present.

    Expected request shape:
    {
        ...
        "trace": {
            "request_id": "...",
            "source": "...",
            "metadata": {...}
        }
    }

    Falls back safely if trace data is absent.
    """
    trace = request.get("trace", {}) if isinstance(request, dict) else {}

    request_id = trace.get("request_id") or str(uuid.uuid4())
    source = trace.get("source") or request.get("source", "unknown")
    metadata = trace.get("metadata") or {}

    return TraceContext(
        request_id=request_id,
        source=source,
        metadata=metadata,
    )