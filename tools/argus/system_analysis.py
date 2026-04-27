from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class SystemAnalysis(BaseTool):

    name = "system_analysis"
    description = "Aggregate system-level diagnostics"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_system_analysis_invoked",
            context=ctx,
            component="system_analysis"
        )

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        highest_severity = "OK"
        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]

        raw_outputs = {}

        # -------------------------
        # DISK
        # -------------------------
        disk_tool = registry.get("disk_analysis")
        if not disk_tool:
            raise ToolValidationError("disk_analysis tool not available")

        disk_result = disk_tool.execute(request)
        disk_data = disk_result.get("data", {})

        findings.extend(disk_data.get("findings", []))
        recommendations.extend(disk_data.get("recommendations", []))

        disk_severity = disk_data.get("severity", "OK")
        if severity_priority.index(disk_severity) > severity_priority.index(highest_severity):
            highest_severity = disk_severity

        raw_outputs["disk"] = disk_data.get("raw", {})

        # -------------------------
        # MEMORY
        # -------------------------
        memory_tool = registry.get("memory_analysis")
        if not memory_tool:
            raise ToolValidationError("memory_analysis tool not available")

        memory_result = memory_tool.execute(request)
        memory_data = memory_result.get("data", {})

        findings.extend(memory_data.get("findings", []))
        recommendations.extend(memory_data.get("recommendations", []))

        memory_severity = memory_data.get("severity", "OK")
        if severity_priority.index(memory_severity) > severity_priority.index(highest_severity):
            highest_severity = memory_severity

        raw_outputs["memory"] = memory_data.get("raw", {})

        # -------------------------
        # NETWORK
        # -------------------------
        network_tool = registry.get("network_analysis")
        if not network_tool:
            raise ToolValidationError("network_analysis tool not available")

        network_result = network_tool.execute(request)
        network_data = network_result.get("data", {})

        findings.extend(network_data.get("findings", []))
        recommendations.extend(network_data.get("recommendations", []))

        network_severity = network_data.get("severity", "OK")
        if severity_priority.index(network_severity) > severity_priority.index(highest_severity):
            highest_severity = network_severity

        raw_outputs["network"] = network_data.get("raw", {})

        # -------------------------
        # PROCESSES (NEW)
        # -------------------------
        process_tool = registry.get("process_top_analysis")
        if not process_tool:
            raise ToolValidationError("process_top_analysis tool not available")

        process_result = process_tool.execute(request)
        process_data = process_result.get("data", {})

        findings.extend(process_data.get("findings", []))
        recommendations.extend(process_data.get("recommendations", []))

        process_severity = process_data.get("severity", "OK")
        if severity_priority.index(process_severity) > severity_priority.index(highest_severity):
            highest_severity = process_severity

        # Flatten raw output
        process_raw = process_data.get("raw", {})
        for key, value in process_raw.items():
            raw_outputs[key] = value

        # -------------------------
        # FINAL
        # -------------------------

        message = f"System Analysis [{highest_severity}]"

        trace_event(
            event="argus_system_analysis_completed",
            context=ctx,
            component="system_analysis",
            status="success"
        )

        return self.build_result(
            status="success",
            message=message,
            data={
                "severity": highest_severity,
                "findings": findings,
                "recommendations": recommendations,
                "raw": raw_outputs
            }
        )