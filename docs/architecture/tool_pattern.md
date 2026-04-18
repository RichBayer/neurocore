# NeuroCore – Tool Pattern (Ground Truth)

---

# Purpose

This document defines how tools ACTUALLY work in NeuroCore.

This is not a theoretical design.

This is based on:

- BaseTool implementation
- system_info tool (first real tool)
- execution engine behavior
- real build results and failures

This document exists so future tools are built consistently and correctly.

---

# Core Principle

Tools do NOT define execution behavior.

NeuroCore does.

Tools are:

> Controlled execution units that run inside the system

All tools must follow the same lifecycle and structure.

---

# Execution Flow (REAL)

All tool execution follows this exact path:

control_plane  
→ execution_engine  
→ tool.validate_request()  
→ tool.execute()  
→ build_result()  
→ runtime  
→ CLI  

Tools are never called directly by:

- CLI
- router
- model
- external input

---

# Tool Structure (REQUIRED)

Every tool must define:

- name
- description
- input_schema
- execution_mode

From BaseTool:

```
name: str
description: str
input_schema: Dict
execution_mode: "auto" | "manual" | "dry-run"
```

---

# Input Model

All tools receive a full request object:

```
{
  "tool": "...",
  "input": {...},
  "trace": {...}
}
```

Tools must:

- extract from request["input"]
- NOT modify request structure
- NOT generate new trace context

---

# Validation Model

Validation is enforced BEFORE execution:

execution_engine → tool.validate_request()

BaseTool handles:

- required field validation
- input type validation
- schema enforcement

Each tool must implement:

```
def validate_input(self, tool_input)
```

---

# Execution Pattern (MANDATORY)

All tools must follow this pattern inside execute():

---

## 1. Extract Context

```
ctx = trace_context_from_request(request)
tool_input = request["input"]
```

---

## 2. Emit Invocation Trace

```
trace_event(
    event="tool_invoked",
    context=ctx,
    component="<tool_name>",
    details={"input": tool_input}
)
```

---

## 3. Perform Execution Logic

- Use CommandRunner for ALL system interaction
- No direct subprocess usage
- No external execution paths

Example:

```
CommandRunner.run([...])
```

---

## 4. Emit Completion Trace

```
trace_event(
    event="<tool_name>_execution_completed",
    context=ctx,
    component="<tool_name>",
    status="success"
)
```

---

## 5. Return Result

ALL tools must return using:

```
return self.build_result(
    status="success",
    message="<formatted output>"
)
```

---

# Command Execution Rule (CRITICAL)

ALL system interaction must go through:

tools/system/command_runner.py

Tools must NEVER:

- import subprocess
- execute shell commands directly
- bypass CommandRunner

---

# Output Contract (REAL)

All tools return:

```
{
  "status": "success" | "error",
  "tool": "<tool_name>",
  "message": "<human readable output>",
  "data": {...} (optional)
}
```

---

## IMPORTANT

The CLI uses:

- status
- message

Tools must ensure:

> message is already readable and formatted

---

# Formatting Rule

Tools are responsible for formatting their output.

NOT the CLI.

This was validated during system_info build:

- CLI expects a clean message
- tools must NOT include duplicate status markers (ex: [OK])

---

# Execution Modes

## auto

- executes immediately
- used for read-only tools

## manual

- requires confirmation
- enforced by control plane

## dry-run

- does not execute
- returns advisory output only

---

# Trace Integration

All tools must:

- use existing trace context
- emit trace events
- NOT generate new request IDs

Trace must remain continuous across:

execution_engine → tool → command_runner

---

# What Tools MUST NOT Do

Tools must NOT:

- bypass execution engine
- modify system state (in current phase)
- create new execution paths
- return raw unformatted command output
- depend on CLI formatting
- assume routing behavior

---

# What Tools ARE Responsible For

Tools ARE responsible for:

- validating input
- executing controlled commands
- formatting output clearly
- emitting trace events
- returning structured results

---

# system_info – Reference Implementation

system_info is the first real tool and defines the working pattern.

Key behaviors:

- uses trace_context_from_request()
- emits trace_event lifecycle
- validates structured input
- uses CommandRunner exclusively
- formats output internally
- returns via build_result()

All future tools must follow this model.

---

# Key Lessons from Real Build

From Phase 019:

- Control plane must explicitly map execution triggers
- Daemon serialization must be correct (JSON boundary is critical)
- CLI must remain simple
- Tools must NOT format for CLI incorrectly
- Output must be clean, not duplicated

---

# Contract vs Behavior (IMPORTANT)

The tool contract is fixed across all tools.

What changes between tools is:

- execution_mode (auto / manual / dry-run)
- level of validation
- whether system state is modified

The execution lifecycle does NOT change.

This ensures:

- consistent system behavior
- predictable execution flow
- safe expansion into more powerful tools

---

# Final Rule

If a tool does not match this pattern:

It is incorrect.

---

# Purpose Going Forward

This document ensures:

- consistent tool behavior
- clean expansion of system capabilities
- stable foundation for Argus

All future tools must follow this pattern exactly.