# Argus Tool Creation Workflow

---

## Purpose

This document defines the correct process for creating new Argus tools.

This exists to prevent:

- broken execution paths  
- daemon startup failures  
- missing tool registration  
- inconsistent behavior across tools  

This workflow must be followed every time a new Argus tool is introduced.

---

## Core Principle

An Argus tool is **not a script**.

It is a component in a controlled execution pipeline:

```
CLI → Daemon → Runtime Manager → Control Plane → Execution Engine → Argus Tool → System Tool → OS
```

If any part of that chain is incomplete, the tool will fail.

---

## Tool Layers (Reminder)

### System Tools

- Collect raw system data  
- Call `CommandRunner`  
- Do not interpret  
- Do not aggregate  

---

### Argus Tools

- Consume system tool data  
- Interpret signals  
- Aggregate findings  
- Produce structured diagnostics  

---

## Required Steps (Do Not Skip)

---

### 1. Create the Argus Tool File

Location:

```
tools/argus/
```

Example:

```
tools/argus/system_analysis.py
```

---

### 2. Implement BaseTool Contract

All Argus tools must:

- inherit from `BaseTool`
- define:
  - `name`
  - `description`
  - `execution_mode`
  - `input_schema`

---

### 3. Use System Tools Only

Argus tools:

- MUST NOT call `CommandRunner`
- MUST use system tools via registry

Correct:

```
system_tool = registry.get("disk_usage")
result = system_tool.execute(...)
```

---

### 4. Enforce Output Contract

All Argus tools must return:

```
{
  "status": "...",
  "message": "...",
  "data": {
    "severity": "...",
    "findings": [...],
    "recommendations": [...],
    "raw": ...
  }
}
```

---

### 5. Preserve Raw Evidence

Every tool must include:

- raw system output  
- unmodified  

This is required for:

- trust  
- verification  
- future model reasoning  

---

### 6. Register the Tool

File:

```
tools/__init__.py
```

Add:

```
from tools.argus.new_tool import NewTool
```

and:

```
registry.register(NewTool())
```

---

### 7. Update Control Plane Keywords

File:

```
runtime/control_plane.py
```

Ensure the tool can be triggered.

Example:

```
"disk", "memory", "network", "processes", "system"
```

Add new keyword if needed.

---

### 8. Restart Daemon

Required after ANY tool change.

```
python -m runtime.neurocore_daemon
```

---

### 9. Validate Execution Path

Test:

```
ai "your_command"
```

Confirm:

- tool is routed correctly  
- no errors  
- output returns  

---

### 10. Validate Output Contract

Check:

- severity present  
- findings present  
- recommendations present  
- raw present  

No missing sections.

---

### 11. Capture Screenshots (Real-Time)

During build:

- capture before/after behavior  
- name screenshots immediately  
- store in correct feature directory  

Do NOT assume output.

---

### 12. Integrate Into System Analysis (If Applicable)

If the tool is a core signal:

- add it to `system_analysis`
- merge findings and recommendations

---

## Common Failure Modes

---

### Tool Imported Before Created

Result:

```
ModuleNotFoundError
```

Cause:

- referenced in `__init__.py` before file exists

---

### Tool Not Registered

Result:

```
Tool not found
```

Cause:

- missing `registry.register()`

---

### Control Plane Not Updated

Result:

- command not routed

Cause:

- keyword missing

---

### Missing Raw Output

Result:

- incomplete diagnostics

Cause:

- not passing through system tool data

---

### Broken Data Shape

Result:

- empty or incorrect output

Cause:

- mismatch between system tool and Argus expectations

---

## Build Discipline Rules

- Never assume output  
- Never pre-name screenshots  
- Validate every step before moving forward  
- Use real system data only  
- Follow full execution path  

---

## Final Note

Creating a tool is not just writing code.

It is integrating into a system with:

- strict execution boundaries  
- enforced data contracts  
- controlled flow through the control plane  

Skipping steps will break the system.

Following this workflow keeps everything stable and predictable.