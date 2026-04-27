# Argus ACLI User Experience Layer – Design

---

## Objective

Transform Argus output from raw diagnostic data into a clean, structured, user-friendly CLI experience.

The system already produces correct diagnostics.

This phase focuses on:

- presentation
- readability
- usability
- consistency

NOT new system intelligence.

---

## Scope

This phase operates at the **Distribution Layer (Argus ACLI)**.

It MUST NOT:

- modify system tools
- modify Argus diagnostic logic
- bypass the control plane
- introduce new execution paths

It ONLY transforms how results are presented to the user.

---

## Current State

Argus tools return structured output:

```
{
  "status": "success",
  "tool": "<name>",
  "message": "...",
  "data": {
    "severity": "...",
    "findings": [...],
    "recommendations": [...]
  }
}
```

This is correct but not optimized for CLI usability.

---

## Problem

Current CLI output:

- feels like structured data, not a tool
- lacks visual hierarchy
- mixes raw and interpreted data
- is harder to scan quickly

---

## Design Goals

### 1. Readability

Output must be:

- easy to scan
- clearly segmented
- visually structured

---

### 2. Severity Awareness

Severity must be:

- immediately visible
- consistently formatted

Example:

[OK]  
[INFO]  
[WARN]  
[CRITICAL]

---

### 3. Structured Sections

Each output should follow:

1. Title / Summary
2. Severity
3. Findings
4. Recommendations

---

### 4. Consistency

All Argus outputs must:

- follow the same structure
- use the same formatting rules
- feel like a unified tool

---

### 5. No Data Loss

All structured data must still exist.

This layer:

- formats
- does NOT remove or alter data

---

## Proposed Output Format

Example:

```
=== Disk Analysis ===

Severity: WARN

Findings:
- High disk usage on /mnt/c (77%)

Recommendations:
- Investigate disk usage
- Free up space
```

---

## Implementation Approach

### Option A – CLI Formatting Layer (Preferred)

Modify:

scripts/ai_cli.py

Responsibilities:

- detect Argus output
- format for display
- preserve raw JSON if needed

---

### Option B – Argus Presentation Wrapper (Alternative)

Introduce formatting layer inside Argus tools.

NOT preferred because:

- mixes logic and presentation
- breaks separation of concerns

---

## Decision

Use:

→ CLI Formatting Layer

---

## Key Constraints

- MUST preserve control plane execution flow
- MUST NOT modify tool output contract
- MUST NOT parse `message` field for logic
- MUST rely on structured `data` field

---

## Future Extensions

- colorized output
- table formatting
- interactive CLI
- filtering options (e.g. show only WARN/CRITICAL)

---

## Summary

This phase converts:

structured diagnostic output  
→ into  
usable system interface

No new intelligence is added.

Only clarity.

---

## End State

A user can run:

```
ai "disk"
```

And instantly understand:

- system health
- problems
- what to do next

Without interpreting raw output.