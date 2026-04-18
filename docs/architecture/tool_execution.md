# NeuroCore – Tool Execution Architecture

---

# Purpose

The Tool Execution layer is responsible for performing controlled system actions inside NeuroCore.

It ensures that:

- all execution flows through a single controlled path
- no component executes system actions directly
- execution is validated, authorized, and observable
- system safety is enforced at all times

At this stage, this layer is no longer theoretical. It is now actively executing real system commands through a controlled interface.

---

# Core Principle

All execution must pass through the execution engine.

No tool is called directly by:

- the router
- the model
- the CLI
- any external input

Execution flow is strictly enforced.

---

# Execution Flow

All execution follows this path:

```
client
→ daemon
→ runtime manager
→ control plane
→ execution engine
→ tool
→ command_runner (if real execution)
→ execution engine
→ control plane
→ runtime manager
```

---

# Architectural Role

The Tool Execution layer consists of:

- Execution Engine (orchestration)
- Tool Registry (tool discovery)
- BaseTool contract (standard interface)
- Tools (implementation layer)
- CommandRunner (system execution layer)

---

# Execution Engine

Location:

```
tools/execution_engine.py
```

Responsibilities:

- receive authorized execution requests from control plane
- resolve the correct tool from registry
- validate tool input
- invoke tool execution
- return structured results
- propagate trace context

The execution engine is the ONLY component allowed to invoke tools.

---

# Tool Registry

Location:

```
tools/tool_registry.py
```

Responsibilities:

- maintain list of available tools
- resolve tools by name
- enforce controlled tool availability

---

# BaseTool Contract

Location:

```
tools/base_tool.py
```

Defines:

- tool identity
- input schema
- validation logic
- execution behavior
- result structure

All tools must inherit from BaseTool.

---

# Tool Interface (UPDATED)

Tools no longer receive only input.

They now receive the full execution request.

## Previous Model (deprecated)

```
tool.execute(input)
```

## Current Model

```
tool.execute(request)
```

---

# Request Structure Passed to Tools

Tools receive a structured request:

```json
{
  "tool": "...",
  "input": { ... },
  "trace": {
    "request_id": "...",
    "source": "...",
    "metadata": {}
  }
}
```

---

# Command Execution Layer (NEW)

Location:

```
tools/system/command_runner.py
```

This is the layer that actually interfaces with the operating system.

Responsibilities:

- execute subprocess commands
- enforce timeout limits (10 seconds default)
- capture stdout, stderr, and return codes

Important:

- Tools do NOT call subprocess directly
- All real execution flows through CommandRunner

---

# Why This Matters

This introduces real system interaction while still preserving control.

Without this layer:

- tools would directly execute system commands
- safety and consistency would break
- observability would be harder to maintain

With it:

- execution remains centralized
- behavior stays predictable
- system remains safe and debuggable

---

# Tool Responsibilities

Each tool must:

- validate input using BaseTool contract
- extract required data from `request["input"]`
- NOT modify trace context
- emit trace events using provided context
- return structured results

Tools must NOT:

- generate new request_ids
- bypass execution engine
- execute system commands directly (must use CommandRunner)

---

# Execution Modes

Each tool defines an execution mode:

## auto
- executes immediately
- used for safe, read-only operations

## manual
- requires confirmation before execution

## dry-run
- never executes
- returns advisory response only

---

# Confirmation Model

For manual tools:

1. user issues command  
2. control plane detects execution intent  
3. execution is blocked  
4. confirmation required  
5. user confirms  
6. execution engine proceeds  

---

# Safety Model

The execution system enforces:

- no execution without control plane approval
- no direct execution from model or router
- no execution from piped input
- no bypass of confirmation model
- strict tool validation before execution

Additionally:

- real system execution is restricted to tool definitions
- execution behavior is explicit and auditable

---

# Observability Integration

Execution is fully traceable.

Each step emits structured trace events:

- execution detection
- tool resolution
- validation
- execution start
- execution completion

All events:

- share the same request_id
- are logged centrally
- allow full request lifecycle inspection

---

# Example Execution Trace

```
runtime_manager → execution detected
control_plane   → execution allowed (auto tool)
execution_engine → execution started
execution_engine → tool resolved
execution_engine → validation passed
system_info      → tool invoked
command_runner   → system command executed
execution_engine → execution completed
```

---

# Current Tools

## service_manager

Capabilities:

- start
- stop
- restart
- status

Behavior:

- simulated execution
- confirmation-based
- full trace support

---

## system_info (NEW)

Capabilities:

- hostname
- uptime
- OS info
- CPU
- memory
- disk

Behavior:

- real system execution via CommandRunner
- read-only
- auto execution mode
- full trace support

---

# Outcome

The tool execution system now provides:

- controlled execution flow
- strict safety enforcement
- standardized tool interface
- full trace visibility
- real system interaction (NEW)

---

# Status

Execution Engine: COMPLETE  
Tool Contract: COMPLETE  
Trace Integration: COMPLETE  
Real Execution Layer: ACTIVE  

---

# Next Step

- expand system toolset (process, network, logs)
- introduce more granular execution controls
- improve output formatting for usability