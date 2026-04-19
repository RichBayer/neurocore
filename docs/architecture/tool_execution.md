# NeuroCore – Tool Execution Architecture

---

# Purpose

The Tool Execution layer is responsible for performing controlled system actions inside NeuroCore.

It ensures that:

- all execution flows through a single controlled path
- no component executes system actions directly outside approved layers
- execution is validated, authorized, and observable
- system safety is enforced at all times

At this stage, this layer is no longer theoretical. NeuroCore actively executes real system commands through controlled system tools, and the architecture is now being aligned to support the future Argus composition layer without breaking existing execution boundaries.

---

# Core Principle

All execution must pass through the execution engine.

No tool is called directly by:

- the router
- the model
- the CLI / ACLI
- any external input
- any component outside the approved execution path

Execution flow is strictly enforced.

---

# System Invariant

All requests must follow:

```text
daemon → runtime_manager → control_plane → system
```

No component bypasses the control plane.

For execution requests, the execution path begins only after the control plane authorizes the request.

---

# Execution Flow

## Top-Level Execution Flow

All execution requests follow this path:

```text
client
→ daemon
→ runtime_manager
→ control_plane
→ execution_engine
→ tool
→ runtime_manager
→ daemon
→ client
```

If the selected tool is a real system execution tool, the path extends to:

```text
client
→ daemon
→ runtime_manager
→ control_plane
→ execution_engine
→ system_tool
→ command_runner
→ operating system
→ system_tool
→ execution_engine
→ control_plane
→ runtime_manager
→ daemon
→ client
```

This is the active real execution path in the current system.

---

# Architectural Role

The Tool Execution layer consists of:

- Execution Engine (orchestration)
- Tool Registry (tool discovery and availability)
- BaseTool contract (standard interface)
- System Tool Layer (real execution primitives)
- Argus Tool Layer (future composed intelligence layer)
- CommandRunner (direct operating system execution boundary)

These layers do not have the same responsibilities and must remain clearly separated.

---

# Execution Engine

Location:

```text
tools/execution_engine.py
```

Responsibilities:

- receive authorized execution requests from the control plane
- resolve the correct tool from the registry
- validate tool input
- invoke tool execution
- return structured results
- propagate trace context

The execution engine is the only component allowed to invoke top-level tools in response to a user request.

Important:

- the execution engine is an entry orchestration layer
- it dispatches the selected tool for the request
- it is not a recursive dispatcher
- tools do not re-enter the execution engine during internal composition

---

# Tool Registry

Location:

```text
tools/tool_registry.py
```

Responsibilities:

- maintain the list of available tools
- resolve tools by name
- enforce controlled tool availability
- provide a single registry surface for the execution layer

The registry is the authoritative map of what tools exist and can be selected by the execution engine.

---

# BaseTool Contract

Location:

```text
tools/base_tool.py
```

Defines:

- tool identity
- input schema
- validation logic
- execution behavior
- result structure

All tools must inherit from BaseTool.

The BaseTool contract standardizes how tools are invoked and how results are returned through the execution layer.

---

# Tool Interface

Tools receive the full execution request, not just a bare input payload.

## Deprecated Model

```text
tool.execute(input)
```

## Current Model

```text
tool.execute(request)
```

This ensures that tools receive consistent structure and trace context.

---

# Request Structure Passed to Tools

Tools receive a structured request such as:

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

The exact payload may evolve, but tools must continue to rely on the structured request model rather than ad hoc positional input.

---

# Tool Layer Separation

NeuroCore now has two distinct tool layers.

They serve different roles and must not be mixed conceptually.

---

## 1. System Tool Layer

Location:

```text
tools/system/
```

Purpose:

- perform focused, read-only system execution
- gather raw system signals
- return structured results for downstream use

System tools are the execution primitives of the platform.

They are responsible for:

- calling CommandRunner when real system access is required
- returning structured output
- exposing real system state safely
- remaining narrow in scope

System tools must not:

- interpret system behavior at a high level
- aggregate multiple system domains into advisory conclusions
- act like Argus intelligence tools
- bypass CommandRunner and shell out directly by other means

