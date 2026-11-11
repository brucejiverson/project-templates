# Implementation Plan

## Architecture Overview

What are the main components? How do they connect?

```
[Component A] → [Component B] → [Component C]
```

> **Guidance**: For software - show data/control flow between modules. For hardware - show mechanical/electrical connections between subsystems. For hybrid - show both.

## Components

| Component | Responsibility | Interfaces | Notes |
|-----------|----------------|------------|-------|
|           |                |            |       |

> **Guidance**: For software - modules, services, libraries. For hardware - subsystems, assemblies, mechanisms. Interface = how components connect (API, shaft coupling, signal wire, fastener pattern).

## Technology & Material Choices

What tools, languages, frameworks, materials, or manufacturing methods will be used? Why?

| Choice | Alternatives Considered | Why This One |
|--------|------------------------|--------------|
|        |                        |              |

> **Guidance**: Document the reasoning. "304 stainless because it resists hydrogen peroxide" or "Python because team knows it" - both valid if explicit.

## External Dependencies

List third-party services, APIs, libraries, or purchased components the system relies on.

| Dependency | Purpose | Source | Notes |
|------------|---------|--------|-------|
|            |         |        |       |

> **Guidance**: Note lead times, single-source risks, licensing terms, or version constraints.

## Data / Material Flow

How does information or material move through the system?

```
[Input] → [Process] → [Output]
```

> **Guidance**: For software - data transformations. For hardware - material path, force transmission, signal flow.

## Key Decisions

Document significant design choices beyond technology/materials.

| Decision | Chosen Approach | Alternatives | Rationale |
|----------|-----------------|--------------|-----------|
|          |                 |              |           |

> **Guidance**: Focus on decisions that would be hard to reverse. "Why this architecture?" not "why this variable name?"

## Failure Modes

What could go wrong? Focus on likely and high-impact failures.

| Component | Failure Mode | Consequence | Mitigation |
|-----------|--------------|-------------|------------|
|           |              |             |            |

> **Guidance**: Not exhaustive FMEA - just the obvious risks worth addressing in design. Software: crashes, data loss, security issues. Hardware: wear, misalignment, jamming, user error.

## Phased Approach

Break implementation into incremental phases.

**Phase 1 (MVP):** Core functionality to validate the concept.

**Future Phases:** Additional capabilities to add after MVP is validated.

> **Guidance**: Resist the urge to design everything upfront. Define the MVP path first. What's the minimum to prove this works?

## Verification

How do we verify components work correctly and together?

| What to Verify | Test Approach |
|----------------|---------------|
|                |               |

> **Guidance**: For software - unit tests, integration tests. For hardware - fit checks, functional tests, load tests. Be specific enough to actually do them.

## Bill of Materials

| Component | Qty | Est. Cost | Source | Lead Time |
|-----------|-----|-----------|--------|-----------|
|           |     |           |        |           |

**Estimated Total:** $___

> **Guidance**: Skip for pure software. For hardware: flag single-source dependencies and long-lead items. Note volume pricing if scaling is in scope.

## Open Design Tasks

Unresolved decisions and incomplete work.

- [ ] Description of open item

> **Guidance**: Working backlog. Update as design progresses. These become implementation tasks once resolved.
