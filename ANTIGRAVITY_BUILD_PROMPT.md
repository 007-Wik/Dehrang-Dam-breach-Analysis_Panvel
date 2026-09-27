# BUILD PROMPT — Dam Break CCCSS Documentation (Dehrang Dam DBA)

Paste this whole prompt to Antigravity as-is. It replaces any previous
attempt at this task. Do not summarize, shorten, or paraphrase anything
described below as "full content" — reproduce it verbatim, including
every paragraph, table, equation, and figure, in the original document
order.

## 0. Ground-truth source material (already prepared — do not re-parse the .docx)

Before doing anything else, unzip `supporting_files.zip` (provided
alongside this prompt) into the repo root. It contains:

```
docs_source/                         <- ground-truth chapter text, extracted
  00_index.md                           verbatim from the report via pandoc,
  01_introduction.md                    already split at chapter boundaries.
  02_dam_description.md                 Treat every file in here as the
  03_idf_analysis.md                    authoritative, complete text for
  04_hydrology_hechms.md                that chapter — full paragraphs,
  05_dambreak_analysis.md               full tables (GFM pipe-table format),
  06_hecras_breach_methodology.md       figure captions, and image
  07_results_discussion.md              references all included.
  annexure_I_eac_table.md
  annexure_II_idf_tables.md
  annexure_III_abm_distribution.md
  annexure_IV_froehlich_derivation.md

assets/                               <- every figure/map embedded in the
  (25 renamed .png / .jpeg files)         report, already extracted and
                                          renamed to match their captions
                                          (e.g. ch03_fig3.1_gumbel_...png,
                                          annexIV_inundation_hazard_map_01.jpeg)

scripts/
  idf_gumbel_analysis.py               <- reference Gumbel EV-I / Lognormal /
                                           IDF / ABM script implementing the
                                           exact methodology in Chapter 3.
                                           Populate RAINFALL_SERIES with the
                                           real 31-yr IMD series before use.
```

**Do not** go back to the original `.docx` and re-extract/re-summarize —
use the files in `docs_source/` as the single source of truth for text,
and `assets/` as the source of truth for images. This avoids the
information loss that happened last time.

## 1. Non-negotiable rules

1. **No summarizing, ever.** Every paragraph in `docs_source/*.md` must
   appear in the corresponding `docs/*.md` page in full. If a paragraph
   is 6 sentences in the source, it is 6 sentences in the output.
2. **Every table stays a table.** Convert GFM pipe tables in the source
   directly into MkDocs-rendered tables — do not turn a table into a
   bullet summary.
3. **Every equation stays an equation.** Wrap equations in `$$ ... $$`
   (block) or `$ ... $` (inline) for the `mkdocs-material` +
   `pymdownx.arithmatex` renderer (see Section 5 for the exact `mkdocs.yml`
   config this requires). Convert the plain-text equations found in the
   source (e.g. `B_avg = 0.1803 * K0 * Vw^0.32 * Hb^0.19`) into proper
   LaTeX (e.g. `$$ B_{avg} = 0.1803 \cdot K_0 \cdot V_w^{0.32} \cdot H_b^{0.19} $$`).
4. **Every figure is rendered, not linked-past.** Use standard Markdown
   image syntax `![caption](../assets/filename.png)` with the exact
   filename from `assets/`, placed at the same point in the text where
   the figure appears in the source, followed by its italic caption line.
5. **Preserve document order.** Do not reorder sections, tables, or
   figures relative to the source chapter file.
6. **Preserve numbering.** Keep the report's own section numbers (e.g.
   "3.5.1", "Table 8", "Figure 5.3") in headings/captions so cross-
   references still make sense.

## 2. Target file structure (final decision — build exactly this)

The existing 5 filenames in `docs/` are kept (renumbered into report
order) and one new file is added for the Introduction. Six files total,
covering all 7 report chapters + all 4 Annexures with nothing left out:

