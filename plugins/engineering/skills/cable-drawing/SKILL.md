---
name: cable-drawing
description: Make or edit a cable / harness drawing (WireViz YAML) for any hardware module. Use when the user asks for cable drawings, harness drawings, wiring diagrams, a pinout for a cable, or when a connectorized physical item (a bought cable we cut, a sensor or motor with a pigtail, a cable we make) has no drawing yet. Covers wire gauge, shielding, twisted pairs, lengths, notes and revision rules.
---

# Cable drawing

One drawing per physical cable design, in the module's own folder:
`hardware/<module>/electrical/harnesses/<name>.yml`, rendered with WireViz (`pip install wireviz`, plus graphviz's
`dot`). If the recursive_robotics repo is on this machine, `hardware/small-arm/electrical/harnesses/` there has a
worked set with a `Makefile` and `_template.yml` to copy.

## What needs a drawing

- **Every connectorized physical item**, not only cables we make: a bought cable we cut or re-terminate (e.g. an
  endstop sold with a 1 m JST-XH lead), a motor or sensor with a pigtail, a cable we crimp ourselves.
- A cable built N times from one design gets **one** drawing; list the cable IDs it covers (e.g. `CBL-JNT-1..6`).
- Bought cables used as-is (USB, mains cords) get a line in the machine's interconnect table, not a drawing.
- **Mains is bought cords only.** Never draw a hand-made mains conductor; the enclosure takes a standard IEC inlet.

## Rules for every drawing

| Topic | Rule |
|---|---|
| **Gauge** | Size each wire for its current, not by habit. State the current in the wire's notes (`2.0 A peak †`). Use the conservative bundled-wire column below, then check that the connector contact rating is not the weaker link (JST-XH is ~3 A per contact). For long low-voltage runs, check voltage drop as well. |
| **Crimp range** | The wire must fit the connector's crimp: JST-XH takes 22-28 AWG, so a 20 AWG wire does not go in an XH. If the current needs a thicker wire than the connector takes, change the connector or land the wire on a screw terminal. |
| **Shielding** | Add `shield: true` where it matters, and say where the drain lands (one end only, usually the controller end): motor phase cables run near signals, encoder/Hall/analog lines, cameras, anything over ~0.5 m next to a motor. Don't shield plain switch or power wires by default. |
| **Twisted pairs** | Call them out in the cable `notes`: CAN_H/CAN_L, any differential signal, each stepper coil pair (A+/A−, B+/B−), each power pair (+/0 V) on runs past ~0.3 m. |
| **Length** | Required on every cable. Until the first build, write `Length: TBD (set at first build)` in the cable `notes` and **leave out `length:`**, because WireViz rejects a non-number. After the first build, enter the measured length and note who measured and when. |
| **Moving joints** | Any cable that crosses a joint says so in its notes and names a flex-rated (high-strand, silicone or PUR) wire. |
| **Unknowns** | Mark `†` and say how the value will be found (e.g. "colours † — check against the cable in hand"). Never invent a part number, colour order or current. |
| **Sources** | Each fact from the repo or a datasheet gets a citation in a header comment (`file:line`, or a URL / order). |
| **Notes** | Notes are fine anywhere: assembly hints, strip lengths, "land by function, not by position". Do not use `->` inside a notes string, because it breaks graphviz. |
| **IDs** | Cable IDs `CBL-<TYPE>-<FROM>-<TO>[-<SEQ>]`; harness part number (if the project numbers parts) in `metadata.pn`; the drawing file can keep a short name. |
| **BOM** | The drawing's BOM is only what is bought to build this cable. A connector that is a device with its own BOM line (PSU, driver board, motor, a sensor drawn elsewhere), and a wire that is part of a bought pigtail, gets `ignore_in_bom: true`. |

Conservative current per conductor, copper, bundled in a harness (chassis wiring at about 30 °C rise). Use it as
the ceiling, not the target:

| AWG | Max A | Typical use |
|---|---|---|
| 26 | 1.0 | sensor signals |
| 24 | 1.5 | endstops, encoder, logic |
| 22 | 3 | CAN, servo, small motors (connector-limited) |
| 20 | 5 | NEMA 17 coils, 24 V joint drops |
| 18 | 7 | NEMA 23 coils (~3-4 A/phase), 24 V trunk |
| 16 | 10 | 24 V main trunk, PSU output |
| 14 | 15 | heavy DC bus only. Mains is bought cord |

## Revisions

Every file starts with a header comment block, and `metadata.revision` matches the top entry:

```yaml
# REVISION HISTORY
# Rev  Date        Built?  Change
# 0.1  2026-10-31  no      Initial release (draft). Lengths TBD at first build.
```

- The first version is `0.1` and is labelled **"Initial release (draft)"**.
- **Before any of the cable has been built**, edit freely and keep the revision, adding a line to the history only if
  the change is worth knowing.
- **Once any of the cable has been built**, a major edit raises the revision (`0.1` to `0.2`, or `1.0` at first
  verified build) with a history line saying what changed and whether built cables need rework. A major edit is
  anything that changes what gets built: pinout, gauge, connector, conductor count, shield, twist or length.
  Fixing a typo or a note is not major.
- Record builds in the history (`Built? yes, 2 built 2026-11-04`) so the next editor knows which rule applies.

## Steps

1. Read the module's interconnect / electronics doc and any existing harness YAML; reuse its connector definitions.
2. Write the YAML from `_template.yml`: header (revision history, sources, † list), connectors with `pinlabels`
   and `pincolors`, cables with gauge, wirecount, colours, shield and notes (current, twist, length or TBD), and
   the connections.
3. Render it: `wireviz <file>.yml -o output/<name>` (or `make` in the harnesses folder). It must render without
   error. Open the PNG and check that the pins land where the pin list says, and follow every wire to a real
   terminal at both ends (a ground wire tied to nothing is the usual error). `output/` is gitignored: renders are
   never committed, so say so in the harness README.
4. Update the harnesses `README.md` table (file, cable IDs, what), including what has been rendered and what has
   been looked at by a person.
5. Report what is still `†` and what has not been checked. A drawing that rendered is not a cable that was built.
