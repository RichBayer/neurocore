# NeuroCore – System Architecture

---

# Purpose

This document defines the architectural structure of NeuroCore, including:

- system layers
- execution flow
- component responsibilities
- system boundaries

This document reflects actual system design, not future assumptions.

---

# System Definition

NeuroCore is a:

- persistent daemon-based system
- local-first cognitive runtime
- control-plane governed execution system

It is NOT:

- a stateless request/response tool
- a simple chatbot
- a direct command execution engine

---

# Architectural Model

NeuroCore is composed of layered systems.

---

## Layer 1 – Distribution Layer (NEW)

This layer defines how NeuroCore is exposed and packaged for users.

Examples:

- Argus (system intelligence distribution)

This layer:

- defines user experience
- constrains system behavior
- selects capabilities

This layer does NOT:

- modify runtime behavior
- bypass control plane
- directly execute commands

---

## Layer 2 – Interface Layer

Handles all user interaction.

Examples:

- CLI (ai)
- Argus CLI (future wrapper)
- future UI / voice interfaces

Responsibilities:

- input collection
- output streaming
- session handling

---

## Layer 3 – Runtime Layer (Core System)

The central execution system.

Components:

- NeuroCore Daemon
- Runtime Manager
- Control Plane

Responsibilities:

- persistent system state
- request lifecycle management
- routing authority
- policy enforcement

All system activity must pass through this layer.

---

## Layer 4 – Execution Layer

Handles controlled system interaction.

Components:

- Execution Engine
- Tool Registry
- Tool Interface

Responsibilities:

- structured tool execution
- controlled system access
- enforcement of execution rules

Execution Path:

    control_plane → execution_engine → tool

---

## Layer 5 – Logic Layer

Responsible for reasoning and routing.

Components:

- Router (jarvis_router.py)

Responsibilities:

- query rewriting
- context resolution
- prompt construction
- routing decisions

Constraints:

- cannot execute commands
- must obey control plane

---

## Layer 6 – Knowledge Layer

Responsible for retrieval and contextual understanding.

Components:

- Chroma vector database
- embedding model
- retrieval system

Capabilities:

- semantic search
- metadata filtering
- contextual grounding

---

## Layer 7 – Model Layer

Responsible for AI processing.

Components:

- local LLM runtime (Ollama)

Responsibilities:

- response generation
- reasoning support

---

## Layer 8 – System Config Layer

Location:

    /mnt/g/ai/system/

Contains:

- personalities
- profiles
- system state

Responsibilities:

- define system behavior configuration
- define user-level behavior patterns
- support distribution customization

---

# Execution Flow

All system interaction follows a strict pipeline:

    Interface Layer
        ↓
    UNIX Socket
        ↓
    NeuroCore Daemon
        ↓
    Runtime Manager
        ↓
    Control Plane
        ↓

        [ Execution Path ]                 [ Reasoning Path ]

        Execution Engine                  Logic Layer (Router)
        ↓                                 ↓
        Tool                              Knowledge System
                                          ↓
                                          Model Runtime (Ollama)

        ↓
    Streaming Response

---

# Core Architectural Rule

All behavior must pass through:

    daemon → runtime_manager → control_plane

Nothing:

- executes
- accesses memory
- interacts with system resources

without passing through the control plane.

---

# System Invariants

## Forbidden

- bypassing the runtime
- raw command execution
- uncontrolled tool usage
- hidden memory modification

---

## Required

- structured inputs
- structured outputs
- policy enforcement
- observable execution
- controlled system access

---

# Argus Integration

Argus is NOT part of the core runtime.

Argus is:

A distribution layer built on top of NeuroCore.

Argus defines:

- system intelligence behavior
- read-only constraints
- user-facing interface style

Argus does NOT:

- modify execution engine
- bypass control plane
- introduce new execution paths

---

# Platform vs Distribution Model

NeuroCore is:

The platform (core system)

Argus is:

A distribution (product layer)

This enables:

- multiple system configurations
- different user experiences
- reuse of core architecture

---

# Future Expansion Model

Additional distributions may be created:

- Argus (system intelligence)
- HomeCore (home automation)
- DevCore (development assistant)

All distributions must:

- use the same runtime
- obey the same control plane
- use the same execution system

---

# Design Principle

NeuroCore = Cognitive Runtime Platform  
Argus = System Intelligence Distribution

---

# Final Rule

There is only ONE runtime.

Distributions must never create parallel systems.

All intelligence, execution, and control must remain centralized.