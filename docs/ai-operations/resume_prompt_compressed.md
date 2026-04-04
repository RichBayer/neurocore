# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

* Do NOT guess system state, paths, or architecture
* If something is unclear → ASK before proceeding
* Always use real paths from this system
* Always provide copy/paste-ready commands
* Move one step at a time (no multi-step jumps)
* Explain WHY before implementation
* Validate each step before continuing
* Never assume code works—test it
* Never introduce temporary fixes that break architecture later

---

# 🧠 CURRENT SYSTEM STATE (CRITICAL)

NeuroCore is now a **persistent, stateful daemon-based AI system with a functional CLI interface**

---

## ✅ COMPLETED CAPABILITIES

* UNIX socket daemon (`/tmp/neurocore.sock`)
* Runtime Manager (persistent processing layer)
* Router integrated into runtime
* Knowledge system refactored to lazy initialization
* Embedding model loads ONLY on first query
* Chroma vector DB persists across queries
* Full request → response pipeline operational
* CLI interface implemented (`scripts/ai_cli.py`)
* System command available:

    ai "your query"

* Stable IPC communication (no deadlocks, no crashes)
* Second query executes in ~3–5 seconds (no re-init)

---

## 🔥 KEY ARCHITECTURAL WIN (IMPORTANT)

Previously:

* knowledge system initialized at import time ❌

Now:

* knowledge system initializes ONLY on first query ✅
* system startup is instant ✅
* runtime controls initialization lifecycle ✅

---

## 🔥 NEW ARCHITECTURAL WIN (CLI + IPC)

The system now includes a fully functional interface layer.

Key fixes implemented:

* request normalization (daemon boundary)
* full socket read handling (no partial reads)
* client request termination (`shutdown(SHUT_WR)`)
* daemon response signaling
* broken pipe protection (no daemon crashes)
* deadlock between client and daemon resolved

Result:

* stable request/response lifecycle
* persistent daemon never crashes
* CLI communicates reliably with runtime

---

# ⚠️ LESSONS LEARNED (DO NOT REPEAT THESE MISTAKES)

### 1. Python Module Execution

DO NOT run:

python runtime/neurocore_daemon.py ❌

ALWAYS run:

python -m runtime.neurocore_daemon ✅

---

### 2. Absolute Imports ONLY

All internal imports must be:

from scripts.query_knowledge import ...
from runtime.runtime_manager import ...

---

### 3. NO Heavy Initialization at Import

NEVER do this again:

embed_model = ...
chroma_client = ...
retriever = ...

at global scope ❌

---

### 4. Persistent System Behavior

Expected behavior:

Startup:

* instant
* no model load

First query:

* initializes knowledge system
* may take longer
* CLI may timeout

Second query:

* fast
* no reinitialization

---

### 5. Socket Communication Rules

Client MUST signal end of request:

client.shutdown(socket.SHUT_WR)

Daemon MUST handle:

* partial reads
* client disconnects
* response completion

Failure to do this results in:

* deadlocks
* broken pipe crashes
* inconsistent behavior

---

# 🏗️ CURRENT ARCHITECTURE

CLI (`ai` command)
↓
UNIX Socket (/tmp/neurocore.sock)
↓
NeuroCore Daemon
↓
Runtime Manager (persistent state)
↓
Router (`jarvis_router.py`)
↓
KnowledgeBase (lazy-loaded)
↓
Chroma + Embeddings
↓
Ollama (LLM)

---

# 📁 PATHING RULES (CRITICAL)

Workspace root:

~/ai → /mnt/g/ai

Project root:

~/ai/projects/jarvis

ALWAYS use:

~/ai/...

NEVER default to:

/mnt/g/...

---

# 📁 KEY DIRECTORIES

* Runtime:
  ~/ai/projects/jarvis/runtime/

* Scripts:
  ~/ai/projects/jarvis/scripts/

* Build logs:
  ~/ai/projects/jarvis/build-logs/

* Screenshots:
  ~/ai/projects/jarvis/docs/screenshots/

* Knowledge DB:
  ~/ai/memory/chroma

---

# 🧪 EXECUTION RULES

Activate environment:

source ~/ai/runtime/python/jarvis-env/bin/activate

Shortcut:

jarvisenv

Run daemon:

python -m runtime.neurocore_daemon

Run CLI:

ai "your query"

---

# 🧾 DOCUMENTATION RULES (MANDATORY)

Every milestone MUST include:

1. Build log
2. Screenshots
3. Embedded image markdown
4. Explanation of:

   * what was built
   * why it was built
   * issues encountered
   * how issues were resolved

---

# 📸 SCREENSHOT RULES

Screenshots must prove behavior:

1. CLI timeout (cold start)
2. Daemon initialization
3. CLI fast response (warm state)

Naming format:

neurocore-<component>-<behavior>.png

---

# 📦 REQUIRED FILES FOR NEW SESSION

If context is missing, request:

* System State File
* Home System Map
* Repository Map
* NeuroCore Vision Document

Located in:

docs/infrastructure/
docs/architecture/

---

# 🧠 DEVELOPMENT STYLE

Act as a senior systems engineer.

* prioritize correct architecture over speed
* avoid temporary hacks
* maintain separation of concerns:

  * daemon = communication
  * runtime = state
  * router = logic

* verify before moving forward

---

# 🎯 CURRENT PHASE

CLI Interface Layer COMPLETE ✅

---

# 🚀 NEXT PHASE

CLI Usability + Interaction Layer

---

# 🎯 NEXT OBJECTIVE

Improve CLI usability beyond single-command execution.

Target usage:

ai
> interactive session

df -h | ai   (future)

---

# 🔧 NEXT IMPLEMENTATION TARGET

Enhance CLI to support:

1. Interactive mode

   ai
   > continuous conversation

2. Improved usability

   * persistent session loop
   * clean prompt handling
   * graceful exit

---

# 🧭 RESUME INSTRUCTION

Start with:

Interactive CLI design

Then implement:

Interactive mode inside scripts/ai_cli.py

Goal:

Transform CLI from single-command tool into a usable conversational interface.