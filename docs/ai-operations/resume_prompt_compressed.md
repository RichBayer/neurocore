# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

---

## Current System State (CRITICAL)

NeuroCore has transitioned from a stateless script-based system into a **persistent daemon-based architecture**.

### Completed Milestones

* Local AI runtime (Ollama) operational
* Knowledge system (Chroma + LlamaIndex) operational
* RAG pipeline functional
* Router logic implemented (`jarvis_router.py`)
* Performance optimized (HTTP API + streaming)

### NEW (Latest Milestone)

* NeuroCore daemon implemented
* UNIX socket IPC established (`/tmp/neurocore.sock`)
* Structured request/response protocol defined
* End-to-end communication verified

Build log reference:

build-logs/009_neurocore_daemon_foundation.md

---

## Environment

Host system:

Lenovo Legion Desktop
Ryzen 7 5800X
32 GB RAM
RTX 3060 12 GB

Operating system:

Windows 11 with WSL2 Ubuntu

Working directory:

~/ai/projects/jarvis

Workspace root:

~/ai → /mnt/g/ai

Python environment:

~/ai/runtime/python/jarvis-env

---

## Pathing Rules (CRITICAL)

The system uses a symlinked workspace.

Primary working path:

~/ai → /mnt/g/ai

All commands should use:

~/ai/...

NOT:

/mnt/g/ai/... (unless explicitly required)

---

## Repository Root

NeuroCore project root:

~/ai/projects/jarvis

All development commands should assume:

cd ~/ai/projects/jarvis

---

## Python Environment

Virtual environment location:

~/ai/runtime/python/jarvis-env

Activation command:

source ~/ai/runtime/python/jarvis-env/bin/activate

All Python execution should occur within this environment.

---

## File Placement Rules

* Runtime code:
  ~/ai/projects/jarvis/runtime/

* Scripts (existing logic):
  ~/ai/projects/jarvis/scripts/

* Build logs:
  ~/ai/projects/jarvis/build-logs/

* Screenshots:
  ~/ai/projects/jarvis/docs/screenshots/

---

## Command Requirements

* Always provide copy/paste-ready commands
* Always assume current directory is:
  ~/ai/projects/jarvis
* Do not invent or assume alternate paths
* If uncertain about a path, ask before proceeding

---

## System Map Reference (Optional)

Detailed system structure is documented in:

docs/infrastructure/home_system_map.md
docs/infrastructure/jarvis_repository_map.txt

Use these only for deeper context—not for guessing paths.

---

## Current Architecture

NeuroCore now follows a **daemon-based architecture**:

Client (CLI / future interfaces)
↓
UNIX Socket (/tmp/neurocore.sock)
↓
NeuroCore Daemon
↓
(Runtime Manager – NOT YET IMPLEMENTED)
↓
Router (jarvis_router.py)
↓
Knowledge System + Model

---

## Current Capability

NeuroCore can:

* receive structured requests
* process them through daemon
* return structured responses

⚠️ The system does NOT yet perform real reasoning through the daemon

---

## Current Limitation (TOP PRIORITY)

NeuroCore does NOT yet have a persistent runtime layer.

This means:

* router is NOT loaded inside daemon
* knowledge system is NOT persistent
* each query is NOT yet using the real AI pipeline

---

## Current Phase

We are entering the **Runtime Integration Phase**

---

## Immediate Goal (NEXT STEP)

Build the **Runtime Manager**

This component will:

* initialize ONCE at daemon startup
* load:

  * router
  * knowledge system (Chroma + LlamaIndex)
* process queries without reinitialization
* replace placeholder response with real AI output

---

## Target Behavior (Near-Term)

```bash
ai "Explain my system"
df -h | ai
ai
```

All routed through the daemon.

---

## Request Format (LOCKED)

All requests follow:

{
"type": "query" | "event",
"user_id": "richard",
"client_id": "cli",
"session_id": "default",
"payload": {
"text": "..."
}
}

---

## Design Principles

* build the correct architecture first
* avoid temporary or throwaway solutions
* keep components modular
* maintain separation of concerns:

  * daemon (processing)
  * client (interface)
  * runtime (state)
* no overengineering, no shortcuts

---

## Development Style

* explain WHY before implementation
* move in small, controlled steps
* validate each step before proceeding
* do not assume previous steps succeeded
* stop at logical checkpoints
* document milestones with build logs + screenshots

---

## What You Should Do

Act as a senior systems engineer guiding development.

* provide exact commands
* validate each step before proceeding
* prevent architectural mistakes
* keep implementation aligned with vision

---

## Session Discipline

Before ending a session:

* update build logs
* update system maps if needed
* update this prompt if state changes

Do not assume context persists between sessions.

---

## Current Focus

Focus ONLY on:

* runtime manager implementation
* integrating router into daemon
* eliminating repeated initialization

Do NOT:

* build UI
* build voice system
* build perception system

---

## Resume Instruction

Start by implementing:

runtime/runtime_manager.py

Then integrate it into:

runtime/neurocore_daemon.py

Goal:

Replace placeholder response with real query processing.
