# NeuroCore Home AI Hardware System

---

# Overview

This document defines the physical hardware architecture of the NeuroCore system.

It translates the system vision into:

- concrete hardware components  
- node design patterns  
- installation strategy  
- scalable deployment model  

The goal is to ensure:

- no wasted purchases  
- consistent architecture across all rooms  
- clean, professional installation  
- long-term scalability  

---

# Design Principles

## Local-First Operation

All hardware must support:

- local communication  
- local processing  
- no cloud dependency requirements  

---

## Modular Node Architecture

The system is built from repeatable room-based nodes.

Each node operates independently but connects to the central NeuroCore runtime.

---

## Clean Integration

Hardware must:

- blend into the home environment  
- minimize visible wiring  
- avoid lab-style appearance  

---

## Serviceability

All installations must allow:

- hardware replacement  
- upgrades  
- maintenance access  

---

## Scalability

The system must support:

- incremental expansion  
- room-by-room deployment  
- additional sensor integration  

---

# System Architecture (Hardware)

## Core Layers

Perception Layer   → Cameras, Microphones  
Interaction Layer  → Speakers, Tablets  
Edge Layer         → Room Nodes (lightweight compute)  
Core Layer         → Legion PC + Closet Server  

---

# Core Systems

## Primary AI Compute

Host System: Lenovo Legion Desktop  
CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  

Role:

- LLM inference (Ollama)  
- reasoning layer  
- advanced AI processing  

---

## Infrastructure Server (Closet)

Model: Dell PowerEdge R730  

Role:

- Proxmox hypervisor  
- Linux homelab environment  
- Home Assistant  
- camera/NVR system  
- automation services  
- databases and logging  

---

## Power Protection

Model: CyberPower CP1500PFCLCD  

Role:

- safe shutdown during outages  
- hardware protection  
- system stability  

---

## Rack System

Model: Rosewill 12U Wall Mount Rack  

Role:

- structured hardware mounting  
- cable organization  
- centralized infrastructure  

---

# Network Core

## Router

Model: Ubiquiti UniFi Dream Machine SE (UDM-SE)  

Role:

- routing and firewall  
- network controller (UniFi OS)  
- central network management  

---

## Core Switch

Model: Ubiquiti USW-24-PoE  

Role:

- primary network distribution  
- PoE for cameras and future devices  
- scalable port expansion  

---

## Patch Panel

Model: TRENDnet 24-Port Cat6 Patch Panel  

Role:

- structured cable termination  
- clean cable management  
- simplified troubleshooting  
- professional installation standard  

---

## Network Structure

Internet  
→ UDM-SE (router/controller)  
→ USW-24-PoE (switch)  
→ Patch Panel  
→ Room Nodes / Cameras / Server  

---

# Room Node Architecture (Edge Nodes)

Each room contains a NeuroCore interaction node.

---

## Mini PC

Model: Beelink Mini S12 Pro (Intel N100)  

Role:

- audio interface processing  
- communication with NeuroCore core  
- local interaction handling  

---

## Microphone

Model: ReSpeaker XVF3800 USB Mic Array  

Role:

- far-field voice capture  
- multi-directional input  

---

## Speakers

Model: Kanto YU2 Powered Speakers  

Role:

- voice output  
- music playback  
- alert delivery  

---

## Tablet Interface

Model: Samsung Galaxy Tab A9+  
Mount: VidaMount Recessed Tablet Mount  

Role:

- avatar interface  
- visual feedback  
- system interaction  
- camera display  

---

## Node Wiring

Microphone → USB → Mini PC  
Speakers → 3.5mm → Mini PC  
Tablet → WiFi + charging mount  
Mini PC → Ethernet (preferred) or WiFi  

---

# Camera System

## Outdoor Camera

Model: Reolink TrackMix PoE  

Role:

- motion tracking  
- perimeter monitoring  
- night vision (IR)  
- security coverage  

---

## Indoor Camera

Model: Ubiquiti G3 Instant  

Role:

- identity recognition  
- presence detection  
- indoor monitoring  

---

# Installation Layout (Room Node)

Camera (elevated, discreet placement)  

Tablet (flush-mounted at eye level)  

Shelf:
- Speaker (left)  
- Microphone  
- Speaker (right)  

In-wall or nearby:
- Mini PC  
- power and wiring  

---

# System Roles

## Legion PC

- AI compute  
- reasoning  
- model execution  

---

## Closet Server

- infrastructure services  
- automation  
- camera system  
- homelab VMs  

---

## Room Nodes

- user interaction  
- voice input/output  
- visual interface  

---

# Buying Strategy

## Phase 1 — Single Node Test Build

Purchase:

- Beelink Mini S12 Pro  
- ReSpeaker XVF3800 Mic Array  
- Kanto YU2 Speakers  
- Samsung Galaxy Tab A9+  
- VidaMount Recessed Tablet Mount  
- ONE camera (Reolink TrackMix PoE or Ubiquiti G3 Instant)  

Goal:

- validate voice interaction  
- validate audio output  
- integrate with NeuroCore  
- test camera ingestion  

---

## Phase 2 — Closet Infrastructure

Purchase:

- Dell PowerEdge R730  
- CyberPower CP1500PFCLCD UPS  
- Rosewill 12U Wall Mount Rack  
- Ubiquiti UniFi Dream Machine SE  
- Ubiquiti USW-24-PoE Switch  

Goal:

- deploy Proxmox  
- move infrastructure services off Legion  
- establish stable network backbone  

---

## Phase 3 — Structured Cabling

Purchase:

- TRENDnet 24-Port Cat6 Patch Panel  

Goal:

- clean cable management  
- scalable infrastructure  
- professional installation  

---

## Phase 4 — Expansion

- additional room nodes  
- additional cameras  
- automation devices  

---

# Summary

This hardware architecture provides:

- centralized AI processing  
- distributed interaction nodes  
- enterprise-style homelab capability  
- scalable home infrastructure  

---

NeuroCore hardware is designed to be:

modular, reliable, efficient, and built for long-term expansion