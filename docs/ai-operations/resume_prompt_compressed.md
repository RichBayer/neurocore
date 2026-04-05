# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

* Do NOT guess system state, paths, or architecture  
* If something is unclear → ASK before proceeding  
* Always use real paths from this system  
* Always provide copy/paste-ready commands  
* Deliver full production-quality implementations (no toy or partial builds)  
* Execution should be guided step-by-step when applying changes (one command at a time when needed)  
* Prioritize clean, complete solutions over incremental or temporary approaches  
* Never introduce temporary fixes that break architecture later  
* Assume system is evolving toward production-grade architecture, not experimentation  

---

# 🧠 EDITING RULES (CRITICAL)

* ALWAYS provide **complete file replacements**  
* NEVER provide partial edits or "find/replace" instructions  
* ALL file edits must be delivered in **a single code block**  
* Use **four backticks (````)** for file blocks to preserve triple backticks inside files  
* This rule applies to:
  - code files  
  - markdown files  
  - configs  
  - scripts  

---

# 🧠 ENVIRONMENT ASSUMPTIONS

* User is working inside **VSCode**  
* A terminal is already open  
* Current working directory is:

```
/mnt/g/ai/projects/neurocore
```

* Commands should assume no navigation is required unless explicitly stated  

---

# 🧠 CURRENT SYSTEM STATE (CRITICAL)

NeuroCore is now a **persistent, streaming, context-aware AI system** with:

- session memory  
- query rewriting  
- metadata-aligned retrieval  
- normalized operational knowledge  

---

## ✅ COMPLETED CAPABILITIES

### Core Runtime
* UNIX socket daemon (/tmp/neurocore.sock)  
* Runtime Manager (persistent processing layer)  
* Router integrated into runtime  
* Streaming response pipeline (end-to-end)  

### CLI
* Installed as system command (`ai`)  
* One-shot mode: `ai "query"`  
* Interactive mode (multi-query session)  
* Real-time streaming output  

### Knowledge System (RAG)
* Chroma vector DB (persistent)  
* HuggingFace embeddings (MiniLM)  
* Lazy-loaded KnowledgeBase  
* Metadata-based indexing  
* Command-aware retrieval (df, ps, etc.)  
* Knowledge normalization (clean operational docs, not raw man pages)  

### Memory System
* Session memory stored at:  
  /mnt/g/ai/memory/sessions/richard/session.json  
* Rolling conversation history  
* Multi-turn context support  

### Reasoning Layer
* Query rewriting (resolves follow-up ambiguity)  
* Metadata-aligned retrieval (prevents cross-command contamination)  
* Exact field-level precision (e.g., `Use%`)  

---

## 🔥 MAJOR ARCHITECTURAL WINS

### 1. Streaming Pipeline (Complete)

Ollama (streaming API)  
↓  
Router (generator-based streaming)  
↓  
Daemon (chunk forwarding over socket)  
↓  
CLI (real-time output)  

---

### 2. Context-Aware Reasoning (NEW)

NeuroCore now correctly handles:

* Follow-up questions  
* Context resolution  
* Command-specific retrieval  
* Structured output reasoning  

Example:

"What column shows disk usage percentage?"

→ rewritten to:

"What column in df -h output shows disk usage percentage?"

---

### 3. Retrieval Stability (NEW)

* No cross-command contamination  
* Command-aware filtering  
* Deterministic retrieval behavior  

---

## 🔥 CLI CAPABILITIES

NeuroCore CLI supports:

One-shot mode:
ai "your query"

Interactive mode:
ai
> query  
> query  
> exit  

Exit methods:

* exit / quit  
* CTRL + C  
* CTRL + D  

---

## ⚠️ LESSONS LEARNED

### Core System Lessons

1. Streaming must originate at source  
   → generators must propagate through system  

2. CLI naming conflicts  
   → always verify with: `type ai`  

3. Silent streaming failures  
   → debug generator + daemon loop  

4. Clean separation of concerns  
   * Router = logic  
   * Daemon = transport  
   * CLI = interface  

---

### Advanced System Lessons (NEW)

5. Raw documentation ≠ usable knowledge  
6. Retrieval must be constrained (metadata matters)  
7. Follow-up questions require rewriting  
8. Memory without interpretation is insufficient  
9. Precision requires clean knowledge + strict prompting  

---

# 🏗️ CURRENT ARCHITECTURE

CLI (ai)  
↓  
UNIX Socket (/tmp/neurocore.sock)  
↓  
NeuroCore Daemon  
↓  
Runtime Manager  
↓  
Router (rewrite + memory + prompt)  
↓  
KnowledgeBase (metadata-aware retrieval)  
↓  
Chroma + Embeddings  
↓  
Ollama (LLM)  

---

# 📁 PATHING RULES

Workspace root:  
~/ai  

Project root:  
~/ai/projects/neurocore  

Knowledge:  
/mnt/g/ai/memory/knowledge  

Chroma DB:  
/mnt/g/ai/memory/chroma  

Session Memory:  
/mnt/g/ai/memory/sessions/richard/session.json  

---

# 🎯 CURRENT PHASE

Session memory + query rewriting + metadata-aligned RAG COMPLETE  

---

# 🚀 NEXT PHASE

Tool Execution Layer  

---

# 🎯 NEXT OBJECTIVES

1. Execute real system commands (df, ps, etc.)  
2. Capture and stream command output  
3. Parse structured CLI output  
4. Route queries between tools vs LLM  
5. Add safe execution boundaries  

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer.

* architecture first  
* no shortcuts  
* full implementations over partial edits  
* validate after each change  
* maintain clean separation of concerns  

---

# 🧭 RESUME INSTRUCTION

Start with:

Design and implementation of Tool Execution Layer