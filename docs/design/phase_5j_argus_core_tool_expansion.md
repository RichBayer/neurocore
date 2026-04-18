# Phase 5J – Argus Core Tool Expansion

## What We’re Actually Doing

Right now I am NOT building Argus.

I am expanding NeuroCore so that Argus can exist later.

This phase is about adding real, safe system tools that can:

- gather system data
- run real commands
- return structured output

All under full control of the control plane.

---

## Why This Matters

Argus is going to be a system intelligence layer.

But it can’t exist without data.

So before Argus can explain anything, NeuroCore has to be able to:

- inspect the system
- gather logs
- check services
- look at resources
- return that data in a structured way

That’s what this phase is.

We are building the foundation Argus will stand on.

---

## What We ARE Doing

- Adding real system tools (read-only)
- Running them through CommandRunner
- Keeping everything inside the execution engine
- Making sure the control plane governs everything
- Returning clean structured output

---

## What We are NOT Doing

- Not building Argus behavior
- Not building explanations
- Not building intelligence
- Not building training features
- Not building evaluation systems

Those come later.

---

## How This Fits the System

NeuroCore:
- gaining more capability (tools)

Argus:
- will use these tools later

Homelab:
- not part of this phase

---

## Architecture Impact

Nothing new is being invented here.

We are just expanding this path:

control_plane → execution_engine → tool → command_runner → OS

We are adding more tools to this system.

That’s it.

---

## Rules I Cannot Break

- ALL execution goes through control plane
- ALL tools must be read-only
- NO direct subprocess calls outside CommandRunner
- NO bypassing execution engine
- NO shortcuts that break architecture later

---

## What Success Looks Like

When this phase is done:

- I can run multiple real tools safely
- everything is observable
- output is structured and usable later
- nothing breaks the architecture

---

## Bottom Line

This phase is not about intelligence.

It’s about capability.

I’m building the system that Argus will use later.