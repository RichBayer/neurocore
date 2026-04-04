# NeuroCore System Architecture

> NOTE:
> This system was originally named "Jarvis".
> It has since been renamed to "NeuroCore".
> References to "Jarvis" reflect the original name during development.

---

# Compute Node

Primary machine: Lenovo Legion Desktop

CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  
OS: Windows 11 with WSL2 Ubuntu  

NeuroCore currently runs primarily on this workstation.

Although the system is currently hosted on a single machine, the architecture is designed so that components may later be distributed across multiple nodes for scalability.

---

# Storage Layout

Primary NVMe (G:)

G:\ai
models
runtime
memory
projects
logs
backups

External HDD (4TB)

Archive storage  
camera recordings  
AI memory archive  
system backups  

This structure keeps all NeuroCore data visible, portable, and easy to back up.

---

# System Architecture (Layered)

NeuroCore is built as a layered system:

Interface Layer  
↓  
Transport Layer (Daemon + Socket)  
↓  
Runtime Layer  
↓  
Logic Layer  
↓  
Knowledge Layer  
↓  
Model Layer  

---

# Interface Layer

Provides user interaction with the system.

Current:

CLI  
[scripts/ai_cli.py](../../scripts/ai_cli.py)

Future:

Open WebUI  
Mobile devices (via Tailscale)  
Tablets  
Voice nodes  

The interface layer sends structured requests into the system.

---

# Transport Layer

Components:

Daemon  
[runtime/neurocore_daemon.py](../../runtime/neurocore_daemon.py)

Socket:

/tmp/neurocore.sock  

Responsibilities:

Maintain persistent process  
Accept client connections  
Normalize requests  
Stream responses back to clients  

This layer decouples the interface from the runtime.

---

# Runtime Layer

File:

[runtime/runtime_manager.py](../../runtime/runtime_manager.py)

Responsibilities:

Process incoming requests  
Coordinate system behavior  
Route requests to the logic layer  

This acts as the system’s central controller.

---

# Logic Layer

File:

[scripts/jarvis_router.py](../../scripts/jarvis_router.py)

Responsibilities:

Interpret user requests  
Determine intent  
Build prompts  
Interact with AI models  
Stream responses  

Key functions:

run_query()  
run_query_stream()  

---

# Knowledge Layer

File:

[scripts/query_knowledge.py](../../scripts/query_knowledge.py)

Core components:

Chroma – vector database  
Embedding model  

Responsibilities:

Index documents  
Store embeddings  
Retrieve relevant context  

Data location:

/mnt/g/ai/memory/knowledge  
/mnt/g/ai/memory/chroma  

This enables retrieval augmented generation (RAG).

---

# Model Layer

Runtime:

Ollama (local LLM runtime)

Endpoint:

http://localhost:11434

Responsibilities:

Generate responses  
Provide streaming output  

---

# Streaming Pipeline (Core Feature)

Streaming is implemented across the full system:

Ollama (streaming API)  
↓  
Router (generator yields chunks)  
↓  
Daemon (forwards chunks over socket)  
↓  
CLI (prints in real time)  

This enables:

Real-time responses  
Improved user experience  
Foundation for future interfaces (UI, voice, API)

---

# Execution Flow (Current System)

1. User runs:

   ai "query"

2. CLI sends request to daemon via UNIX socket

3. Daemon:
   - normalizes request
   - forwards to runtime manager

4. Runtime Manager:
   - routes to logic layer

5. Logic Layer:
   - retrieves knowledge context
   - builds prompt
   - sends request to Ollama

6. Ollama streams response

7. Response propagates back:

   Router → Daemon → CLI

8. CLI prints output in real time

---

# Runtime Behavior

Cold Start:

Embedding model loads  
Vector database initializes  
First query slower  

Warm State:

No reinitialization  
Fast streaming responses  

---

# Memory Layer

Separate from knowledge system.

Types:

Conversation memory  
User memory  
System memory  

Memory must remain isolated per user.

---

# Tool Execution Layer

Allows interaction with external systems.

Examples:

System diagnostics  
Internet search  
Automation commands  
Development tools  

The logic layer determines when tools are used.

---

# Perception Layer (Future)

Potential inputs:

Microphones  
Cameras  
Sensors  
Smart devices  

This enables environmental awareness.

---

# Automation Layer (Future)

Powered by Home Assistant.

Controls:

Lights  
Cameras  
Sensors  
Automation rules  

Communication via MQTT or similar protocols.

---

# Distributed Architecture (Future)

Planned node roles:

AI compute node  
Knowledge node  
Automation node  
Interface nodes  

This allows horizontal scaling over time.

---

# Design Principles

Local-first computing  
Transparent filesystem-based state  
Modular architecture  
Persistent runtime  
Real-time streaming  

---

# Current Capabilities

Interactive CLI  
Real-time streaming responses  
Semantic knowledge retrieval (RAG)  
Persistent daemon-based runtime  

---

# Related Documentation

System Map  
[neurocore_system_map.txt](../infrastructure/neurocore_system_map.txt)

Repository Map  
[neurocore_repository_map.txt](../infrastructure/neurocore_repository_map.txt)

Resume Prompt  
[resume_prompt_compressed.md](../ai-operations/resume_prompt_compressed.md)

---

# Next Phase

STDIN ingestion (df -h | ai)  
Session memory  
Tool execution expansion  

---

# Design Goal

Centralized intelligence with distributed interaction points.

One powerful AI core supported by modular subsystems and flexible interfaces.