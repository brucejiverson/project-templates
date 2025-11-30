# CLAUDE.md - AI Coding Guidelines

## Build/Test Commands

```bash
# Full validation (lint, typecheck, test)
make dev

# Single test
poetry run pytest -k test_name

# Auto-fix formatting
make fix
```

## Code Style

- **Linting**: Ruff with rules: E, W, F, I, C, B, N, A, RET, FURB, RUF, ASYNC
- **Type Checking**: Pyright strict mode
- **Dependencies**: Poetry
- **Imports**: Sort with ruff (stdlib / third-party / local)
- **Naming**: snake_case, descriptive names, avoid abbreviations
- **Error Handling**: Explicit error checks, structured logging

## Testing

- Coverage required
- Use `make dev` before committing
- Mark hardware/integration tests appropriately

## Workflow

1. Run `make fix` to auto-format
2. Run `make dev` to validate (lint, typecheck, test)
3. Fix issues before committing

## Project Structure

```
project/
├── src/              # Source code
├── tests/            # Test files
├── pyproject.toml    # Poetry config + tool settings
├── Makefile          # Build commands
└── CLAUDE.md         # This file
```
