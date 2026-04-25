# Argus Tool Layer – Design

---

# Objective

Introduce the Argus Tool Layer as a composition layer on top of system tools.

This layer will:

- aggregate multiple system tool outputs
- interpret system signals
- produce structured, human-meaningful results
- remain strictly read-only
- fully respect control plane and execution boundaries

---

# Architecture Impact

NeuroCore currently supports:

control_plane → execution_engine → system_tool → command_runner

We are extending this to:

control_plane → execution_engine → argus_tool
→ system_tool(s)
→ command_runner (only inside system tools)
→ argus_tool
→ execution_engine

---

# Key Constraints

Argus tools MUST:

- inherit from BaseTool
- be registered in tool_registry
- use system tools as their ONLY data source
- NEVER call CommandRunner directly
- NEVER execute subprocess directly
- remain read-only
- return structured output

---

# Tool Behavior Model

Each Argus tool will:

1. Receive request from execution engine
2. Call one or more system tools directly
3. Aggregate results
4. Interpret findings
5. Return structured response

---

# Initial Tool Target

First tool to implement:

system_summary

Reason:

- defined in manifest
- low complexity
- exercises multi-command aggregation
- validates composition pattern

---

# Output Model

All Argus tools must return:

- status
- message
- structured data (interpreted)

No raw command dumps allowed.

---

# Deterministic Presentation Layer (CRITICAL)

Argus tools must include a **deterministic presentation layer** as part of their output.

This exists for a specific reason:

NeuroCore must support a **no-model installation mode**, where no LLM is present.

In that mode:

- Argus is the ONLY source of interpretation  
- There is no model to “explain” results  
- Output must already be usable by a human  

---

## What This Means

Argus tools are responsible for:

- producing clear, human-readable summaries  
- formatting findings in a consistent way  
- presenting recommendations in a usable format  

Example:

Instead of returning:

Network Analysis [WARN]

The tool should return something like:

⚠ Network Issue Detected  
• 1 interface is down  

Recommendation:  
→ Check interface configuration  

---

## What This Is NOT

This is NOT:

- natural language generation  
- conversational output  
- dynamic phrasing  
- model-like behavior  

The presentation layer must remain:

- deterministic  
- rule-based  
- consistent for identical inputs  

Same input → same output, always.

---

## Why This Matters

Without this layer:

- output is technically correct but hard to use  
- users must interpret system data manually  
- no-model installs feel incomplete  

With this layer:

- Argus is immediately useful without a model  
- output feels intentional and readable  
- system behavior remains fully trustworthy  

---

## Architectural Boundary

This presentation layer lives inside Argus tools.

It must NOT:

- rely on external reasoning  
- call any model  
- introduce variability  

Future model integration will sit **on top of this layer**, not replace it.

---

# Enforcement Boundary

The following must remain true:

- execution_engine only dispatches top-level tool
- Argus tools do NOT call execution_engine
- system tools remain the ONLY execution primitives
- CommandRunner remains isolated

---

# Success Criteria

- Argus tool successfully composes system tool outputs
- No violation of execution boundaries
- Output is human-readable and structured
- Trace context preserved
- Output is readable and usable without a model

---

# Next Step

Implement first Argus tool:

tools/argus/system_summary.py