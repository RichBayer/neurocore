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

Phase 5J – Argus Tool Layer Expansion

Confirmed capabilities:

- execution engine COMPLETE
- control plane COMPLETE
- system tools ACTIVE
- structured data model PARTIAL
- Argus tools STARTED (system_summary)

---

## Phase-Based Implementation Rules

---

### Phase 5J (CURRENT) – Argus Tool Layer

Allowed work:

- build Argus tools
- expand system tool coverage
- enforce structured data output
- define output contracts
- establish deterministic diagnostics

Required focus:

- structured system data (CRITICAL)
- consistent tool behavior
- clean separation between system and Argus tools

---

### MUST be implemented DURING Phase 5J

These are foundational and must NOT be delayed:

#### 1. Structured Output Contract

All tools must return:

- message (human-readable)
- data (machine-readable)

Argus tools MUST include:

- severity
- findings
- recommendations

Reason:

This enables:

- memory system
- future model reasoning
- tool composition

---

#### 2. System Tool Data Compliance

ALL system tools must:

- return structured data
- NOT rely on raw text output

Reason:

Argus tools depend on data, not message parsing.

---

#### 3. Argus Tool Pattern Enforcement

ALL Argus tools must:

- consume system tool data
- produce structured findings
- remain deterministic

Reason:

This is the core of Argus behavior.

---

#### 4. Command Consistency (Control Plane)

Command patterns must stabilize:

summary  
processes  
disk  
memory  
logs  
network  

Reason:

This becomes the product API.

---

#### 5. Incident Memory Integration Points

NOT full implementation.

BUT must define:

- incident candidate structure
- where candidates are generated (Argus tools)
- deterministic signature approach

Reason:

Prevents rework when memory system is added.

---

## MUST NOT be implemented in Phase 5J

These introduce premature complexity:

- full installer
- packaging (deb, rpm, etc.)
- multi-distro abstraction
- advanced model integration
- training system (Argus Lab)
- evaluation systems
- automation / remediation

Reason:

Foundation is not complete yet.

---

## Phase 6 – Distribution Layer (NEXT)

This is where Argus becomes a product.

---

### To be implemented in Phase 6

#### 1. ACLI Interface

Create:

distributions/argus/cli/acli.py

Responsibilities:

- wrap NeuroCore CLI behavior
- provide user-friendly command interface
- maintain control plane flow

---

#### 2. Runtime Packaging

Bundle:

- runtime/
- tools/
- Argus tools

Ensure:

- clean install
- reproducible environment

---

#### 3. File System Layout

Example:

/opt/argus/
/opt/argus/runtime/
/opt/argus/tools/

User data:

~/.argus/

---

#### 4. Incident Memory (FULL IMPLEMENTATION)

Now implement:

- save incident after user confirmation
- load incident history
- recurrence detection

Reason:

Now enough structured data exists.

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