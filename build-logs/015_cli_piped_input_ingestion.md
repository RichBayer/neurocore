# Build Log 015 – CLI Piped Input Ingestion

Date: April 2026

---

## Objective

Introduce the ability for NeuroCore to accept input from shell pipelines.

This allows command output to be analyzed directly by the system.

---

## Feature Attempted

NeuroCore CLI was tested with:

    command | ai

Examples:

    echo "hello world" | ai
    du -f | ai

---

## Observed Behavior

### Case 1 – Simple Input

    echo "hello world" | ai

Result:

- CLI successfully receives piped input
- input is forwarded to runtime
- model produces a response

However:

- response is influenced by prior session context
- piped input is NOT treated as a standalone query

---

### Case 2 – Command Output (Failure Case)

    du -f | ai

Result:

- CLI enters repeated error loop:

    CLI Error: EOF when reading a line

- process does not terminate cleanly
- requires manual interruption (Ctrl+C)

---

## Root Cause

The CLI does not distinguish between:

- interactive input (TTY)
- piped input (stdin)

Current behavior:

- CLI always attempts to read using `input()`
- piped input is consumed once
- subsequent reads trigger EOF
- loop continues indefinitely

---

## Architectural Gap Identified

The system currently lacks:

### 1. Input Mode Detection

No distinction between:

- interactive mode
- piped mode

---

### 2. Execution Mode Separation

Piped input should:

- be processed once
- bypass interactive loop
- terminate after response

---

### 3. Context Isolation

Piped input currently:

- shares session memory
- is treated as continuation of prior conversation

Instead, it should:

- operate as a standalone request
- have isolated context

---

## Interpretation

This is not a simple bug.

This is a **missing architectural layer**:

- input classification
- execution mode control
- context isolation

---

## Relation to Phase 5

These issues will be addressed in:

### Phase 5A – Runtime Control Plane

Specifically:

- request typing (query vs piped vs tool)
- execution path selection
- context isolation rules

---

## Current Status

Piped input is:

- partially functional (simple input works)
- unstable for real command output
- not production-ready

---

## Outcome

NeuroCore now has:

- initial external input pathway
- visibility into execution requirements
- a clearly defined boundary between reasoning and execution systems

---

## Next Step

Design and implement:

- input mode detection (TTY vs stdin)
- execution mode branching
- request classification

As part of Phase 5A – Control Plane