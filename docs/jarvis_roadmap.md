# jarvis roadmap

Notes for ideas and improvements discovered while building Jarvis.

The architecture docs describe the planned system design.
Build logs record what has already been implemented.

This file is just for ideas to explore later.

---

## cli improvements

Keep improving the `ai` helper so it works well as a normal command-line tool.

Right now it can handle prompts, pipes, and files. There may be ways to make this smoother for everyday Linux use.

Ideas:

- make log analysis easier
- simplify troubleshooting workflows
- reduce typing when sending command output to Jarvis

Examples that already work:

journalctl -xe | ai  
dmesg | ai  
ai /etc/fstab

---

## model routing

Experiment with automatically selecting the best model depending on the task.

The idea is that the user just talks to Jarvis and the system decides which model to use.

Possible direction:

- general reasoning model for normal questions
- coding model for scripts and troubleshooting
- other specialized models later if needed

Concept:

user request → router → selected model → response

---

## system awareness

Experiment with automated log monitoring where system events are forwarded to Jarvis for analysis.

Instead of always sending logs manually, the system could detect important events and ask Jarvis to interpret them.

Possible uses:

- summarize system errors
- explain unusual behavior
- assist with troubleshooting infrastructure issues

Concept:

system logs → event filter → Jarvis analysis → notification

Manual version that already works:

journalctl -xe | ai