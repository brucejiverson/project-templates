# <Machine>, release notes v<X.Y>

**Status:** Draft / Released (YYYY-MM-DD)
**Replaces:** v<previous>
**CAD:** <CAD document link and version, or `cad/v<X.Y>/`>
**BOM:** <`release/bom.csv` at commit ..., or link>

## Why this version

<One or two sentences: what problem in the last version this fixes, or what it adds. Link the evidence: an incident
report, a test result, a requirement.>

## What changes

| Part or item | Was | Now | Why |
|--------------|-----|-----|-----|
| <part number and name> | <old> | <new> | <reason, link> |

## What does not change

<Anything someone might expect to change but does not. Delete if nothing.>

## Effect on built units

<Can an older unit be upgraded to this version? What has to be swapped? Which units are affected?>

| Unit | Built to | Upgrade to this version? |
|------|----------|--------------------------|
| <ACR NNN> | v<old> | Yes / No / Not yet, <why> |

## Checks before calling it released

- [ ] CAD frozen and its version recorded above
- [ ] BOM regenerated
- [ ] Build instructions updated for the changed parts
- [ ] Tests that cover the changed parts named, and re-run on the first unit built to this version