Examples in the current system include:

- system_info
- process_top
- disk_usage
- memory_usage
- disk_layout
- network_interfaces
- network_connections
- uptime_load
- system_logs
- users_sessions
- recent_logins
- service_manager (simulated/manual pattern reference)

---

## 2. Argus Tool Layer

Location:

```text
tools/argus/
```

Purpose:

- compose multiple system-level signals
- aggregate results from system tools
- interpret findings
- produce structured, human-meaningful diagnostic output

Argus tools are not raw execution primitives.

They are the intelligence composition layer for the Argus distribution.

Argus tools must:

- use system tools as their system data source
- remain read-only
- interpret and explain findings
- produce structured outputs appropriate for Argus behavior

Argus tools must not:

- call CommandRunner directly
- execute subprocess commands directly
- bypass system tools for system access
- behave like unmanaged execution code

This preserves the platform/distribution boundary:

- NeuroCore = execution platform
- Argus = intelligence distribution built on top of the platform

---

# Command Execution Layer

Location:

```text
tools/system/command_runner.py
```

This is the only layer that directly interfaces with the operating system for real command execution.

Responsibilities:

- execute subprocess commands
- enforce timeout limits
- capture stdout
- capture stderr
- capture return codes

Important:

- tools do not call subprocess directly
- real command execution is isolated here
- CommandRunner is part of the system tool layer boundary, not the Argus layer

This keeps real execution centralized, predictable, auditable, and safe.

---

# Current Real Execution Model

The active execution model implemented in NeuroCore today is:

```text
control_plane → execution_engine → system_tool → command_runner
```

This is the proven execution pattern established during the real system tool build phases.

Key characteristics:

- control plane decides whether execution is allowed
- execution engine selects and invokes the tool
- the system tool performs scoped execution work
- CommandRunner performs the real operating system call
- results return back up the same controlled path

This is the current source-of-truth execution pattern for real tool execution.

---

# Argus Composition Model

The Argus layer extends the execution architecture without changing the top-level execution boundary.

The intended Argus composition path is:

```text
control_plane → execution_engine → argus_tool
→ system_tool(s)
→ command_runner (only inside system tools)
→ argus_tool
→ execution_engine
```

Important clarification:

- the execution engine dispatches the top-level Argus tool for the request
- the Argus tool may call one or more system tools directly as internal composition primitives
- those system tools remain the only layer allowed to use CommandRunner
- Argus tools do not route back through the execution engine for each internal system-tool call

This preserves clear orchestration boundaries while avoiding nested dispatch behavior.

---

# Why the Separation Matters

Without strict layer separation:

- raw execution and reasoning become mixed together
- system access becomes harder to audit
- Argus could accidentally bypass platform safety
- tools become harder to reason about and maintain

With strict separation:

- system tools remain stable execution primitives
- Argus tools remain intelligence/composition primitives
- safety boundaries stay explicit
- platform behavior remains predictable as capabilities grow

---

# Tool Responsibilities

## System Tool Responsibilities

Each system tool must:

- validate input using the BaseTool contract
- extract required data from `request["input"]`
- use CommandRunner for real command execution when needed
- emit trace events using the provided trace context
- return structured output
- stay narrow and capability-specific

System tools must not:

- generate new request IDs
- bypass the execution engine for top-level requests
- call subprocess directly outside CommandRunner
- perform high-level diagnosis or recommendation logic intended for Argus
- become broad multi-domain intelligence tools

---

## Argus Tool Responsibilities

Each Argus tool must:

- validate input using the BaseTool contract
- use system tools as its data source
- aggregate signals across relevant domains
- interpret results into meaningful findings
- return structured, grounded output suitable for Argus responses
- preserve trace continuity across composed tool usage

Argus tools must not:

- generate new request IDs
- call CommandRunner directly
- execute subprocess commands directly
- modify system state
- bypass system tools for operating system access

---

# Output Model

The two tool layers return different classes of value.

## System Tools

