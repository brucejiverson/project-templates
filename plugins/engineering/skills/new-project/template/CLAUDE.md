# CLAUDE.md - __PROJECT__

## User preferences

- Has agents set up and likes them used (see **Delegating to agents**).
- The mediocre admire complexity; genius is shown through simplicity. Keep it simple.
- Very clear, people-oriented communication, almost as if to a layman or a young person.

## What this project is

<One paragraph: the problem, who it is for, what exists today. Fill in from `docs/01_concept.md`.>

## Where the rest lives

| What | Where |
|------|-------|
| Problem, requirements, scope | `docs/01_concept.md` |
| Architecture and key decisions | `docs/02_implementation.md` |
| Files / parts / functions | `docs/03_design_map.md` |
| How the three docs are meant to be used | `docs/PLAYBOOK.md` |
| Status of everything | `MILESTONES.md` (the only place status is claimed) |
| Hardware modules (if any) | `hardware/<module>/`, layout below |

Put package- or module-specific rules in a nested `CLAUDE.md` inside that folder (it loads automatically
when files there are touched) and add a row to this table. Keep this file for project-wide rules.

## Commands

```bash
make install   # uv sync + pre-commit hooks
make fix       # format and auto-fix lint
make dev       # lint, typecheck, test: run before every commit
uv run pytest -k test_name   # one test
```

## Code style

- Python 3.11+, managed with uv. Ruff for lint and format (config in `pyproject.toml`), pyright for types.
- Line length 120. Imports sorted by ruff (stdlib / third-party / local).
- Comments explain **why**, not what. Docstrings on public functions and classes.
- Small functions, early returns, max 3-4 levels of nesting. Named constants, not magic numbers.
- Errors: specific exceptions with the failing value in the message (`f"Port must be 1-65535, got {port}"`).
  Never catch and silence; log with context before re-raising.
- Tests live in `tests/`; a test folder never shares its name with the package.

## Behavioral guidelines

Source: [Andrej Karpathy's CLAUDE.md guidelines](https://raw.githubusercontent.com/multica-ai/andrej-karpathy-skills/main/CLAUDE.md).
They bias toward caution over speed; use judgment for trivial tasks.

| # | Rule | Guidance |
|---|------|----------|
| 1 | Think before coding | State assumptions; ask if uncertain. Offer interpretations rather than picking silently. Say when a simpler approach exists. Name what's confusing rather than guessing. |
| 2 | Simplicity first | Minimum code that solves the problem: no speculative features, one-caller abstractions, unrequested config, or handling for impossible cases. If 200 lines could be 50, rewrite it. |
| 3 | Surgical changes | Touch only what you must; match existing style. Remove only what your own change orphaned; mention other dead code rather than deleting it. Every changed line traces to the request. |
| 4 | Goal-driven execution | Turn tasks into verifiable goals ("fix the bug" means reproduce it with a test, then make it pass). Multi-step plans get a verify step per line. |

| Extension | Guidance |
|-----------|----------|
| Checkpoint | After each significant step of a multi-step task, report progress rather than plowing ahead on a possibly broken state. |
| Read before write | Read existing callers and shared utilities before adding code near them. |
| Fail loud | Surface partial failures and skipped cases. Never report success you did not test. Reading a log is not verification. |
| Brutal completion | "Done" means every item in the request, not the convenient 80%. If something was deferred or half-finished, finish it or say plainly what remains and why. |
| Session budget | For long sessions, summarize progress and start fresh rather than letting context grow forever. |

### Delegating to agents

Err on the side of handing sizable chunks of work to subagents. The `engineering` plugin (from the
`project-templates` marketplace, enabled in `.claude/settings.json`) provides `engineering:python-pro`,
`engineering:code-reviewer`, `engineering:test-automator`, `engineering:debugger`,
`engineering:refactoring-specialist`, `engineering:documentation-engineer`, `engineering:performance-engineer`,
`engineering:embedded-systems`, `engineering:mechanical-designer` and `engineering:systems-engineer`. Pick the
one whose remit matches before falling back to a general-purpose agent.

Match the model to the task: Sonnet for well-specified, mechanical work (implement a described change, tests
against a spec, sweeps, doc updates); Opus for ambiguous, design-heavy or judgment-heavy work. Spot-check every
hand-back: open the files and confirm the change landed. Do not trust an agent's summary of its own edits.

### Working with the maintainer

The maintainer has a clear vision of what the product must do but does not carry the codebase in their head.
Put decisions to them as **capability trade-offs** ("should it be allowed to run a step it can't verify?"),
never as function, flag or file choices. Before asking about any module or config, say in one sentence what it
is *for*. Code-level decisions are yours: state the choice and the reason in a line, mark it overridable, move on.

### Status doc convention

Status lives in `MILESTONES.md` only. Don't write "done", "complete" or "not implemented" into READMEs,
docstrings or comments; point to the tracker. Every status claim carries a last-verified date, at the
granularity actually checked. Don't fabricate precision.

## Design decisions (V-model)

Design decisions navigate the systems-engineering V, applied recursively. At any level: (1) state the
requirements that bound the choice at that level, (2) select a concept that satisfies them, (3) descend: the
chosen concept's parts each get their own requirements and selection. The right side of the V is
verification: each level's requirements are what the built thing is later checked against, so they are written
where the choice is made, not reconstructed after it.

Every decision doc says:

| Field | Question it answers |
|---|---|
| Level | What is being chosen: a subsystem, a concept, or a part number? |
| Requirements at this level | What bounds the choice, in units, stated before options were compared? |
| Pushed down | What was deliberately left to the next level? |

A doc that doesn't name its level tends to conflate a concept choice with an implementation choice; the
concept then inherits the limits of one implementation, and the comparison is quietly rigged. A concept choice
one level up can delete a whole level of downstream decisions (e.g. "buy an integrated actuator" removes the
gearbox/encoder/controller selection entirely); that stays visible only if each doc names its level.

Document conventions:

- **† marks a value not decided or not measured.** Keep the dagger and write the method that will produce the number. Never invent one.
- **Cite, do not restate.** Upstream requirements are referred to by ID and file.
- **CONFLICT** flags a disagreement between documents; never resolve one silently.
- Part numbers are constraints (what was fixed), not requirements (what the thing must do).

## Hardware modules

Delete this section if the project has no hardware. Start a module with the `engineering:new-hardware-module`
skill; collect bought-part facts with `engineering:part-data`; draw cables with `engineering:cable-drawing`.

Each module is one folder under `hardware/` holding everything about it:

```
hardware/<module>/
├── README.md      # what it is, what is in each folder (no status claims)
├── docs/          # conops, requirements, concept_selection, test plans, test_evidence/
├── mechanical/ electrical/ firmware/   # only if the module has them
├── src/<module>/  # code, if any
├── tests/
├── config/        # settings files the code reads
├── scripts/       # things you run on the bench
├── release/       # release_notes_v<X.Y>.md per version, release BOM
└── units/         # one traveler per built unit (<ACR>_<NNN>.md)
```

- A module never imports another module's code; shared code goes in `src/` or a shared package.
- Project-wide docs (`MILESTONES.md`, `docs/`) link into modules; they don't hold module content.
- Bought-part fact sheets: `hardware/common/components/<maker>_<partnumber>/`, one per part, every number sourced.

## Plans

Every implementation plan ends with a **Verification** section: the commands or checks that prove each item is
done (`make dev`, a named test, a file that must exist, a behaviour to observe). Run them before reporting
the plan complete, and list anything that could not be verified.
