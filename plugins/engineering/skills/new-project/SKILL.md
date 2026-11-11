---
name: new-project
description: Create a new project (software, hardware or both) from the standard template - uv, ruff, pyright, pre-commit, CI, CLAUDE.md working rules, the shared engineering agents - then take it through concept, implementation plan and design map with the maintainer. Use when the user says "create a new project called X", "start a new repo", "new project for X", or "set up a project like my others".
---

# New project

Two parts: make the folder (a script, one minute), then define the project (the three docs, with the
maintainer, one review stop after each).

## 1. Make the folder

```bash
bash <this skill's folder>/new_project.sh <name> [parent_dir]   # parent defaults to ~/Code
```

The name is lower case with `-` or `_`; the Python package is the same name in snake_case. The script copies
`template/`, fills in the names, runs `git init`, `uv lock`, `uv sync`, installs the git hooks and makes the
first commit. It refuses to overwrite an existing folder. Afterwards:

- Run `make dev` in the new folder and confirm it passes. Report the output, not "it worked".
- If the project has no hardware, delete the **Hardware modules** section from its `CLAUDE.md`.
- Do not create a GitHub remote or push unless the maintainer asks.

## 2. Ask the intake questions, all together, before drafting

Asking these one at a time, late, is what makes designs reverse direction. Ask them in one go, in plain words,
as capability trade-offs, and record the answers with the date in `docs/01_concept.md`.

1. What is the **one job**, and for whom? What is explicitly **out of scope**?
2. What exists today, and why is it not good enough (prior art, a tool already owned)?
3. What is the **limit** on money, time and size? Written as a hard check, it is applied to every decision.
4. How will we **know it works**? One or two checks that could fail.
5. Software, hardware, or both? For hardware: power available, who loads and unloads, how the work is held.
6. Which **exact** parts, services or files must it use? Check the real thing (order history, the part in hand,
   the existing repo) before writing requirements around it.
7. **Later / optional** items: name them so the design keeps them possible without building them.
8. **Failure policy**: what happens when something goes wrong (default: retry up to 2 times if safe, then stop
   and tell a person).

## 3. The three documents

Templates are in the new project's `docs/`; `docs/PLAYBOOK.md` says how to fill them and the usual pitfalls.

| # | Document | Answers | Stop |
|---|----------|---------|------|
| 1 | `docs/01_concept.md` | WHAT and WHY: problem, users, requirements with a verification each, scope, prior art | Maintainer reviews before step 2 |
| 2 | `docs/02_implementation.md` | HOW: architecture, choices with alternatives, failure modes, MVP phase | Maintainer reviews before step 3 |
| 3 | `docs/03_design_map.md` | WHERE: files / parts / functions, stands alone for the implementer | Maintainer reviews before building |

Then fill the **What this project is** paragraph in the project's `CLAUDE.md` and add the first rows to
`MILESTONES.md`.

Rules while drafting:

- Scale detail to size: a small tool needs two or three requirements, not ten. Omit sections that do not apply.
- Each decision names its **Level / Requirements at this level / Pushed down** (V-model, in the project `CLAUDE.md`).
- **† marks an unknown** with the method that will produce it. Never invent numbers or percentages.
- For hardware modules inside the project, use `engineering:new-hardware-module` instead of these three docs.
- When the maintainer answers a question, find every doc that asked it and mark it closed with the date.

## Which model

| Work | Model |
|------|-------|
| Intake questions, concept and implementation docs, final review | Opus (judgment-heavy) |
| Design map from an approved implementation doc, scaffolding, tests from a spec | Sonnet subagent (`engineering:python-pro`, `engineering:test-automator`) |
