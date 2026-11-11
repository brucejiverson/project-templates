---
name: part-data
description: Collect the maker's data for a bought (off-the-shelf) part - electrical values, dimensions, mounting, mass - from datasheets, maker pages, seller listings and dimension drawings on the web, and file it as one reusable fact sheet with its sources under hardware/common/components/. Use when a design needs facts about a motor, servo, driver board, sensor, bearing or connector ("what is the stall current", "get the datasheet", "what are the dimensions of", "find the pinout"), or before sizing or drawing anything around a bought part. For the 3D CAD file itself use ots-cad-download.
---

# Part data

One folder per bought part, shared by every machine that uses it:

```
hardware/common/components/<maker>_<partnumber>/     lower case, underscores: kst_ds135mg
├── README.md      the fact sheet
└── sources/       maker datasheet PDF, dimension drawing, our screenshots of spec tables and drawings
```

If the recursive_robotics repo is on this machine, `hardware/common/components/kst_ds135mg/` there is a worked example.

## Before you start

Check the folder does not already exist. If it does, add to it; do not start a second sheet.

## Steps

1. **Search** the exact part number with "datasheet", "technical specification", "dimension drawing"
   (two or three WebSearch calls, sent together). Look for, in this order: the maker's own page, the
   maker's download page, a spec aggregator, then two or three sellers.
2. **Read the maker first.** If the maker's page gives its table as a picture (common), open the page in
   the maintainer's Chrome, zoom on the table, and save that screenshot into `sources/`.
3. **Get the datasheet PDF and the dimension drawing** if the maker publishes them. A direct link that
   works with `curl` is fine. A link that only works in a browser: click the site's own link in Chrome.
4. **Read two or three sellers** for what the maker left out (spline, connector, what is in the box).
   **Always look at the Amazon listing's pictures**: one of them is often a dimension drawing (open the
   listing in Chrome, step through the picture gallery, zoom on the drawing and save that screenshot).
5. **Always save the dimension drawing** into `sources/` when one exists anywhere (maintainer,
   2026-11-11), at the largest size the page offers, and show it in the fact sheet above the table of
   numbers read from it. A sheet with dimensions but no saved drawing is not finished.
6. **Write the fact sheet.** Sections: Electrical, Mechanical, "What the web could not answer", Sources.
   Add a Pinout or Mounting section when the part has one.
7. **Link it**: add a row to the table in `hardware/common/README.md` (create it if missing), and point the machine's own doc at
   the sheet in place of repeating the numbers.
8. **Tell the maintainer** what is still to be measured, as a short list.

## Rules for the fact sheet

- **Every number has a source tag** (S1, S2...) that points to a row in the Sources table: who, what, link,
  date seen.
- **Trust order: maker > several sellers that agree > one seller.** When sources disagree, show both
  values and say which wins and why. Never average them and never pick silently.
- **Not published means MEASURE.** Write "MEASURE" in the value cell. Never fill a gap from a sibling
  part, from memory or from what is typical. If a sibling's value is a useful hint, say it is a
  sibling's.
- **Keep the maker's units and wording**, then add the SI value beside it (5.2 kgf·cm (0.51 N·m)).
- **Dimensions read off a picture are for layout only.** Mark them "from drawing, check with calipers".
  Anything a part must mate with gets measured before it is printed or cut.
- **Record what was not obtained** and why (dead link, login wall, refused fetch, large file waiting for
  an OK). The next person should not repeat a dead route.
- No status claims in the sheet (status lives in `MILESTONES.md`).

## Rules for getting files (strict)

- **Never get past a block.** CAPTCHA, bot check, 403, 429, login wall: stop that route and write it
  under "Not obtained". No retry loops, no user-agent or referer tricks, no second tool on the same URL.
  The one allowed step up is opening the page in the maintainer's Chrome and clicking the site's own
  link, as a person would.
- **Logins:** only a session the maintainer already has open. Never type a password or create an account.
- **Ask before a download that is not plainly the one datasheet or drawing for this part**: a bundle,
  a zip, an installer, anything over a few MB. Say the file name, where it comes from and its size.
- **Downloads are untrusted.** Put each in its own new, empty folder first. Never run anything from it.
  Unpack zips there and copy out only the PDF or image that is needed.
- **What goes in `sources/`:** maker datasheets and maker drawings (they are published to be handed to
  customers), and our own screenshots of a maker's spec table or of a dimension drawing in a listing.
  **Seller photos and marketing pictures are linked, not copied.**
- Record a SHA-256 for each saved PDF in the Sources table.
- Nothing about the maintainer or the project goes into a search query or a web form.
- Close every Chrome tab you opened.

## What was learned (add to this list when a new site teaches something)

- **Maker spec tables are often pictures**, so a text fetch of the page returns nothing useful. Open the
  page in Chrome and zoom on the table (KST, 2026-11-11).
- **Maker download links can be dead** (KST's per-part link gave a 404) while a whole-series bundle sits
  on the maker's download page. Look there before giving up.
- **Files on a maker's file host may refuse `curl` (403)** but download fine from a click in Chrome.
- **Several shop sites answer automated page reads with 429 "too many requests".** Do not hammer them;
  the search result summary plus one seller that does answer is usually enough.
- **servodatabase.com** is a quick cross-check for hobby servos (torque, speed, size, spline, pulse
  range). It is an aggregator and is sometimes wrong (it listed this servo's motor and gears differently
  from the maker).
- **Amazon listings often carry the dimension drawing the maker's site lacks** (maintainer's tip,
  2026-11-11; it was the only drawing found for the DS135MG). The maintainer's Chrome is logged in to
  Amazon: look only, never click Add to cart or Buy.
- **A drawing in a listing has no tolerances and unclear leader lines.** Write down what each number is
  taken to mean, and mark any that are a guess.
- **Cheap hobby parts rarely publish stall current.** Say so early; do not spend ten searches hunting
  for it.
- **Not yet tried:** a part with a real PDF datasheet (motor driver, sensor). The PDF steps above
  (download, SHA-256, reading tables out of the PDF) are written from the plan, not from a run.

## Hand-offs

- The 3D CAD file of the part: download the maker's STEP under the same file rules, into `sources/`.
- A cable or pinout drawing from the data: `cable-drawing`.
