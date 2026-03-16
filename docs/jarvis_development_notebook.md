# Jarvis Development Notebook

This document acts as a **working notebook for ideas discovered while building Jarvis**.

Unlike the Vision, Architecture, and Build Log documents, the notes here are intentionally informal.

Purpose of this document:

- capture interesting ideas during development
- record experiments worth exploring later
- keep track of small improvements discovered while working on the system

Items listed here are **not committed design decisions**.

If an idea proves useful, it may later be moved into:

- the Architecture document
- a Build Log
- or an implementation task

---

# CLI Interaction Experiments

While developing Jarvis, the `ai` command-line helper has proven useful for interacting with the local AI system directly from the terminal.

Current examples that already work well:

```
journalctl -xe | ai
dmesg | ai
ai /etc/fstab
```

Possible areas to explore:

- making log analysis easier
- simplifying troubleshooting workflows
- reducing typing when sending command output to Jarvis
- improving readability of AI responses for terminal use
- creating helper commands for common diagnostic tasks

Goal: make Jarvis feel like a **natural extension of the Linux command line**.

---

# Multi-Model Routing Experiments

Currently Jarvis runs a single model.

Future experiments may explore selecting different models depending on the task.

Possible directions:

- general reasoning model for normal questions
- coding-focused model for scripts and debugging
- lightweight model for fast responses
- larger reasoning models for complex analysis

Conceptual flow:

```
user request
↓
logic router
↓
model selection
↓
response
```

This would allow Jarvis to evolve into a **multi-model system without requiring the user to manually choose models**.

---

# System Log Awareness

While troubleshooting Linux systems, piping logs into Jarvis has been useful.

Example:

```
journalctl -xe | ai
```

Future experiments could explore making Jarvis more aware of system state.

Possible directions:

- detecting important system events automatically
- forwarding interesting log entries to Jarvis for interpretation
- summarizing errors in plain language
- assisting with troubleshooting infrastructure issues

Conceptual idea:

```
system logs
↓
event filter
↓
Jarvis analysis
↓
notification or explanation
```

This could eventually evolve into a **system diagnostic assistant for homelab environments**.