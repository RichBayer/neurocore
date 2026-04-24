# Argus – Output & Tool Execution Contract (V1)

---

## Purpose

This document defines the required behavior and output structure for:

- Argus tools
- System tools (as consumed by Argus)
- Data contracts between layers

This document ensures:

- consistent tool behavior
- compatibility with incident memory
- future model integration readiness
- prevention of architectural drift

This is a strict contract document.

If a tool does not follow this contract, it is considered incorrect.

---

## Core Principle

Argus operates on structured system intelligence, not raw command output.

All tools must produce:

- deterministic results
- structured data
- human-readable summaries

The system must never depend on:

- parsing formatted text
- CLI-specific output
- implicit assumptions

---

## Execution Model (Ground Truth)

All execution follows:

daemon → runtime_manager → control_plane → execution_engine → tool

Tools are NEVER called directly by:

- CLI / ACLI
- router
- model
- external input

---

## Tool Layer Responsibilities

### System Tools

Location:

tools/system/

Responsibilities:

- execute system commands via CommandRunner
- collect raw system signals
- return structured data

Rules:

- MUST use CommandRunner
- MUST NOT perform interpretation
- MUST NOT aggregate multiple concerns
- MUST return structured data

---

### Argus Tools

Location:

tools/argus/

Responsibilities:

- call system tools
- aggregate structured data
- interpret system state
- produce findings and recommendations

Rules:

- MUST NOT call CommandRunner
- MUST NOT execute system commands directly
- MUST consume structured data only
- MUST NOT parse formatted message output

---

## Output Contract (CRITICAL)

ALL tools must return a structured result using:

{
  "status": "success" | "error",
  "tool": "<tool_name>",
  "message": "<human readable output>",
  "data": { ... }
}

---

## Message Field

The message field:

- is intended for human readability (CLI output)
- must be clean and formatted
- must NOT contain duplicated status markers
- must NOT require additional formatting by CLI

---

## Data Field (REQUIRED FOR ARGUS COMPATIBILITY)

The data field is REQUIRED for all system tools and Argus tools.

It is used for:

- Argus tool composition
- incident memory system
- recurrence detection
- future model reasoning

---

## System Tool Data Requirements

System tools MUST return structured data in a consistent, machine-usable format.

Example:

{
  "cpu": {...},
  "memory": {...},
  "disk": {...}
}

System tools MUST NOT:

- return only raw text
- require parsing of message field
- mix formatting with data

---

## Argus Tool Data Requirements

Argus tools MUST return structured interpretation in data.

Minimum required structure:

{
  "severity": "OK" | "WARNING" | "CRITICAL",
  "findings": [
    {
      "severity": "...",
      "message": "...",
      "category": "<optional>"
    }
  ],
  "recommendations": [
    "..."
  ]
}

Optional (future-ready):

"recurrence": {
  "count": <int>,
  "window_days": <int>,
  "message": "..."
}

---

## Severity Model

Allowed severity values:

OK  
WARNING  
CRITICAL  

Rules:

- severity must reflect highest detected issue
- findings may contain mixed severities
- severity must be deterministic

---

## Findings Structure

Each finding must include:

- severity
- message

Optional:

- category (e.g., memory, cpu, disk, service)

Findings must be:

- deterministic
- derived from structured data
- not dependent on natural language parsing

---

## Recommendations

Recommendations must:

- be actionable
- be relevant to findings
- be deterministic (not model-generated in V1)

Recommendations must NOT:

- execute commands
- assume system state changes
- be vague or generic

---

## Incident Memory Integration (V1)

Argus tools MUST support incident memory integration.

### Incident Candidates

Argus tools must internally produce structured incident candidates:

{
  "service": "<service or system>",
  "symptom": "<normalized issue identifier>",
  "severity": "...",
  "signature": "<deterministic signature>"
}

These are NOT automatically stored.

They are:

- generated during diagnostics
- used for recurrence detection
- optionally saved after user confirmation

---

### Storage Model

Stored incidents must follow:

- JSON format
- one file per incident

Location:

~/.argus/incidents/

---

### Recurrence Detection

Recurrence is determined using:

- matching signature
- matching service
- time window

Example:

"This issue has occurred 3 times in the past 14 days."

---

### Rules

Incident memory MUST:

- require user approval before storage
- remain read-only with respect to system state
- NOT influence execution behavior
- NOT trigger automatic fixes

---

## CLI / ACLI Expectations

ACLI consumes:

- message → display to user
- data → internal use (future expansion)

ACLI must NOT:

- reformat tool output
- interpret raw data
- perform logic outside tool system

---

## Command Consistency Requirement

Commands must remain stable and predictable.

Examples:

summary  
processes  
disk  
memory  
logs  
network  

The control plane mapping defines the system API.

---

## Observability Requirements

All tools must:

- use trace_context_from_request()
- emit trace_event() for:
  - invocation
  - execution completion

Trace continuity must be preserved across:

execution_engine → tool → command_runner

---

## Execution Safety Rules

Tools must NEVER:

- bypass the execution engine
- execute commands directly (outside system tools)
- modify system state (V1)
- depend on CLI behavior

---

## Validation Requirements

Tools must:

- validate input via BaseTool
- reject invalid input
- enforce schema requirements

---

## Future Compatibility

This contract ensures compatibility with:

- incident memory system
- recurrence detection
- model reasoning (Ollama)
- future training system (Argus Lab)

---

## Final Rule

If a tool does not follow this contract:

It is incorrect.

---

## Summary

This document defines:

- how tools behave
- how data is structured
- how Argus maintains consistency
- how future systems integrate cleanly

This is the foundation for:

- reliable diagnostics
- system intelligence
- long-term system awareness