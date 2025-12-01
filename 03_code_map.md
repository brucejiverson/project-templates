# Code Map

## Project Structure

```
project/
├── src/
├── tests/
└── config/
```

## Modules

### Module: [Name]

**Purpose:**

**Files:**
- `filename.ext` - description

**Key Functions:**

```
function_name(params) -> return_type
  - What it does
```

**Unit Tests:**
- Test case 1
- Test case 2

> **Guidance**: Specify interfaces, not implementations. Let the LLM figure out the internals. Don't stub out every method - describe what each module does and its public API.

## Dependencies

External libraries or services required.

## Example Interactions

Show concrete examples of how the system behaves. Include sample inputs, outputs, data structures, or user flows as relevant to the project.

## Error Handling

How errors are managed across the system.

> **Guidance**: This document must stand alone - the implementing LLM may not see the other documents. Include enough context to build from, but resist over-specifying implementation details.
