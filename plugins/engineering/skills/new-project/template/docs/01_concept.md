# Concept of Operations

## Problem Statement

What specific problem are we solving? Be concrete - avoid vague statements.

> **Guidance**: A good problem statement can be verified. "Development is slow" is vague. "Deploying code to my robot requires 4 manual steps" is testable. "Seeding trays by hand takes 20 minutes each" is concrete.

## Users

Who uses this? What are they trying to accomplish?

## Operational Context

How does this fit into the user's broader workflow? What happens before and after?

> **Guidance**: Understanding the full context prevents building isolated solutions. What triggers use of this system? What does the user do with the output? For hardware: what environment does it operate in?

## Requirements

What must the system do, and how do we verify it works?

| Requirement | How to Verify |
|-------------|---------------|
|             |               |

> **Guidance**: Keep this minimal. Resist scope creep - if a requirement isn't directly tied to the problem statement, question whether it belongs. Avoid invented metrics like "50% faster" unless you'll actually measure them. "I can deploy in one command" or "seeds are evenly distributed" is more honest than percentage claims.

## Critical Specifications

Quantitative values that constrain the solution. Include units and tolerances where applicable.

| Specification | Value | Rationale |
|---------------|-------|-----------|
|               |       |           |

> **Guidance**: For software - API rate limits, latency requirements, payload sizes, compatibility requirements. For hardware - dimensions, tolerances, forces, speeds, environmental limits, material constraints. Skip if there are no hard numeric constraints.

## Scope

**In Scope:**
-

**Out of Scope:**
-

> **Guidance**: Out of scope is as important as in scope. Be explicit about what you're NOT building to prevent feature creep.

## Constraints

What limits the solution? Only include constraints that actually affect design decisions.

-

> **Guidance**: Budget, timeline, existing systems to integrate with, regulatory requirements, manufacturing capabilities, available tools/skills.

## Prior Art

Existing solutions - commercial products, open source projects, or previous attempts.

| Solution | What Works | What Doesn't | Key Insight |
|----------|------------|--------------|-------------|
|          |            |              |             |

> **Guidance**: Skip if truly greenfield. Otherwise, 10 minutes of research here saves hours of reinventing. Include links where useful. Note what you'd steal vs. improve.
