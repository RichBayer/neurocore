# Jarvis System Architecture

## Compute Node

Primary machine: Lenovo Legion Desktop

CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  
OS: Windows 11 with WSL2 Ubuntu

---

## Storage Layout

Primary NVMe (G:)

```
G:\ai
models
runtime
memory
projects
logs
backups
```

External HDD (4TB)

Archive storage  
camera recordings  
AI memory archive  
system backups

---

## AI Runtime Layer

Runs inside WSL Ubuntu.

Core components:

Ollama – model runtime  
Open WebUI – chat interface  
Whisper – speech-to-text  
Piper – text-to-speech  

---

## Interface Layer

User interfaces include:

Tablets  
Voice nodes  
Web interface  
Mobile devices via Tailscale

---

## Logic Layer

The logic layer acts as the control system for Jarvis. It receives requests from the interface layer and determines how the system should respond.

Responsibilities of this layer:

Interpret user requests  
Determine which system capability should be used  
Route requests to the appropriate tool or data source  
Assemble context for the AI model  
Return responses to the interface layer

Possible routing targets include:

Knowledge retrieval  
System diagnostics  
Home automation commands  
Internet search  
External AI models

Conceptual request flow:

User request  
→ Intent detection  
→ Tool selection  
→ Data retrieval  
→ AI reasoning  
→ Response returned to interface

---

## Knowledge Layer

The knowledge layer allows Jarvis to retrieve and use information from local data sources rather than relying only on model training.

Core components:

Chroma – vector database used to store semantic embeddings  
LlamaIndex – document ingestion and retrieval framework

Responsibilities of this layer:

Index local documents and notes  
Store semantic embeddings for retrieval  
Provide relevant context to the AI during queries

Typical knowledge sources may include:

Personal documentation  
GitHub repositories  
System logs  
Technical notes  
Project files

Conceptual workflow:

```
documents
   ↓
text chunking
   ↓
embedding generation
   ↓
vector database storage
   ↓
semantic retrieval
   ↓
context injected into AI prompt
```

This layer enables **retrieval augmented generation (RAG)** so Jarvis can answer questions using locally indexed knowledge.

---

## Perception Layer

Sensors feeding the AI:

Microphones  
Cameras  
Motion sensors  
Door sensors  
Smart devices

---

## Automation Layer

Home Assistant provides integration with:

lights  
cameras  
sensors  
automation rules

Communication handled through MQTT.

---

## Design Goal

Centralized intelligence with distributed interaction points.

One powerful AI brain, many lightweight terminals.