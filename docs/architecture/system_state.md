# NeuroCore – System State

---

# Purpose

This document represents the **current implementation state of NeuroCore only**.

It defines:

- what exists
- how it behaves
- what is working
- what is NOT yet implemented

This document is used to guide development decisions.

If this document is incorrect, development decisions will be incorrect.

---

# System Identity

NeuroCore is a:

- local-first AI system
- persistent daemon-based runtime
- streaming, context-aware reasoning system
- control plane governed execution system

It is NOT:

- a stateless chatbot
- a request/response script
- an uncontrolled execution system

---

# Current Architecture

All interaction flows through:

CLI / Input  
↓  
UNIX Socket (/tmp/neurocore.sock)  
↓  
NeuroCore Daemon  
↓  
Runtime Manager  
↓  
Control Plane  
├── Execution Path → Execution Engine → Tool  
└── Reasoning Path → Router → Knowledge System → LLM  
↓  
Streaming Response  

---

# Core Components

## Runtime Layer

- `runtime/neurocore_daemon.py`
- `runtime/runtime_manager.py`
- `runtime/control_plane.py`

Responsibilities:

- persistent process
- request handling
- streaming output
- request validation
- request classification
- execution enforcement
- ambiguity interception

---

## Execution Layer (NEW)

- `tools/base_tool.py`
- `tools/tool_registry.py`
- `tools/execution_engine.py`
- `tools/system/service_manager.py`

Responsibilities:

- structured tool interface
- controlled execution entry point
- validation and normalization
- policy-aligned execution

---

## Logic Layer

- `scripts/jarvis_router.py`

Responsibilities:

- query rewriting
- context handling
- routing decisions
- prompt construction

Constraints:

- must operate within control plane constraints
- cannot trigger execution
- cannot bypass policy enforcement

---

## Knowledge System

- `scripts/query_knowledge.py`
- Chroma (vector DB)
- HuggingFace embeddings (MiniLM)

Capabilities:

- semantic retrieval
- metadata-aligned filtering
- command-aware knowledge lookup

---

## Interface Layer

- `scripts/ai_cli.py`
- installed command: `ai`

Capabilities:

- one-shot queries
- interactive mode
- real-time streaming output
- piped input ingestion

---

# Runtime Behavior

## Startup

- daemon starts instantly
- no heavy components loaded

---

## First Query (Cold Start)

- embedding model loads
- Chroma initializes
- retriever initializes

Behavior:

- slower response (~1–2 minutes)

---

## Warm State

- no reinitialization
- fast responses (~1–3 seconds)
- streaming active

---

# Input Capabilities

## Direct Query

```
ai "your query"
```

---

## Interactive Mode

```
ai
> query
> query
> exit
```

---

## Piped Input

```
command | ai
```

---

### Behavior

- classified as external input
- analyzed only
- never executed
- isolated from normal context

---

# Execution Behavior

## Execution Intent Detection

Requests implying system action are:

- detected by control plane
- classified as execution intent

---

## Execution Policy

Execution is governed by tool execution modes:

- auto
- manual
- dry-run

---

## Current Execution Model

- execution is NOT automatic
- execution requires explicit confirmation for manual tools
- no background execution

---

## Example Execution Flow

```
ai "restart nginx"
→ confirmation required

ai "confirm restart nginx"
→ tool execution (simulated)
```

---

## Current Tool

### service_manager

Capabilities:

- start
- stop
- restart
- status

Behavior:

- simulated execution only
- no real system interaction

---

# Ambiguity Handling

Ambiguous queries such as:

- "what does that mean?"
- "explain that"

Are:

- detected at runtime level
- intercepted before processing
- prevented from using context or memory
- responded to safely

---

# Memory System

## Session Memory

Location:

```
/mnt/g/ai/memory/sessions/richard/session.json
```

---

## Capabilities

- rolling conversation history
- multi-turn context
- supports query rewriting

---

## Limitations

- short-term only
- no long-term memory system
- no session boundary control
- manual reset required for clean context

---

# Reasoning Capabilities

## Query Rewriting

- resolves ambiguous follow-ups
- injects missing context

---

## Retrieval Control

- metadata filtering
- prevents cross-command contamination

---

## Response Behavior

- grounded in retrieved knowledge
- supports structured explanations
- constrained by control plane

---

# Knowledge System Behavior

- lazy initialization
- persistent vector database
- optimized after first query

---

# Communication Model

- UNIX socket-based communication
- full request/response lifecycle
- streaming supported end-to-end

---

# Current Capabilities Summary

NeuroCore currently supports:

- persistent daemon runtime
- streaming responses
- CLI interface (`ai`)
- piped input analysis (`| ai`)
- RAG-based knowledge retrieval
- metadata-aligned retrieval
- query rewriting
- session memory (short-term)
- control plane enforcement
- execution intent detection
- controlled tool execution
- confirmation-based execution safety model
- ambiguity handling at runtime level

---

# Known Limitations

NeuroCore does NOT yet have:

- real system command execution
- full policy system
- observability / logging system
- task persistence
- long-term memory
- session lifecycle management

---

# Current Phase

Phase 5 – Execution & Control Architecture

---

# Current Status

Phase 5B – Tool Execution Layer + Safety Model  
Status: COMPLETE

---

# Immediate Focus

- real system execution
- policy expansion
- observability

---

# Development Rules

- do not bypass daemon
- do not bypass control plane
- do not assume automatic execution
- do not assume safe execution
- always validate behavior against runtime

---

# Maintenance

Update this document whenever:

- capabilities change
- architecture evolves
- major features are added

This document must always reflect **actual system behavior**