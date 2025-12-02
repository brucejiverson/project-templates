# CLAUDE.md - AI Coding Guidelines

## Creating a New Project

When the user asks to "create a new project called X" or similar:

1. **Create new directory** as sibling: `/home/bruce/software_projects/X/`
2. **Initialize git**: `git init` in the new directory
3. **Copy and customize these files:**
   - `pyproject.template.toml` → `pyproject.toml` (replace `project_name` with `X`)
   - `Makefile.template` → `Makefile` (replace `project_name` with `X`)
   - `CLAUDE.md` (update project structure section with `X`)
   - `.gitignore` (copy as-is)
   - `01_concept.md`, `02_implementation.md`, `03_design_map.md`, `PLAYBOOK.md` (copy as-is)
4. **Create directories:**
   - `src/X/` with `__init__.py`
   - `tests/` with `__init__.py` and a placeholder test
5. **Create `README.md`** for the new project
6. **Do NOT copy** the template's README.md or .git/

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
