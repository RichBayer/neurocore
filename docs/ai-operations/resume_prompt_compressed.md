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
- governed by a runtime control plane  

It is NOT:

- a chatbot  
- a stateless script  
- a direct LLM wrapper  

---

# 🧠 CURRENT CAPABILITIES (REAL STATE)

## Runtime
- Persistent daemon (UNIX socket: /tmp/neurocore.sock)  
- Runtime Manager (control + orchestration layer)  
- Control Plane (enforces all behavior)  
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

## Piped Input

command | ai

Example:
du -f | ai

Status:

- fully integrated into control plane
- classified as external input
- executed in analysis mode only
- NOT executable
- isolated from normal context

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
- Controlled during validation scenarios  

---

## Reasoning

- Query rewriting  
- Context-aware responses  
- Grounded retrieval  

---

# ⚠️ CURRENT LIMITATIONS

The system does NOT yet have:

- tool execution layer  
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
↓  
Router  
↓  
Knowledge System  
↓  
Ollama  
↓  
Streaming Response  

---

# 🎯 CURRENT PHASE

Phase 5 – Execution & Control Architecture  

---

# 🎯 CURRENT STATUS

Phase 5A – Runtime Control Plane  
Status: COMPLETE  

---

# 🎯 IMMEDIATE OBJECTIVE

Begin implementing:

- Tool Execution Layer  
- Structured tool interface  
- Controlled execution routing  

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

Design for Phase 5B – Tool Execution Layer

---

# 🧭 SESSION CONTINUITY (UPDATE EACH BUILD SESSION)

## Current Phase
Phase 5 – Execution & Control Architecture

## Last Completed Milestone

Phase 5A complete:

- runtime control plane implemented
- request classification enforced
- piped input isolated and controlled
- execution intent detection implemented
- ambiguity handling enforced at runtime level
- system behavior made deterministic

## Current Focus

Transition from controlled reasoning system → controlled execution system

## Next Step

Design and implement Phase 5B – Tool Execution Layer