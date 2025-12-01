# Project Definition Templates

Templates for collaborative AI-assisted development. Works for software, hardware, or hybrid projects. Human describes the problem, AI fills out templates and asks clarifying questions, human reviews, AI implements.

## Documents

| Document | Purpose |
|----------|---------|
| [01_concept.md](01_concept.md) | WHAT and WHY - problem, requirements, scope, prior art |
| [02_implementation.md](02_implementation.md) | HOW - architecture, technology/material choices, failure modes |
| [03_design_map.md](03_design_map.md) | SPECIFIC structure - files, parts, functions, dependencies |

## Process

1. AI fills out concept doc, human reviews
2. AI fills out implementation doc, human reviews
3. AI fills out design map, human reviews
4. AI implements, validates (software: `make dev`; hardware: build and test)

See [PLAYBOOK.md](PLAYBOOK.md) for guidance and common pitfalls.

## Project Setup (Python)

| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | AI coding guidelines |
| [pyproject.template.toml](pyproject.template.toml) | Poetry config with ruff/pyright |
| [Makefile.template](Makefile.template) | Build commands |

```bash
make fix    # Auto-format
make dev    # Lint, typecheck, test
```
