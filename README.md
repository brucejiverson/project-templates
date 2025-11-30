# Project Definition Templates

Templates for collaborative AI-assisted software development. The process is designed to be AI-led: the AI guides the human through requirements gathering, proposes architecture, and drives implementation while the human provides domain knowledge and approval at key checkpoints.

## How It Works

1. **Human** describes the problem or goal
2. **AI** fills out templates, asks clarifying questions
3. **Human** reviews and approves each phase before proceeding
4. **AI** implements based on approved specifications

## Documentation Templates

| Document | Purpose | Creates |
|----------|---------|---------|
| [01_concept.md](01_concept.md) | WHAT and WHY | Requirements + Acceptance Tests |
| [02_implementation.md](02_implementation.md) | HOW | Architecture + Integration Tests |
| [03_code_map.md](03_code_map.md) | SPECIFIC structure | Code Blueprint + Unit Tests |

## Project Setup Templates (Python)

| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | AI coding guidelines |
| [pyproject.template.toml](pyproject.template.toml) | Poetry config with ruff/pyright |
| [Makefile.template](Makefile.template) | Build commands (dev, fix, test) |

## Process

1. AI fills out 01_concept.md, human reviews
2. AI fills out 02_implementation.md, human reviews
3. AI fills out 03_code_map.md, human reviews
4. AI implements, running `make dev` to validate

## V-Model Alignment

```
Requirements (01) ──────────────► Acceptance Tests
        ↘                              ↗
    Architecture (02) ────► Integration Tests
            ↘                    ↗
        Code Map (03) ──► Unit Tests
                ↘        ↗
              IMPLEMENTATION
```

## Workflow

```bash
make fix    # Auto-format
make dev    # Lint, typecheck, test
```

## Detailed Guidance

See [PLAYBOOK.md](PLAYBOOK.md) for comprehensive process documentation, examples, and checklists.
