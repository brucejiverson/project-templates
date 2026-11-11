---
name: new-hardware-module
description: Start a new hardware module (a machine, mechanism, end effector or device; a folder under hardware/) and take it through the systems-engineering V - ConOps, requirements, concept selection, sizing, electrical plan and BOM, traceability and test plan, final review - with a review stop at each level and the right model for each step. Use when the user says "start a new machine", "new module", "new device", "set up a hardware project for X", or asks for specs, a concept down-selection or an electrical plan for hardware that has no folder yet.
---

# New hardware module

Release notes and unit traveler templates are in this skill's `templates/` folder. A full worked example of
this sequence lives in the recursive_robotics repo (`hardware/small-arm/`, `hardware/drill-press/`) if it is
on this machine.

## Step 0: intake questions (ask before drafting anything)

One past run went through nine reversals (printed vs aluminium, drill vs ream, milling in and out, mains vs
24 V) because these were asked one at a time, late. Ask them together, in plain words, as capability
trade-offs. Record the answers with the date in the ConOps.

1. What is the module's **one job**, and which **materials or parts** does it work on? What is out of scope?
2. **Automation bar:** must it run with no person during a job from the first version? Do not propose a "person
   does it in version 1" phasing that breaks the bar; if the cheap version cannot meet it, say so and offer a
   costed option that does.
3. **Capital and size limit:** money, footprint, shared-machine time. Write it as a hard-check requirement.
4. **Sizes and counts:** a realistic range (e.g. M3-M6), not "standard sizes". The tool count and tool-change
   design follow from it. Who owns the table that lists them?
5. **Who loads and unloads**, and from where?
6. **Power:** mains allowed inside the module, or low-voltage DC only?
7. **Tolerance meaning:** the right *size*, or the right size in the right *place*? That picks between a
   self-centering method and a position-driven one.
8. **Optional / later** items: name them so the design keeps them possible but does not build them.
9. **Which exact parts** does it handle or use? Check the order history or the part in hand before writing
   requirements around it.
10. **How is the work held?** Clamped, gripped, or left to gravity or friction?
11. **Failure policy:** default retry up to 2 times if safe, then stop and call a person. Confirm or record the exception.
12. **Replacement time:** how fast must a spare be swapped in (e.g. 30 minutes walk-up to working)? It steers
    toward quick mounts, plug-in cables and fast calibration.

Also run a quick market survey (buy before build) as `docs/market_options.md`, labelled search-level and
unverified until each price and spec is checked on a maker page.

## The sequence

| # | Step | File it produces | Who does it |
|---|------|------------------|-------------|
| 1 | Read the plan or request the module comes from; review it for gaps and conflicts before building on it | review notes to the maintainer | Orchestrator |
| 2 | Create the folder (layout below) with an empty `docs/test_evidence/`; add the module to the project `CLAUDE.md` and `MILESTONES.md` | `README.md`, `docs/`, ... | Orchestrator |
| 3 | **ConOps** (Level 1): problem, what it works with, its jobs, why this and not an existing product, requirements owned upstream (cited) vs proposed, scope, constraints, open questions | `docs/conops.md` | Orchestrator; maintainer reviews |
| 4 | **Requirements** (Level 2): ID, specification, basis or derivation, verification with a pass rule that could fail. Part numbers are constraints, not requirements | `docs/requirements.md` | Orchestrator drafts; **Opus reviews**; apply the review |
| 5 | **Concept selection** (Level 2): real alternatives with numbers, a V-model table per decision, scoring matrix plus hard pass/fail checks, conflicts, proposed requirement changes, questions for the maintainer | `docs/concept_selection.md` | **Opus** (`engineering:systems-engineer`) |
| 5b | **Operating sequence** (if it runs without a person), written *with* the concept, not after: it is what exposes a concept that cannot be automated | `docs/automation_sequence.md` | Same agent as step 5 |
| 6 | Put open questions to the maintainer as capability trade-offs; record each answer with its date; fold approved changes into the requirements. **Sweep every doc that asked the question** and mark it CLOSED with the date and answer | updated docs | Orchestrator |
| 7 | **Sizing** (Level 3): loads, torques, speeds, margins, via scripts. Provisional until inputs are reviewed | `docs/sizing.md`, scripts | `engineering:mechanical-designer` (Sonnet) |
| 8 | **Electrical**: parts and drivers, block diagram, pinouts, power budget, interconnect, BOM (Item, Qty, Price, Buy, Documentation, Notes), one drawing per cable (`engineering:cable-drawing`). Bought-part facts via `engineering:part-data` | `docs/electronics.md`, `electrical/` | `engineering:embedded-systems` (Sonnet); orchestrator renders and checks |
| 9 | **Traceability and test plan**: every requirement maps to a test and every test back to a requirement; scripts and timestamped evidence go in `docs/test_evidence/` | `docs/test_traceability_matrix.md` | Sonnet |
| 10 | **Final review**: traceability both ways, numbers consistent across documents, every unknown marked †, citations checked against real files, `MILESTONES.md` rows exist with a last-verified date | review report | **Opus** |