System tools return structured system signals.

They may format results for readability, but their role is still execution and signal retrieval, not broad interpretation.

Examples:

- process listings
- disk usage views
- network state
- log output
- uptime data
- session visibility

## Argus Tools

Argus tools return structured interpreted outputs.

They are responsible for:

- combining relevant system signals
- identifying what matters
- explaining findings in plain language
- recommending next steps without executing them

This is where system capability becomes Argus intelligence.

---

# Execution Modes

Each tool defines an execution mode.

## auto

- executes immediately
- used for safe, read-only operations

## manual

- requires confirmation before execution

## dry-run

- advisory only
- no real execution

Current system emphasis is on safe read-only execution, with manual confirmation retained for higher-risk patterns such as the simulated service manager behavior.

---

# Confirmation Model

For manual tools:

1. user issues command
2. control plane detects execution intent
3. execution is blocked pending confirmation
4. confirmation is required
5. user confirms
6. execution engine proceeds

The confirmation system remains part of the control plane authority model and is not delegated to tools themselves.

---

# Safety Model

The execution system enforces:

- no execution without control plane approval
- no direct execution from the router
- no direct execution from the model
- no unmanaged direct execution from CLI or ACLI
- no bypass of confirmation model for manual tools
- strict tool validation before execution
- strict separation between execution primitives and intelligence composition

Additionally:

- real system execution is restricted to the system tool layer
- Argus remains read-only and interpretive
- execution behavior is explicit and auditable

---

# Observability Integration

Execution is fully traceable.

Each step emits structured trace events across the execution path.

This includes:

- execution detection
- tool resolution
- validation
- execution start
- execution completion

For composed Argus behavior, trace continuity must extend across:

- top-level Argus tool invocation
- internal system tool calls
- CommandRunner usage inside system tools

All events must remain tied to the same request lifecycle.

---

# Example Execution Trace – Current System Tool Path

```text
runtime_manager  → execution detected
control_plane    → execution allowed
execution_engine → execution started
execution_engine → tool resolved
execution_engine → validation passed
system_tool      → tool invoked
command_runner   → system command executed
execution_engine → execution completed
```

This reflects the current active real execution pattern.

---

# Example Execution Trace – Future Argus Composition Path

```text
runtime_manager  → execution detected
control_plane    → execution allowed
execution_engine → argus tool resolved
execution_engine → argus tool invoked
argus_tool       → system tool requested
system_tool      → command execution requested
command_runner   → system command executed
system_tool      → structured result returned
argus_tool       → findings aggregated and interpreted
execution_engine → execution completed
```

This extends the current model without changing the top-level execution boundary.

---

# Relationship to CLI and ACLI

The CLI and ACLI are interface layers.

They may:

- accept user requests
- frame requests correctly
- send requests into the NeuroCore runtime
- present results to the user

They may not:

- execute system commands directly
- bypass the control plane
- bypass the execution engine
- create alternate execution paths

This preserves the same execution architecture across both the NeuroCore platform interface and the Argus distribution interface.

---

# Current Status

Execution Engine: COMPLETE  
Tool Registry: COMPLETE  
BaseTool Contract: COMPLETE  
System Tool Layer: ACTIVE  
CommandRunner: ACTIVE  
Real System Execution: ACTIVE  
Argus Tool Layer: NOT YET IMPLEMENTED  
Argus Composition Boundary: ARCHITECTURALLY DEFINED

---

# Outcome

The Tool Execution architecture now provides:

- controlled top-level execution flow
- strict safety enforcement
- standardized tool contracts
- isolated real operating system execution
- traceable end-to-end execution behavior
- a clear separation between platform execution tools and Argus intelligence tools

This keeps the current NeuroCore execution system accurate to reality while establishing the correct architectural boundary for Argus growth.

---

# Next Step

- keep expanding and stabilizing the system tool layer as needed
- implement the Argus tool layer on top of system tools
- maintain strict read-only enforcement for Argus
- preserve CommandRunner isolation inside the system tool layer
- keep control plane authority intact as capabilities expand