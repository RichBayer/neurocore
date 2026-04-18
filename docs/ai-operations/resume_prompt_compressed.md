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

---

# 🧠 CONTEXT LOADING PROTOCOL (MANDATORY)

At the start of EVERY new thread:

1. Ask the user to upload ALL required documents
2. Ingest ALL documents silently
3. Do NOT analyze or act yet
4. Wait for explicit task instruction

🚨 If any required document is missing → STOP and ask for it

---

# 📂 REQUIRED DOCUMENTS (LOAD IN THIS ORDER)

Prompt the user to upload the following:

---

## 🔹 1. SYSTEM STATE (SOURCE OF TRUTH)

1. system_state.md  

Purpose:

- defines current architecture  
- defines real system capabilities  
- prevents incorrect assumptions  

---

## 🔹 2. REPOSITORY STRUCTURE

2. neurocore_repository_map.txt  

Purpose:

- ensures correct file paths  
- prevents directory guessing  
- enforces real repo alignment  

---

## 🔹 3. EXECUTION ARCHITECTURE

3. tool_execution.md  

Purpose:

- defines execution flow  
- defines tool system rules  
- defines CommandRunner constraints  

---

## 🔹 4. CORE ARCHITECTURE (IF PROVIDED)

(Optional but recommended if available)

- control_plane.md  
- system_architecture.md  
- neurocore_master_blueprint.md  

Purpose:

- deeper understanding of system design  
- prevents architectural drift  

---

## 🔹 5. ARGUS SYSTEM DESIGN (REQUIRED FOR THIS PHASE)

4. argus_v1_blueprint.md  
5. acli_spec.md  
6. argus_tool_manifest.md  

Purpose:

- defines WHAT tools must exist  
- defines HOW Argus tools behave  
- defines expected outputs and scope  
- prevents building incorrect or duplicate tools  

🚨 These are REQUIRED before implementing ANY Argus tools

---

## 🔹 6. (OPTIONAL) CURRENT BUILD CONTEXT

(Optional)

- latest build log (e.g. build-logs/020_*.md)

Purpose:

- understand recent changes  
- maintain continuity  

---

# 🧠 AFTER DOCUMENT LOAD

- Confirm ingestion is complete  
- Do NOT assume next steps  
- Ask:

> "What is the task for this phase?"

---

# 🧠 EDITING RULES (CRITICAL)

- ALWAYS provide complete file replacements  
- NEVER provide partial edits  
- ALL files must be in a single code block  
- Use four backticks (````)  

---

# 🧠 BUILD PHASE WORKFLOW (MANDATORY)

Before starting ANY build phase:

---

## 1. Create Design File

```
docs/design/<feature>.md
```

Must define:

- objective  
- approach  
- architecture impact  
- constraints  

---

## 2. Create Screenshot Directory

```
docs/screenshots/<feature-name>/
```

---

## 3. Define Screenshot Plan

Before running commands:

```
01_name.png
02_name.png
03_name.png
```

---

## 4. Capture DURING Build

Capture:

- failures  
- broken states  
- fixes  
- final output  

Do NOT reconstruct later.

---

## 5. Build Log Written LAST

Location:

```
build-logs/
```

Rules:

- Must reflect REAL events  
- Must embed screenshots inline  
- Must read naturally  

---

# 🧠 DOCUMENTATION REQUIREMENTS

All changes must include:

- Build log  
- Updated system_state.md (if needed)  
- Updated architecture docs (if needed)  

No feature is complete without documentation alignment.

---

# 🧠 SYSTEM IDENTITY

NeuroCore is:

- a local-first AI system  
- a persistent daemon-based runtime  
- a control-plane governed execution system  

It is NOT:

- a chatbot  
- a stateless script  

---

# 🧠 PLATFORM MODEL

NeuroCore = platform  
Argus = distribution  

Argus:

- defines user experience  
- uses tools  
- never bypasses control plane  

---

# 🧠 TOOL ARCHITECTURE (CRITICAL)

NeuroCore has TWO tool layers:

---

## 1. System Tool Layer (COMPLETE)

Location:

```
tools/system/
```

Purpose:

- direct system execution  
- raw system signals  
- read-only (current phase)  

Rules:

- uses CommandRunner  
- one tool = one capability  
- no aggregation  
- no interpretation  

---

## 2. Argus Tool Layer (CURRENT PHASE)

Location:

```
tools/argus/
```

Purpose:

- compose system tools  
- aggregate multiple signals  
- produce structured outputs  

Rules:

- MUST NOT call CommandRunner directly  
- MUST use system tools  
- MUST remain read-only  

---

# 🧠 CURRENT CAPABILITIES (REAL STATE)

- Persistent daemon  
- Control plane enforcement  
- Execution engine  
- Tool registry + BaseTool contract  
- CommandRunner (real system execution)  

System tools implemented:

- system_info  
- process_top  
- disk_usage  
- memory_usage  
- disk_layout  
- network_interfaces  
- network_connections  
- uptime_load  
- system_logs  
- users_sessions  
- recent_logins  
- service_manager (simulated)  

- Full observability + tracing  

---

# 🎯 CURRENT PHASE

Phase 6 – Argus Tool Layer

---

# 🎯 CURRENT FOCUS

- Build Argus tool layer  
- Follow tool manifest EXACTLY  
- Compose system-level insights  
- Maintain strict execution boundaries  

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer:

- architecture first  
- no shortcuts  
- no system breakage  
- validate everything  

---

# 🧭 RESUME INSTRUCTION

Continue with:

- Argus tool layer implementation  
- manifest-driven tool development  
- strict control plane enforcement  