| New file | Content (from `docs_source/`) |
|---|---|
| `docs/00_Introduction.md` | `01_introduction.md` (Ch. 1: General, Objective, Scope, Limitations) |
| `docs/01_Storage_Elevation_Analysis.md` | `02_dam_description.md` (Ch. 2: dam/reservoir description, Table 1) **+** `annexure_I_eac_table.md` (Annexure I: EAC table + curve, appended as a final "Annexure I" section) |
| `docs/02_IDF_Analysis_Panvel.md` | `03_idf_analysis.md` (Ch. 3: IDF/Gumbel/ABM/SCS Type II) **+** `annexure_II_idf_tables.md` **+** `annexure_III_abm_distribution.md` (both appended as "Annexure II" / "Annexure III" sections) **+** the contents of `scripts/idf_gumbel_analysis.py` embedded as a fenced ```python code block under a new "## Reference Script" heading at the end of the chapter body (before the annexures) |
| `docs/03_DBA_Basin_HydroPrep.md` | `04_hydrology_hechms.md` (Ch. 4: HEC-HMS methodology, subbasin params, CN, Muskingum routing, inflow hydrograph) |
| `docs/04_DamBreak_Analysis.md` | `05_dambreak_analysis.md` (Ch. 5: model inputs & breach scenarios) **+** `06_hecras_breach_methodology.md` (Ch. 6: 2D mesh, Froehlich breach parameterisation) **+** `annexure_IV_froehlich_derivation.md` (Annexure IV: Froehlich derivation + the 10 inundation/hazard JPEG maps, appended as "Annexure IV" section) |
| `docs/05_Maps_GoogleColab.md` | `07_results_discussion.md` (Ch. 7: results, inundation discussion, hazard/vulnerability maps, EAP implications) |

Update `docs/index.md` navigation links and `mkdocs.yml`'s `nav:` block
to point to these six files in this order, replacing whatever the
previous nav pointed to.

## 3. Chapter-by-chapter build instructions

For **each** file in the table above:

1. Open the listed `docs_source/*.md` file(s) and copy the *entire* body
   into the new `docs/*.md` file, in the order listed — do not drop the
   opening narrative paragraphs before the first numbered subsection.
2. Convert the top-level `# N. Title` line from the source into an
   MkDocs page `# Title` (drop the leading report chapter number from
   the H1 only — keep numbers on every subsection, e.g. `## 3.2
   Frequency Analysis - Gumbel EV-I and Lognormal`).
3. Every `*Figure X.Y: caption*` line in the source must become, in the
   output: the image (`![Figure X.Y: caption](../assets/exact-filename)`)
   immediately followed by the caption rendered as an italic paragraph
   directly under it (MkDocs figure convention).
4. Every `*Table X: caption*` line must become a caption paragraph placed
   directly **above** its pipe table (MkDocs convention — captions
   precede tables), with the table reproduced in full immediately below.
5. Any `***Note:** ...*` block in the source becomes an
   `!!! note` mkdocs-material admonition block, e.g.:
   ```
   !!! note
       Validation: The 24-hr 100-yr intensity = 486.72 / 24 = 20.28 mm/hr...
   ```
6. Do not compress multi-item numbered lists (objectives, scope,
   limitations) into shorter bullet points — keep every numbered item
   and its full explanatory text.

### 3.1 Special handling — `docs/02_IDF_Analysis_Panvel.md`

- After the Chapter 3 body (through Section 3.5.2), insert:
  ```
  ## Reference Script

  Reference implementation of the Gumbel EV-I / Lognormal / IDF / ABM
  methodology described above. Populate `RAINFALL_SERIES` with the
  actual 31-year IMD annual-maximum series (Station ID 102187319)
  before running.

  ```python
  <full contents of scripts/idf_gumbel_analysis.py>
  ```
  ```
- Then append the Annexure II and Annexure III content as `## Annexure
  II — IDF Computation Tables` and `## Annexure III — Alternating Block
  Method (ABM) Storm Distribution` sections, each with their full tables
  intact.

### 3.2 Special handling — `docs/04_DamBreak_Analysis.md`

- After the Chapter 6 body, append `## Annexure IV — Froehlich (2008)
  Breach Parameter Derivation`, including both Froehlich equations (as
  LaTeX per Rule 3), the input-parameter bullets, and the full
  parameter-comparison table.
- Immediately after that table, render **all ten** inundation/hazard
  JPEGs (`annexIV_inundation_hazard_map_01.jpeg` through `_10.jpeg`),
  one per line, each as its own image (do not combine multiple images
  on one line — they must stack vertically and be individually
  viewable), followed by the closing note about the H1 hazard class
  pixel-visibility caveat.

### 3.3 Special handling — `docs/05_Maps_GoogleColab.md`

This is the largest chapter (Results & Discussion, ~950 lines of
source). Preserve every subsection exactly:
7.1 (Overtopping inundation) → 7.1.1 → 7.1.2 → 7.2 (Piping inundation)
→ 7.2.1 → 7.2.2 → 7.3 (Computation log/volume accounting) → 7.3.1-7.3.4
→ 7.4 (Flood inundation mapping discussion) → 7.4.1-7.4.5 → the second
"7.3" (Comparative Summary/EAP Implications, numbered 7.3 again in the
source — keep this numbering exactly as-is, do not renumber it, and do
not merge it with the earlier 7.3) → 7.3.1-7.3.2. Render all 4 figures
in this chapter in place.

## 4. Raw data / GIS files and outputs — chronological ordering

Wherever this documentation set references or lists raw data, GIS
layers, model files, or generated outputs (in `data/`, `models/`,
`outputs/`, or in any "Data Sources" / "Methodology" section you add),
order them chronologically by the actual analysis workflow, **not**
alphabetically:

1. Raw IMD rainfall series (`data/raw/`)
2. Copernicus GLO-30 DEM (`data/raw/` or `data/spatial/`)
3. Hydrologically conditioned DEM / basin & subbasin delineation
   (`data/processed/`, `models/HEC-HMS/`)
4. ESA WorldCover / Sentinel-2 LULC classification (`data/spatial/`)
5. USDA/soil hydrologic group maps and derived CN grid
   (`data/spatial/`, `data/processed/`)
6. HEC-HMS basin/meteorological model files (`models/HEC-HMS/`)
7. HEC-HMS simulation outputs — inflow hydrograph (`outputs/`)
8. HEC-RAS terrain, 2D mesh, Manning's n grid, storage-area/EAC input
   (`models/ArcGIS/`, `data/processed/`)
9. HEC-RAS breach plans (Overtopping, Piping) and simulation outputs
   (`models/ArcGIS/`, `outputs/`)
10. Final inundation/hazard maps and figures (`outputs/maps/`,
    `outputs/figures/`)

Reflect this same order in `data/README.md` and `outputs/README.md` if
you touch them, and in any generated `docs/methodology.md` overview
page.

## 5. `mkdocs.yml` requirements

Ensure the config includes, at minimum:

```yaml
markdown_extensions:
  - admonition
  - tables
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.superfences

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Home: index.md
  - 1. Introduction: 00_Introduction.md
  - 2. Storage-Elevation Analysis: 01_Storage_Elevation_Analysis.md
  - 3. IDF Analysis (Panvel): 02_IDF_Analysis_Panvel.md
  - 4. Basin Hydrology Prep: 03_DBA_Basin_HydroPrep.md
  - 5. Dam-Break Analysis: 04_DamBreak_Analysis.md
  - 6. Results & Maps: 05_Maps_GoogleColab.md
```

(Create `docs/javascripts/mathjax.js` with the standard MathJax config
if it does not already exist.)

## 6. Verification checklist (run before declaring done)

- [ ] `mkdocs build --strict` passes with no broken image links.
- [ ] Word-count spot check: `docs/05_Maps_GoogleColab.md` should be
      the longest generated file (source chapter 7 is ~950 lines) —
      if it is short, content was dropped; go back and re-copy in full.
- [ ] All 25 files in `assets/` are referenced by at least one `docs/*.md`
      file — grep for each filename to confirm none were skipped.
- [ ] Every `Table N:` and `Figure N.M:` caption from `docs_source/`
      appears somewhere in `docs/` (grep both directories and diff the
      caption lists).
- [ ] The Froehlich equations and the SCS-CN `Ia = 0.2S` equation render
      as LaTeX, not as plain text with `^` and `*`.
- [ ] The full `idf_gumbel_analysis.py` script (not a snippet) is
      visible on the rendered IDF page.
