# LLM Project Definition Playbook

## Purpose

Guide for defining projects for LLM implementation. Works for software, hardware, or hybrid projects. The goal: specifications clear enough that an LLM can build working systems without constant clarification.

## For LLMs Using This Template

- This is a process guide - understand the document relationships, don't copy structure literally
- Keep outputs simple. Resist adding abstractions, flexibility, or "future-proofing"
- Scale detail to project size: a small tool needs 2-3 requirements, not 10
- When filling templates, ask clarifying questions rather than making assumptions
- Sections marked "skip if not applicable" should be omitted entirely, not filled with "N/A"

## The Three Documents

| Document | Defines | Key Question |
|----------|---------|--------------|
| **01_concept.md** | WHAT and WHY | What problem are we solving? |
| **02_implementation.md** | HOW | What's the architecture? |
| **03_design_map.md** | SPECIFIC structure | What files/parts/functions exist? |

```
[Problem] → [Concept] → [Implementation] → [Design Map] → [Working System]
              WHAT          HOW              WHERE
```

Each document builds on the previous. Don't skip ahead.

## Document 1: Concept of Operations

Define the problem and requirements without specifying solutions.

**Good problem statement:**
> "Deploying code to my robot requires 4 manual steps: ssh, scp, ssh again, run command"
> "Seeding microgreens trays by hand takes 20 minutes per tray and causes repetitive strain"

**Bad problem statement:**
> "Development workflow is inefficient" (vague, unmeasurable)

**Key sections:**
- Problem (concrete, verifiable)
- Users (who and what they need)
- Operational Context (what happens before/after)
- Requirements (minimal, with verification method)
- Critical Specifications (hard numbers: dimensions, rates, limits)
- Scope (what's in AND out)
- Prior Art (existing solutions, what to learn from them)

> **Guidance**: If you can't explain why a requirement exists, cut it.

## Document 2: Implementation Plan

Define architecture and technical approach. This is where you make technology and material choices.

**Key sections:**
- Architecture (components and how they connect)
- Technology/material choices (and why, with alternatives considered)
- Data/material flow (inputs → transformations → outputs)
- Key decisions (document the hard-to-reverse choices)
- Failure modes (what could break, how to mitigate)
- Phased approach (MVP first, extras later)
- Bill of materials (hardware projects)
- Open design tasks (unresolved items)

**Example architecture (software):**
```
[CLI] → [Config Loader] → [SSH Manager] → [Remote Host]
                              ↓
                       [File Transfer]
```

**Example architecture (hardware):**
```
[Hopper] → [Feed Drum] → [Brush] → [Tray]
              ↑
         [CVT Drive]
```

> **Guidance**: Resist the urge to design everything upfront. Define the MVP path first.

## Document 3: Design Map

The blueprint for implementation. This document must stand alone - the implementing LLM or fabricator may not see the other documents.

**Key sections:**
- Project structure (directories/files or assembly hierarchy)
- Modules/assemblies (purpose, key functions/features)
- Dependencies (external libraries or purchased components)
- Example interactions (concrete usage examples)
- Error handling / failure recovery

**Example module spec (software):**
```
### Module: ssh_manager

**Purpose:** Handle SSH connections and remote command execution

**Files:**
- `ssh_manager.py` - connection handling, command execution

**Key Functions:**
connect(host, key_path) -> Connection
execute(connection, command) -> Result
transfer(connection, local_path, remote_path) -> None
```

**Example assembly spec (hardware):**
```
### Assembly: Feed Drum

**Purpose:** Meter seeds from hopper onto tray at controlled rate

**Parts:**
- `drum_body.stl` - main cylinder with seed pockets
- `drum_cap_l.stl` / `drum_cap_r.stl` - end caps with bearing seats

**Key Features:**
- Pocket pattern: 5mm diameter, 3mm deep, 8mm pitch
- Bearing interface: 608ZZ press fit
- Drive interface: O-ring groove for belt drive
```

> **Guidance**: Specify interfaces, not implementations. Let the LLM/fabricator figure out the internals.

## Process

1. Fill out concept doc, review it yourself
2. Fill out implementation doc, review
3. Fill out design map, review
4. Implement (software: LLM runs `make dev` to validate; hardware: build and test)

At each step, ask: "Is this the simplest thing that solves the problem?"

## Common Pitfalls

**Over-engineering**: LLMs will add abstractions, factories, and flexibility you didn't ask for. Be explicit about keeping things simple.

**Invented metrics**: "50% faster" or "95% success rate" are meaningless unless you'll measure them. Use concrete verifications instead: "I can deploy in one command" or "seeds land in the tray, not on the floor."

**Scope creep**: Every requirement should trace back to the problem statement. If it doesn't, cut it.

**Under-specification**: Vague requirements invite LLM assumptions. Be specific about what you want.

**Skipping documents**: Don't jump to design map before understanding the architecture. Don't architect before understanding the problem.

**Ignoring prior art**: Existing solutions reveal what works. 10 minutes of research saves hours of reinventing.

## Troubleshooting

| Problem | Symptom | Fix |
|---------|---------|-----|
| Vague requirements | Questions keep coming up during implementation | Add concrete acceptance criteria |
| Over-engineered architecture | Complex design for simple problem | Strip back to MVP, add complexity only when needed |
| Incomplete design map | LLM asks clarifying questions while coding | Add missing function signatures and behaviors |
| Scope creep | Requirements growing mid-project | Revisit problem statement, cut what doesn't trace back |
| Technology assumptions in concept | ConOps mentions specific tools/frameworks | Remove implementation details, focus on what not how |
| Missing specifications | Design decisions made without data | Add critical specs with real numbers and sources |
