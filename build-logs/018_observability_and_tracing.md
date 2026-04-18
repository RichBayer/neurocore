# 018 – Observability & Tracing Implementation

## Objective

The goal of this phase was to make NeuroCore fully observable.

Up to this point, the system worked, but it was essentially a black box. You could send it a command and get a result, but there was no clear visibility into how the system made decisions or what happened internally.

This phase focused on:

- Tracking a request from start to finish
- Making system decisions visible
- Verifying execution safety behavior
- Eliminating guesswork when debugging

---

## Starting State

Before this phase:

- No traceability between components
- No shared request identity
- No visibility into execution decisions
- Debugging required assumptions instead of evidence

---

## Phase 1 – Tracing Foundation

A core tracing system was introduced to generate structured logs for every major system action.

This included:

- A trace context (`request_id`, source, metadata)
- A `trace_event()` function for consistent logging
- JSON-based structured output

### Validation

![Trace Module Validation](../docs/screenshots/observability-tracing/01_trace_module_validation.png)

Result:

- Tracing system successfully initialized
- Logs confirmed writing to `/mnt/g/ai/logs/neurocore_trace.log`

---

## Phase 2 – CLI Trace Injection

The CLI was updated to generate a trace context for every request.

Each request now includes:

- `request_id`
- `source`
- `trace` block

### Result

![CLI Trace Injection](../docs/screenshots/observability-tracing/02_cli_trace_injection.png)

Observation:

- Trace context successfully included in outgoing requests

---

## Phase 3 – Runtime Manager Tracing

Tracing was added to the runtime manager to track:

- Request intake
- Path selection (reasoning vs execution)
- Response return

### Initial Result

![Initial Runtime Trace](../docs/screenshots/observability-tracing/03_runtime_tracing_initial.png)

---

## Issue Encountered

Initially, trace logs did not appear.

### Root Cause

The daemon was still running an older version of the code.

### Fix

Restarted the daemon to reload updated modules.

---

## Phase 4 – Trace ID Mismatch

At this point, traces were being generated, but something was clearly off.

### Observed Issue

- The CLI generated a `request_id`
- The runtime manager showed a different `request_id`
- The control plane showed yet another one

### Evidence

![Trace ID Mismatch](../docs/screenshots/observability-tracing/04_trace_id_mismatch.png)

---

## Root Cause

The issue was traced back to how incoming requests were processed inside the daemon.

Specifically, the function:

```
normalize_request() in runtime/neurocore_daemon.py
```

was unintentionally dropping the `trace` field.

This meant:

- The CLI created a valid request_id
- The daemon removed it
- Each downstream component generated a new one

Result:

A single request looked like multiple unrelated events.

---

## Fix

The fix was implemented in:

```
runtime/neurocore_daemon.py
```

The `normalize_request()` function was updated to preserve the incoming `trace` block instead of discarding it.

### Result

![Trace ID Fixed](../docs/screenshots/observability-tracing/05_trace_id_fixed.png)

After the fix:

- One request = one request_id
- All components shared the same trace context
- End-to-end trace continuity restored

---

## Phase 5 – Execution Detection Regression

After fixing trace propagation, a new issue appeared.

### Observed Issue

Execution commands were no longer being recognized correctly.

Example:

```
ai "restart nginx"
```

Instead of triggering execution logic, the system responded with a general explanation.

### Evidence

![Execution Detection Broken](../docs/screenshots/observability-tracing/06_execution_detection_broken.png)

---

## Root Cause

The control plane expects a field called `query`.

However, after restructuring the request, the runtime manager was no longer providing it correctly.

---

## Fix

The runtime manager was updated to explicitly inject:

```
query = input
```

before passing the request to the control plane.

### Result

![Execution Detection Fixed](../docs/screenshots/observability-tracing/07_execution_detection_fixed.png)

Execution detection restored:

- Commands correctly classified
- Control plane engaged
- Confirmation flow working again

---

## Phase 6 – Control Plane Tracing

Tracing was expanded into the control plane.

This allowed visibility into:

- Execution detection
- Confirmation checks
- Tool resolution
- Policy enforcement

### Result

![Control Plane Trace](../docs/screenshots/observability-tracing/08_control_plane_tracing.png)

This was the first time the system’s decision-making process became fully visible.

---

## Phase 7 – Execution Engine Tracing

Tracing was added to the execution engine to show:

- Tool lookup
- Validation
- Execution lifecycle

### Result

![Execution Engine Trace](../docs/screenshots/observability-tracing/09_execution_engine_tracing.png)

This clearly showed the transition from decision-making to actual execution.

---

## Phase 8 – Tool-Level Tracing

Tracing was added inside the tool layer (`service_manager`).

### Issue Observed

Trace continuity broke again at this layer.

### Evidence

![Tool Trace Break](../docs/screenshots/observability-tracing/10_tool_trace_break.png)

---

## Root Cause

The execution engine was only passing:

```
tool.execute(input)
```

This meant the tool received no trace context and generated a new request_id.

---

## Fix

Two changes were made:

1. Execution engine updated to pass the full request:

```
tool.execute(request)
```

2. Tool updated to extract trace context from the request

### Result

![Tool Trace Fixed](../docs/screenshots/observability-tracing/11_tool_trace_fixed.png)

Now:

- Tool shares same request_id
- No trace breaks
- Full continuity achieved

---

## Final Result – Full Trace Chain

![Full Trace Success](../docs/screenshots/observability-tracing/12_full_trace_success.png)

---

## Final System Behavior

A single request now flows cleanly through:

```
CLI
→ Runtime Manager
→ Control Plane
→ Execution Engine
→ Tool
→ Execution Engine
→ Control Plane
→ Runtime Manager
```

All under a single:

```
request_id
```

---

## Capabilities Achieved

- Full request traceability
- Execution visibility
- Verified safety enforcement
- Deterministic debugging
- Structured logging across all layers

---

## Key Takeaways

1. Trace context must be preserved at every layer  
2. Small assumptions can break system-wide visibility  
3. Observability requires intentional design  
4. Debugging becomes trivial when the system is transparent  

---

## Outcome

NeuroCore now has a fully observable architecture.

Every request can be traced, every decision can be inspected, and every execution can be verified.

This lays the foundation for:

- real system tools
- automation workflows
- Argus analysis capabilities