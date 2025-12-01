# LLM Project Definition Playbook

## Purpose

Guide for defining software projects for LLM implementation. The goal: specifications clear enough that an LLM can build working software without constant clarification.

## For LLMs Using This Template

- This is a process guide - understand the document relationships, don't copy structure literally
- Keep outputs simple. Resist adding abstractions, flexibility, or "future-proofing"
- Scale detail to project size: a small tool needs 2-3 requirements, not 10
- When filling templates, ask clarifying questions rather than making assumptions

## The Three Documents

| Document | Defines | Key Question |
|----------|---------|--------------|
| **01_concept.md** | WHAT and WHY | What problem are we solving? |
| **02_implementation.md** | HOW | What's the architecture? |
| **03_code_map.md** | SPECIFIC structure | What files/functions exist? |

```
[Problem] → [Concept] → [Implementation] → [Code Map] → [Working Code]
              WHAT          HOW             WHERE
```

Each document builds on the previous. Don't skip ahead.

## Document 1: Concept of Operations

Define the problem and requirements without specifying solutions.

**Good problem statement:**
> "Deploying code to my robot requires 4 manual steps: ssh, scp, ssh again, run command"

**Bad problem statement:**
> "Development workflow is inefficient" (vague, unmeasurable)

**Key sections:**
- Problem (concrete, verifiable)
- Users (who and what they need)
- Requirements (minimal, with verification method)
- Scope (what's in AND out)

> **Guidance**: If you can't explain why a requirement exists, cut it.

## Document 2: Implementation Plan

Define architecture and technical approach. This is where you make technology choices.

**Key sections:**
- Architecture (components and how they connect)
- Technology choices (and why)
- Data flow (inputs → transformations → outputs)
- Phased approach (MVP first, extras later)
- Risks (what could break)

**Example architecture:**
```
[CLI] → [Config Loader] → [SSH Manager] → [Remote Host]
                              ↓
                       [File Transfer]
```

> **Guidance**: Resist the urge to design everything upfront. Define the MVP path first.

## Document 3: Code Map

The blueprint for implementation. This document must stand alone - the implementing LLM won't see the other documents.

**Key sections:**
- Project structure (directories and files)
- Modules (purpose, key functions)
- Dependencies (external libraries)
- Error handling approach

**Example module spec:**
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

> **Guidance**: Specify interfaces, not implementations. Let the LLM figure out the internals.

## Process

1. Fill out concept doc, review it yourself
2. Fill out implementation doc, review
3. Fill out code map, review
4. Implement (LLM runs `make dev` to validate)

At each step, ask: "Is this the simplest thing that solves the problem?"

## Common Pitfalls

**Over-engineering**: LLMs will add abstractions, factories, and flexibility you didn't ask for. Be explicit about keeping things simple.

**Invented metrics**: "50% faster" or "95% success rate" are meaningless unless you'll measure them. Use concrete verifications instead: "I can deploy in one command."

**Scope creep**: Every requirement should trace back to the problem statement. If it doesn't, cut it.

**Under-specification**: Vague requirements invite LLM assumptions. Be specific about what you want.

**Skipping documents**: Don't jump to code map before understanding the architecture. Don't architect before understanding the problem.

## Troubleshooting

| Problem | Symptom | Fix |
|---------|---------|-----|
| Vague requirements | Questions keep coming up during implementation | Add concrete acceptance criteria |
| Over-engineered architecture | Complex design for simple problem | Strip back to MVP, add complexity only when needed |
| Incomplete code map | LLM asks clarifying questions while coding | Add missing function signatures and behaviors |
| Scope creep | Requirements growing mid-project | Revisit problem statement, cut what doesn't trace back |
| Technology assumptions in concept | ConOps mentions specific tools/frameworks | Remove implementation details, focus on what not how |