**Stop and report to the maintainer after step 4 and after step 8.** If asked to go further, do it, but say
which stop was passed and that the earlier documents are unreviewed.

### The operating sequence document (step 5b)

A step list alone is unclear. It opens with: a plain-language picture of the module; a **cast list** of every
moving thing (what it is, what it moves, what moves it, what tells it, what it reports back); a labelled side
and top view (ASCII) and one mermaid sequence diagram; a **who-moves-what table per step** (what happens, which
actor, checks before and after, failure response); explicit answers to how a part gets in and out, how it is
held (what actuates, how force is limited, how seating is sensed), how each feature is lined up, how a tool is
changed, and how it knows the work is done and good; then a one-part journey a non-programmer can follow.

### Working with the agent that owns the documents

- Give **one agent ownership** of conops, requirements, concept selection and the operating sequence, and send
  every maintainer answer to that same agent (`SendMessage`) so the files stay consistent. Each reply should be
  a short summary of what moved and what the maintainer must still decide.
- When an answer **reverses** an earlier one, strike through the old item (keep its ID, never renumber), date
  it, and say what the new answer displaces.
- A reported number is the agent's arithmetic, not a measurement. Say so, and have it **re-derive** any figure
  whose input later changed.
- **Spot-check every hand-back** (open the files, grep that the answer landed). Don't trust the agent's summary.
- Keep each decision to its recommendation, the numbers and a table of rejected options; move derivations to an
  appendix. Concept documents otherwise pass 2,000 lines.
- Keep **one source** for any table two sides read, and name its owner.

### Electrical checks (step 8)

Per-cable rules are in `engineering:cable-drawing`. At module level:

- Current vs contact rating uses the **worst case** (supply ceiling), not the average.
- A connector in a bus drop (CAN, RS-485) adds to the stub length.
- A nominal supply at a driver's top voltage has no margin.
- Every cable length is `TBD (set at first build)` until the first build measures it.

## Document header and conventions

Every Level 2 and Level 3 document opens with a quoted block:
`Level` / `Requirements at this level` / `Placeholders` / `Pushed down` / `Status` / `Date`.

- **† marks a value not decided or not measured.** Keep the dagger and write the method that will produce it.
- **Cite, do not restate.** Upstream requirements are named by ID and file.
- **CONFLICT** flags a disagreement between documents; never resolve one silently.
- Status claims go in `MILESTONES.md` only, with a date.
- Part numbers are constraints, not requirements.

## Folder template

```
hardware/<module>/
├── README.md       # what it is, what is in each folder (no status claims)
├── docs/           # conops, market_options, requirements, concept_selection, automation_sequence,
│                   #   sizing, electronics, test_traceability_matrix, test_evidence/
├── electrical/     # interconnect, bom, harnesses/ (WireViz YAML)
├── mechanical/ firmware/   # only if the module has them
├── src/<module>/   # code, if any
├── tests/          # a test folder never shares its name with the package
├── config/         # settings files the code reads
├── scripts/        # things you run on the bench
├── release/        # release_notes_v<X.Y>.md (from templates/release_notes.md), release BOM
└── units/          # one traveler per built unit, <ACR>_<NNN>.md (from templates/traveler.md)
```

A module never imports another module's code; shared code goes in a shared package.

### Versions and units

- A version is a design: `v1.0`, `v1.1`, `v2.0`. Change the second number when the design changes but stays the
  same module; the first when it is a new design. Release notes are written before the build and are final once
  a unit is built to them; later fixes go in the next version.
- A unit is one physical thing with a serial written on it (`VIS 001`; file name `VIS_001.md`). Its traveler
  stays with it for life: add log lines, never rewrite old ones. A unit reworked to a newer version keeps its
  serial.

## Which model for which step

| Work | Model | Why |
|------|-------|-----|
| Requirements review, concept selection, final review | Opus, always | Judgment-heavy; a quiet error is expensive |
| Sizing, electrical choices, code, test plans | Sonnet | Well specified once the concept is chosen |
| Kinematics, motor drivers, anything where a quiet error costs hardware | Opus, and verify | — |

If the maintainer names a model for a step, that wins; say which step ran on which model.

## Gotchas

- A stand-in "phase 1" that breaks the maintainer's bar is not an answer; ask instead.
- Several sources can name different parts for the same function; ask which one is fitted.
- Check every citation against the real file; reviewers routinely find wrong ones in first drafts.
- Copy templates, not old documents, and cite numbers instead of copying them.
