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

## Comments & Documentation

**Comments explain WHY, not WHAT** - code shows what happens, comments explain reasoning:

```python
# BAD: Duplicates the code
user_count = len(users)  # Get the length of users list

# GOOD: Explains the reason
user_count = len(users)  # Limit enforced by API quota (max 100)
```

- **Docstrings**: Required for public functions/classes (purpose, params, returns, raises)
- **Avoid obvious comments**: Don't restate what the code clearly shows
- **Comment when needed**: Non-obvious algorithms, business logic rationale, edge cases, workarounds, TODOs with context
- **Keep comments updated**: Outdated comments are worse than no comments

## Clean Code Principles

**Simplicity over cleverness** - prefer obvious solutions:

- **Function size**: Keep focused and small (~20-30 lines guideline)
- **Complexity**: Limit branching (cyclomatic complexity ~10 max)
- **Nesting depth**: Max 3-4 levels; use early returns to flatten:

```python
# BAD: Deep nesting
def process(data):
    if data:
        if data.is_valid():
            if data.user:
                return data.user.process()
    return None

# GOOD: Early returns
def process(data):
    if not data:
        return None
    if not data.is_valid():
        return None
    if not data.user:
        return None
    return data.user.process()
```

- **Single Responsibility**: Each function/class has one clear purpose
- **DRY Principle**: Extract repeated code into helper functions
- **Magic numbers**: Extract to named constants: `MAX_RETRIES = 3`
- **Meaningful names**: Variables should be pronounceable and searchable

## Error Handling

**Fail fast and fail clearly** - validate early, provide context:

- **Specific exceptions**: Use `ValueError`, `TypeError`, etc. - not generic `Exception`
- **Contextual messages**: Include what failed, why, and relevant values:

```python
# BAD: Vague error
raise ValueError("Invalid input")

# GOOD: Actionable error
raise ValueError(f"Port must be 1-65535, got {port}")
```

- **Input validation**: Validate all external inputs early in the function
- **Structured logging**: Use consistent format with appropriate levels (INFO/WARNING/ERROR)
- **Never silence**: Don't catch exceptions without handling or logging
- **Preserve context**: Log before re-raising to maintain error trail

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
