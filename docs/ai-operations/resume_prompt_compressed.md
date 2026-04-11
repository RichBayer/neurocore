# NeuroCore Development – Resume Prompt (Compressed)

We are continuing development of my local AI system: **NeuroCore**

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

- Do NOT guess system state, paths, or architecture  
- If something is unclear → ASK before proceeding  
- Always use real paths from this system  
- Always provide copy/paste-ready commands  
- Deliver full implementations (no partial solutions)  
- Do NOT introduce temporary fixes that break architecture later  
- Respect existing system design — do not bypass core components  
- When documents are provided, ingest them silently unless instructed otherwise  
- When documents are provided as part of context loading:
  - ingest them silently
  - do NOT analyze, summarize, or act on them
  - wait until the user explicitly provides a Task before responding with analysis or implementation
  
---

# 🧠 EDITING RULES (CRITICAL)

- ALWAYS provide complete file replacements  
- NEVER provide partial edits  
- ALL files must be in a single code block  
- Use four backticks (````) for markdown/code files  

---

# 🧠 EXECUTION STYLE

- Guide implementation step-by-step when applying changes  
- Prefer small, verifiable steps only when architecturally necessary  
- Validate behavior after each step when needed  

---

# ⚡ BUILD EXECUTION MODE (IMPORTANT)

- Build correct architectural implementations the FIRST time  
- Do NOT create simplified or temporary versions that will be replaced  
- Only break work into steps when architecturally necessary  
- Avoid rework and duplicate effort  
- Optimize for efficient, forward progress  

- All work must remain educational:
  - always explain WHY decisions are made  
  - explain how components fit into the system  

---

# 🧠 GITHUB DOCUMENTATION RULES (MANDATORY)

## Purpose

All documentation must:

- reflect REAL system behavior (not intended behavior)
- be written for humans (natural tone, not robotic)
- explain reasoning, not just outcomes

---

## Build Logs

All build logs MUST:

- follow sequential numbering (e.g. 016_*.md)
- include:
  - problem
  - troubleshooting process
  - root cause
  - fix
  - validation
- include only meaningful troubleshooting (no noise)
- read like a human wrote them

---

## Screenshot Workflow

- define screenshot filenames BEFORE capture  
- use consistent naming:

```
01_name.png
02_name.png
```

- store under:

```
docs/screenshots/<feature>/
```

- embed using:

```markdown
![Description](../docs/screenshots/<folder>/<file>.png)
```

- screenshots must:
  - be cropped
  - show only relevant output
  - support the narrative (problem → fix → validation)

---

## Documentation Consistency Rule

Docs must ALWAYS match:

- actual system behavior
- implemented features

If system changes → docs must be updated in same commit

---

# 🧠 ENVIRONMENT ASSUMPTIONS

- Working in VS Code (Remote WSL)  
- Terminal already open  

Current directory:

```
/mnt/g/ai/projects/neurocore
```

---

# 🧠 SYSTEM IDENTITY

NeuroCore is:

- a local-first AI system  
- a persistent daemon-based runtime  
- a streaming, context-aware reasoning system  
- a **control plane governed execution system**  

It is NOT:

- a chatbot  
- a stateless script  
- a direct LLM wrapper  

---

# 🧠 CURRENT CAPABILITIES (REAL STATE)

## Runtime
- Persistent daemon (UNIX socket: /tmp/neurocore.sock)  
- Runtime Manager (control + orchestration layer)  
- Control Plane (enforces all behavior and execution policy)  
- Streaming pipeline (end-to-end)  

## CLI
- Installed as: `ai`  
- One-shot queries  
- Interactive mode  
- Real-time streaming output  

## Input Modes

### Direct Query
ai "question"

### Interactive
ai → session

### Piped Input
command | ai

- classified as external input  
- analyzed only  
- never executed  

---

## Execution Layer (NEW)

- Tool-based execution system  
- Execution Engine (single execution entry point)  
- Tool Registry (controlled tool availability)  
- BaseTool contract (structured tool interface)  

### Current Tool

- service_manager
  - start / stop / restart / status (SIMULATED)

---

## Execution Behavior

- execution intent detected by control plane  
- execution is NOT automatic  
- execution requires explicit confirmation for manual tools  

### Example

```
ai "restart nginx"
→ confirmation required

ai "confirm restart nginx"
→ execution allowed
```

## Execution Modes

- auto  
- manual (requires confirmation)  
- dry-run (blocked)  

---

## Knowledge System (RAG)

- Chroma vector DB (persistent)  
- HuggingFace embeddings (MiniLM)  
- Metadata-aligned retrieval  
- Command-aware filtering  

---

## Memory

- Session memory (short-term only)  
- Supports multi-turn context  

---

## Reasoning

- Query rewriting  
- Context-aware responses  
- Grounded retrieval  

---

# ⚠️ CURRENT LIMITATIONS

The system does NOT yet have:

- real system command execution (tools are simulated)  
- full policy engine  
- observability / logging  
- task persistence  
- long-term memory  
- session lifecycle management  

---

# 🏗️ CURRENT ARCHITECTURE

CLI / Input  
↓  
UNIX Socket  
↓  
Daemon  
↓  
Runtime Manager  
↓  
Control Plane  
├── Execution Path → Execution Engine → Tool  
└── Reasoning Path → Router → Knowledge → LLM  
↓  
Streaming Response  

---

# 🎯 CURRENT PHASE

Phase 5 – Execution & Control Architecture  

---

# 🎯 CURRENT STATUS

Phase 5B – Tool Execution Layer + Safety Model  
Status: COMPLETE  

---

# 🎯 IMMEDIATE OBJECTIVE

Transition from:

- simulated execution  

To:

- controlled real system execution  

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer:

- architecture first  
- no shortcuts  
- maintain clean separation of concerns  
- do not break working systems  
- validate each step before proceeding  

---

# 🧭 RESUME INSTRUCTION

Start with:

Design for Phase 6 – Real Execution + Policy Expansion

---

# 🧭 SESSION CONTINUITY

## Current Phase
Phase 5 – Execution & Control Architecture

## Last Completed Milestone

Phase 5B complete:

- tool execution layer implemented  
- execution engine integrated  
- control plane governs execution  
- confirmation-based safety model implemented  
- CLI integrated with execution system  
- reasoning and execution paths separated  

## Current Focus

Transition from simulated execution → real execution  

## Next Step

Design and implement safe real system command execution