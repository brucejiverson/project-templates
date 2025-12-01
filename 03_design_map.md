# Design Map

## Project Structure

```
project/
├── src/           # Software source code
├── tests/         # Test files
├── cad/           # CAD files, drawings
├── docs/          # Documentation, datasheets
└── config/        # Configuration files
```

> **Guidance**: Adapt to your project. Software-only might just have src/tests. Hardware-only might have cad/drawings/bom. Show what actually exists.

## Modules / Assemblies

### [Name]

**Purpose:**

**Files / Parts:**
- `filename.ext` or `part_name` - description

**Key Functions / Features:**

```
function_name(params) -> return_type
  - What it does
```

Or for hardware:
- Feature description and critical dimensions
- Interface with other assemblies

**Verification:**
- How to test this module/assembly works

> **Guidance**: Specify interfaces, not implementations. For software: describe what each module does and its public API. For hardware: describe function and critical interfaces. Let the implementer figure out internals.

## Dependencies

External libraries, services, or purchased components required.

| Dependency | Version/Spec | Purpose |
|------------|--------------|---------|
|            |              |         |

## Example Interactions

Show concrete examples of how the system behaves.

> **Guidance**: For software - sample inputs/outputs, API calls, user flows. For hardware - operational sequences, adjustment procedures. Make it concrete enough that someone could verify the system works.

## Error Handling / Failure Recovery

How errors and failures are managed.

> **Guidance**: For software - exception handling strategy, logging, recovery. For hardware - what happens when things jam, misalign, or wear out? How does the user recover?

---

> **Guidance**: This document must stand alone - the implementing LLM or fabricator may not see the other documents. Include enough context to build from, but resist over-specifying implementation details.
