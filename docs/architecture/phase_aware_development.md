# NeuroCore / Argus – Phase-Aware Documentation & Development Integration

---

## Purpose

This document defines WHEN and HOW system components must be implemented relative to development phases.

It exists to:

- prevent premature implementation
- avoid architectural rework
- ensure correct build sequencing
- align documentation with actual system state

This is a CONTROL document.

All development and documentation must follow this progression.

---

## Core Principle

NeuroCore is built in layers.

Argus depends on those layers.

Therefore:

Features must ONLY be implemented when their required foundation exists.

---

## System Layer Dependency Model

The system is built in this order:

1. Runtime (daemon, control plane, execution engine)
2. System Tool Layer (data collection)
3. Argus Tool Layer (interpretation)
4. Distribution Layer (ACLI)
5. Intelligence Enhancements (model, memory, training)

Each layer depends on the one before it.

---

## Current Development Position

System is currently in:

## Phase 6 – Distribution Layer (NEXT)

Phase 5J is COMPLETE.

Confirmed capabilities:

- execution engine COMPLETE
- control plane COMPLETE
- system tools ACTIVE
- **structured data model FULLY ENFORCED across all system tools**
- **Argus diagnostic layer FULLY IMPLEMENTED across core domains**
- **deterministic interpretation ACTIVE (severity + findings + recommendations)**

---

## Phase-Based Implementation Rules

---

### Phase 5J (COMPLETE) – Argus Tool Layer

This phase is COMPLETE and serves as a foundational reference.

What was achieved:

- full Argus diagnostic layer across system domains  
- structured output contract enforced across ALL system tools  
- deterministic interpretation pattern established  
- consistent tool composition model (system → Argus)  
- stable control plane routing for diagnostic commands  

Established pattern:

```
system tool → structured data → interpretation → normalized output
```

This pattern is now **canonical** and must be followed for all future Argus development.

---

### MUST have been implemented DURING Phase 5J

(These are now COMPLETE and must be preserved)

#### 1. Structured Output Contract

All tools return:

- message (human-readable)
- data (machine-readable)

Argus tools include:

- severity
- findings
- recommendations

Status: ✅ COMPLETE

---

#### 2. System Tool Data Compliance

ALL system tools:

- return structured data
- do NOT rely on raw text output

Status: ✅ COMPLETE

---

#### 3. Argus Tool Pattern Enforcement

ALL Argus tools:

- consume system tool data
- produce structured findings
- remain deterministic

Status: ✅ COMPLETE

---

#### 4. Command Consistency (Control Plane)

Command patterns stabilized:

summary  
processes  
disk  
memory  
logs  
network  

Status: ✅ STABLE (treated as product API moving forward)

---

#### 5. Incident Memory Integration Points

Defined but NOT implemented:

- incident candidate structure
- generation point (Argus tools)
- deterministic signature approach

Status: ⚠️ DEFINED ONLY (implementation deferred to Phase 6)

---

## MUST NOT be implemented in Phase 5J

(Still applies historically — preserved for reference)

- full installer
- packaging (deb, rpm, etc.)
- multi-distro abstraction
- advanced model integration
- training system (Argus Lab)
- evaluation systems
- automation / remediation

Reason:

Foundation had to be completed first.

---

## Phase 6 – Distribution Layer (CURRENT / NEXT)

This is where Argus becomes a **real user-facing product**.

---

### To be implemented in Phase 6

#### 1. Argus ACLI User Experience Layer (PRIMARY FOCUS)

Create:

```
distributions/argus/cli/acli.py
```

Goals:

- improve CLI output readability  
- structure findings clearly  
- group results by severity  
- refine human-readable summaries  
- make outputs feel like a real tool, not raw data  

Constraints:

- MUST NOT bypass control plane  
- MUST preserve structured output contract  
- MUST consume Argus tool outputs (not system tools directly)

---

#### 2. Runtime Packaging (INITIAL, NOT FINAL)

Bundle:

- runtime/
- tools/
- Argus tools

Ensure:

- clean reproducible setup
- minimal install friction

(NOT full packaging system yet)

---

#### 3. File System Layout (PLANNING LEVEL)

Example:

/opt/argus/  
/opt/argus/runtime/  
/opt/argus/tools/  

User data:

~/.argus/

---

#### 4. Incident Memory (FULL IMPLEMENTATION)

Now that structured diagnostics exist, implement:

- save incident after user confirmation
- store structured diagnostic output
- load historical incidents
- detect recurrence patterns

Reason:

Phase 5J made this possible.

---

## Phase 7 – Intelligence Layer

---

### To be implemented AFTER distribution is stable

#### 1. Model Integration (Ollama)

Capabilities:

- explanation
- reasoning
- follow-up interaction

Model must:

- consume structured data
- NOT replace deterministic logic

---

#### 2. Optional Enhancements

- better log interpretation
- contextual explanations
- deeper diagnostics

---

## Phase 8 – Training System (Argus Lab)

---

### NOT part of ACLI product

Includes:

- scenario generation
- guided troubleshooting
- performance tracking
- coaching behavior

---

## Documentation Integration Rules

When adding documentation:

- Phase 5J docs → architecture/ or design/
- Distribution docs → distributions/argus/
- Contracts → architecture/
- Vision → vision/

---

## Validation Rule

Before implementing ANY feature:

Ask:

1. Does the required lower layer exist?
2. Is structured data available?
3. Does this violate current phase boundaries?

If ANY answer is “no”:

→ STOP

---

## Final Principle

Build in order.

Do NOT:

- skip layers
- mix responsibilities
- introduce future features early

The system must evolve:

capability → interpretation → distribution → intelligence

---

## End State Goal

A system that:

- gathers real system data
- interprets it deterministically
- optionally enhances it with AI
- evolves into a full training and intelligence platform