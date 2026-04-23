# Idea: Argus ACLI Incident Memory + Recurrence Detection

---

## Metadata

- Status: Backlog  
- Priority: Medium  
- Category: Architecture / Argus ACLI / Data System  
- Origin: Email / Concept Capture  
- Date: 2026-04-21  

---

## Summary

Introduce a structured **incident memory system** for Argus ACLI that captures resolved issues and enables detection of recurring faults over time.

This system will:

- persist resolved incidents (with user approval)  
- build system-specific operational history  
- detect recurring failure patterns  
- surface recurrence insights during diagnostics  

---

## Core Concept

This is NOT “AI memory”.

This is:

> Structured, system-derived incident history with deterministic recurrence awareness.

The system captures real troubleshooting outcomes and turns them into:

- reusable knowledge  
- pattern detection  
- operational awareness  

---

## Problem This Solves

Current Argus ACLI behavior:

- does not persist resolved issues  
- does not track recurrence over time  
- does not provide historical awareness  

This leads to:

- repeated troubleshooting of the same issues  
- lack of visibility into unstable systems  
- no accumulation of operational knowledge  

---

## Structure / Design

### Incident Capture Flow

After issue resolution, Argus prompts:

> “Do you want to save this as a resolved incident?”

If approved, store:

- system context (host, service)  
- observed symptoms  
- actions taken  
- resolution  
- timestamp  

---

### Storage Model (v1)

- Local-only storage  
- JSON-based structure  
- One file per incident  
- Human-readable and portable  

Location:

```
~/.argus/incidents/
```

No external dependencies.

---

### Recurrence Detection (v1)

Simple deterministic pattern detection based on:

- repeated incidents involving the same service  
- similar symptom patterns  
- frequency within a defined time window  

Example output:

> “This nginx failure has occurred 3 times in the past 14 days.”

---

### Output Behavior

- surfaced during diagnostics  
- non-intrusive  
- informational only  
- does NOT modify system state  
- does NOT apply fixes automatically  

---

## Design Constraints

- Must remain within Argus read-only model  
- No automatic system changes  
- No execution outside control plane  
- Human confirmation required for storage  
- Implementation must remain simple and deterministic  

---

## Integration Points

- Argus Tool Layer (diagnostic output)  
- Execution Engine (data collection boundaries)  
- Control Plane (confirmation enforcement)  
- Future memory systems (optional integration)  

---

## Strategic Purpose

- reduce repeated troubleshooting effort  
- build system-specific operational history  
- improve awareness of unstable components  
- enhance decision-making for admins  
- move Argus toward long-term system understanding  

---

## Success Indicators

- reduced repetition of identical troubleshooting workflows  
- detection of recurring system faults  
- meaningful recurrence insights surfaced during diagnostics  
- consistent and structured incident data  

---

## Risks

- inconsistent data quality across incidents  
- uncontrolled growth of incident files  
- weak matching if structure is not enforced  

---

## Mitigation

- enforce structured incident schema  
- keep v1 matching logic simple  
- introduce pruning/retention strategy later  
- validate usefulness before expanding  

---

## Dependencies / Execution Gate

This idea should NOT be implemented until:

- Argus tool layer is more complete  
- core diagnostic workflows are stable  
- structured output across tools is reliable  

---

## Long-Term Vision

- enriched recurrence detection (pattern refinement)  
- correlation across multiple services  
- integration with higher-level analysis systems  
- optional aggregation into broader system intelligence  

---

## Notes

This is a **data system**, not an AI feature.

Focus on:

- structure  
- determinism  
- reliability  

Avoid:

- premature complexity  
- over-engineering pattern matching  
- conflating with general AI memory systems  