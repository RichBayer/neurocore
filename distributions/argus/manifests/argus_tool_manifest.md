# Argus V1 – Tool Manifest

---

# Purpose

This document defines the executable tool layer for Argus V1.

It maps:

- tool names → system commands
- tool types → core vs optional
- dependencies → required binaries
- behavior → execution + fallback rules

---

# Tool Execution Model

All tools must:

1. Execute through the execution engine
2. Be registered in the tool registry
3. Return structured output (no raw dumps)
4. Respect read-only constraints
5. Support graceful failure if dependencies are missing

---

# Tool Metadata Standard

Each tool should define:

- name
- category
- command
- arguments
- required_binary
- dependency_package (if applicable)
- tier (core / optional)
- description
- failure_mode

---

# Tier 1 — Core Tools

---

## system_summary

- category: system
- commands:
  - uptime
  - free -h
  - df -h
  - cat /etc/os-release
- required_binary: coreutils
- tier: core

---

## process_top

- category: system
- commands:
  - ps aux --sort=-%cpu | head
  - ps aux --sort=-%mem | head
- required_binary: ps
- tier: core

---

## disk_layout

- category: system
- commands:
  - lsblk
- required_binary: lsblk
- tier: core

---

## service_status

- category: service
- commands:
  - systemctl status <service>
- required_binary: systemctl
- tier: core

---

## service_list

- category: service
- commands:
  - systemctl list-units --type=service --state=running
  - systemctl list-units --type=service --state=failed
- required_binary: systemctl
- tier: core

---

## log_recent_errors

- category: logs
- commands:
  - journalctl -p err -n 50
- required_binary: journalctl
- tier: core

---

## log_service

- category: logs
- commands:
  - journalctl -u <service> -n 100
- required_binary: journalctl
- tier: core

---

## kernel_log_check

- category: logs
- commands:
  - dmesg | tail
- required_binary: dmesg
- tier: core

---

## disk_usage

- category: disk
- commands:
  - df -h
- required_binary: df
- tier: core

---

## disk_usage_breakdown

- category: disk
- commands:
  - du -sh /var/* 2>/dev/null | sort -hr | head
- required_binary: du
- tier: core

---

## memory_usage

- category: system
- commands:
  - free -h
- required_binary: free
- tier: core

---

## network_interfaces

- category: network
- commands:
  - ip a
- required_binary: ip
- tier: core

---

## routing_check

- category: network
- commands:
  - ip route
- required_binary: ip
- tier: core

---

## listening_ports

- category: network
- commands:
  - ss -tuln
- required_binary: ss
- tier: core

---

## network_connectivity

- category: network
- commands:
  - ping -c 3 8.8.8.8
- required_binary: ping
- tier: core

---

## dns_check

- category: network
- commands:
  - nslookup google.com
- required_binary: nslookup
- tier: core

---

## auth_log_scan

- category: security
- commands:
  - journalctl -u ssh | grep "Failed password"
- required_binary: journalctl
- tier: core

---

## sudo_activity_check

- category: security
- commands:
  - journalctl | grep sudo
- required_binary: journalctl
- tier: core

---

## find_file

- category: file
- commands:
  - find <path> -name "*pattern*"
- required_binary: find
- tier: core

---

## find_by_content

- category: file
- commands:
  - grep -R "pattern" <path>
- required_binary: grep
- tier: core

---

## read_file_safe

- category: file
- commands:
  - cat <file>
- required_binary: cat
- tier: core

---

## whereis_binary

- category: file
- commands:
  - whereis <binary>
- required_binary: whereis
- tier: core

---

# Tier 2 — Optional Tools

---

## io_stats

- category: performance
- commands:
  - iostat -x
- required_binary: iostat
- dependency_package: sysstat
- tier: optional

---

## memory_pressure_detail

- category: performance
- commands:
  - vmstat
- required_binary: vmstat
- tier: optional

---

## fast_file_lookup

- category: file
- commands:
  - locate <file>
- required_binary: locate
- dependency_package: mlocate or plocate
- tier: optional

---

## dns_deep_check

- category: network
- commands:
  - dig google.com
- required_binary: dig
- dependency_package: dnsutils
- tier: optional

---

## open_files_for_process

- category: system
- commands:
  - lsof
- required_binary: lsof
- tier: optional

---

## disk_health_smart

- category: hardware
- commands:
  - smartctl -H /dev/sdX
- required_binary: smartctl
- dependency_package: smartmontools
- tier: optional

---

# Failure Handling Standard

If required_binary is missing, return:

- status: unavailable
- reason: missing dependency
- package: suggested install package
- impact: what analysis cannot be performed

---

# Final Rule

Tools must provide:

- structured output
- no direct system modification
- safe execution
- predictable behavior

Argus must never expose raw command output without interpretation.