<!--  ═══════════════════════════════════════════════════════════════════════
      DEHRANG DAM — HYDROLOGICAL & DAM BREAK ANALYSIS
      ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

```
██████╗ ███████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗ ██████╗
██╔══██╗██╔════╝██║  ██║██╔══██╗██╔══██╗████╗  ██║██╔════╝
██║  ██║█████╗  ███████║██████╔╝███████║██╔██╗ ██║██║  ███╗
██║  ██║██╔══╝  ██╔══██║██╔══██╗██╔══██║██║╚██╗██║██║   ██║
██████╔╝███████╗██║  ██║██║  ██║██║  ██║██║ ╚████║╚██████╔╝
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝
         DAM  ·  HYDROLOGICAL & DAM BREAK ANALYSIS
```

**Dehrang Dam, Raigad District, Maharashtra, India**
*Earthen Dam · Client: Panvel Municipal Corporation · Commissioned 1957*

* **Developer & Engineer:** **Satwik Kamlakar Udupi, Agriculture Er.**
* **Institution:** **Centre for Climate Change and Sustainability Studies (CCCSS), Shivaji University, Kolhapur**
* **Client / Authority:** **Panvel Municipal Corporation, Government of Maharashtra**

---

[![Documentation](https://img.shields.io/badge/Docs-Live%20Portal-blue?style=flat-square&logo=materialformkdocs)](https://007-wik.github.io/Dehrang-Dam-breach-Analysis_Panvel/)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-Ready-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)
![GEE](https://img.shields.io/badge/Google%20Earth%20Engine-Integrated-4285F4?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 🌊 Project Overview

This repository contains a complete, end-to-end hydrological analysis pipeline for **Dehrang Dam** — a minor earthen dam with an automatic gated spillway located in Raigad District, Maharashtra (19°1′54″N, 73°14′32″E), owned and operated by the **Panvel Municipal Corporation**.

The study was conducted in accordance with **IS 11223**, **CDSO GUD DS-06 v1.0 (June 2021)**, and **CWC Manual on Flood Estimation (1989)**, covering:

| Theme | Coverage |
|---|---|
| 🏗️ Reservoir Engineering | Storage-Elevation analysis from 10×10 m sludge survey (3,193 boxes) |
| 🌧️ Design Hydrology | Gumbel EV-I IDF analysis, Panvel raingauge (1992–2024, N=31 years) |
| 🗺️ Basin Characterisation | ESA WorldCover LULC, ISRIC SoilGrids, SCS-CN, Manning's n |
| 💧 Watershed Delineation | COP30 + SRTM DEMs, D8 routing with pysheds, two pour points |
| 📐 Dam Break Pre-processing | CN Grid, HSG Grid, Manning's roughness rasters, zonal statistics |
| 🖼️ Professional Maps | Five publication-quality cartographic outputs at 300 DPI |

---

## 📁 Repository Structure

```
dehrang-dam-analysis/
│
├── 📓 notebooks/                         ← All Jupyter notebooks (run in order)
│   ├── 01_Storage_Elevation_Analysis.ipynb
│   ├── 02_DBA_Basin_HydroPrep.ipynb
│   ├── 03_DamBreak_Analysis.ipynb
│   ├── 04_IDF_Analysis.ipynb
│   └── 05_Maps_GoogleColab.ipynb
│
├── 📂 data/
│   ├── raw/                              ← Place your input files here (see data/README.md)
│   └── processed/                        ← Auto-populated by the notebooks
│
├── 📂 outputs/                           ← All generated artefacts
│   ├── figures/                          ← Engineering plots (PNG, 150–300 DPI)
│   ├── maps/                             ← Cartographic map exports (PNG, 300 DPI)
│   ├── Reports                           ← Reports
│   └── tables/                           ← CSV tables (Storage-Elevation, IDF, etc.)
│
├── 📂 docs/
│   └── methodology.md                    ← Detailed methodology & references
│
├── requirements.txt                      ← pip-installable dependencies
├── environment.yml                       ← conda environment (recommended)
├── .gitignore
└── LICENSE
```

---

## 📓 Notebooks — What Each Does and What You Get

### `01_Storage_Elevation_Analysis.ipynb`
**🏗️ Reservoir Storage-Elevation (Capacity Curve) Analysis**

**What it does:**
Reads the raw sludge survey spreadsheet (`SLUDGE_QNTY_10X10_DEHRANG_DAM.xlsx`) collected using the 10×10 m box method (3,193 survey boxes, Pre-monsoon 2025, Yash Engineering Consultant Pvt. Ltd.). It bins survey data into 0.2 m elevation intervals, computes water-spread area at each level for both pre-siltation (original) and post-siltation (current) conditions, then integrates volume using the **trapezoidal method** across the full elevation range from the lowest river bed (75.40 m MSL) to FRL/MWL (89.15 m MSL). Areas above the survey limit are extrapolated using a 2nd-order polynomial fit.

**Key parameters used:**

| Level | Elevation (m MSL) |
|---|---|
| Full Reservoir Level (FRL/MWL) | 89.15 |
| Minimum Draw Down Level (MDDL) | 80.77 |
| Spillway Crest | 86.65 |
| Lowest River Bed | 75.40 |
| Total Silt Volume | 517,705.69 m³ |

**What you get:**
- `Dehrang_Dam_Storage_Elevation.csv` — Complete storage-elevation table with columns: Elevation, Original/Current Area (ha), Incremental Volume, Cumulative Capacity (×1,000 m³), Capacity Loss (absolute + %), and Key Level flags
- `Dehrang_Area_Elevation_Curve.png` — Engineering-grade water spread area vs. elevation plot with graph-paper background, key level annotations, siltation shading
- `Dehrang_Capacity_Elevation_Curve.png` — Cumulative storage capacity vs. elevation, pre/post siltation comparison
- `Dehrang_Combined_Engineering_Sheet.png` — Side-by-side combined engineering sheet (area + capacity), suitable for inspection reports

---

### `02_DBA_Basin_HydroPrep.ipynb`
**🌊 Dam Break Analysis Basin — Hydrological Pre-Processing**

**What it does:**
Prepares all hydrological raster layers required as inputs to a dam break hydraulic model. The notebook operates in **Google Colab** with Google Drive integration and Google Earth Engine (GEE). It downloads ESA WorldCover 2021 (10 m resolution) via the GEE batch export API, clips it to the Dehrang DBA Basin shapefile boundary, and downloads ISRIC SoilGrids v2 clay/sand/silt textures (0–5 cm, 5–15 cm, 15–30 cm depth slices) at 250 m via the OGC WCS 2.0 REST API. It then assembles a depth-weighted composite (0–30 cm profile weights: 5/30, 10/30, 15/30) and classifies each pixel into a **Hydrological Soil Group (HSG A/B/C/D)** using the USDA textural triangle, per Mishra & Singh (2003) adaptations for Indian conditions. Each LULC class is cross-referenced with its HSG to derive a **Curve Number (CN)** grid (AMC II, NRCS TR-55) and a **Manning's roughness (n)** grid using values from Chow (1959), CWPRS (2018), and Arora et al. (2021).

**Data sources:**
- ESA WorldCover v200 2021 (10 m) via Google Earth Engine
- ISRIC SoilGrids v2 (250 m) via WCS REST API — no authentication required
- SCS-CN values adapted from USDA TR-55 / Mishra & Singh (2003)
- Manning's n from Chow (1959), CWPRS (2018), Arora et al. (2021)

**What you get:**
- `ESA_WorldCover_2021.tif` — Land use / land cover raster clipped to basin (10 m, EPSG:4326)
- `HSG_Grid.tif` — Hydrological soil group classification raster (A/B/C/D, values 1–4)
- `CN_Grid.tif` — SCS Curve Number raster (AMC II conditions)
- `Mannings_n_Grid.tif` — Manning's roughness coefficient raster
- `LULC_Stats.csv` — Area statistics per land cover class (ha, %)
- `SoilGrids/` — Raw clay/sand/silt GeoTIFFs per depth interval
- `00_AOI.png` — Basin boundary location map

---

### `03_DamBreak_Analysis.ipynb`
**🏞️ Dam Break Analysis — Full Watershed Delineation & Characterisation**

**What it does:**
A standalone, locally-runnable notebook (no GEE required for core workflow) that performs complete hydrological characterisation for dam break modelling across **two pour points**:

| Pour Point | Purpose | Lat | Lon |
|---|---|---|---|
| PP1 | Dehrang Dam Catchment | 19°2′1.71″N | 73°14′31.07″E |
| PP2 | River Basin Confluence | 19°1′13.73″N | 73°9′36.06″E |

It extracts local COP30 and SRTM DEM tiles from `.tar.gz` archives, mosaics multi-tile downloads, fills pits and depressions, resolves flat areas, computes D8 flow direction and accumulation, snaps pour points to the nearest stream (above a configurable accumulation threshold), and delineates catchment polygons using `pysheds`. LULC is obtained from ESA WorldCover via GEE or STAC API; HSG from SoilGrids REST; CN and Manning's n grids are assembled identically to notebook `02`. Zonal statistics are computed per watershed polygon. A `folium` interactive HTML map is produced showing both watersheds, streams, pour points, and all raster overlays.

**What you get:**
- `PP1_watershed.shp` / `.geojson` — Dehrang Dam catchment polygon
- `PP2_watershed.shp` / `.geojson` — River confluence basin polygon
- `cop30_mosaic.tif` / `srtm_mosaic.tif` — Mosaicked DEM tiles
- `dem_preview.png` — Side-by-side DEM preview (COP30 vs SRTM)
- `CN_Grid_*.tif`, `HSG_Grid_*.tif`, `Mannings_n_Grid_*.tif` — Per-watershed rasters
- `Zonal_Stats_PP1.csv` / `Zonal_Stats_PP2.csv` — Mean CN, HSG distribution, mean Manning's n per watershed
- `dehrang_interactive_map.html` — Folium interactive map (open in any browser)

---

### `04_IDF_Analysis.ipynb`
**🌧️ Intensity-Duration-Frequency (IDF) Analysis — Panvel Raingauge**

**What it does:**
Performs a complete design storm derivation for dam break analysis using **31 years** (1992–2024, excluding 1997 and 2006) of IMD annual maximum 24-hour rainfall from Panvel Station [102187319] (18.9833°N, 73.1167°E). The workflow follows CWC Manual on Flood Estimation (1989) and CDSO GUD DS-06 v1.0 for a **Minor Dam (100-year return period)** design standard (IS 11223). The notebook fits a **Gumbel Extreme Value Type-I (EV-I)** distribution using Gumbel (1958) reduced variate tables interpolated for N=31, performs a Grubbs two-sided outlier test (the 2005 Mumbai flood event, 473.5 mm, is flagged but retained per CWC practice), cross-checks against Lognormal distribution, validates fit with Kolmogorov-Smirnov and Chi-square goodness-of-fit tests, and runs a sensitivity analysis with/without the 2005 outlier. Sub-daily rainfall depths are disaggregated from the 24-hour design value using the **IMD Empirical Reduction Formula** (Pt = P24 × (t/24)^⅓). The **Alternating Block Method (ABM)** is applied to derive a hyetograph for hydraulic modelling.

**Design parameters derived:**
- 100-yr 24-hr design rainfall (Gumbel EV-I)
- 95% confidence limits (Chow 1951)
- IDF table: durations 15 min → 24 hr, return periods 2 → 1,000 years
- ABM hyetograph for 100-yr, 6-hr storm

**What you get:**
- `IDF_Table_Depth_mm.csv` — Rainfall depth (mm) for all duration × return period combinations
- `IDF_Table_Intensity_mmhr.csv` — Rainfall intensity (mm/hr)
- `ABM_Hyetograph_100yr.csv` — Alternating block hyetograph (time-step rainfall depths)
- `Gumbel_Frequency_Plot.png` — Gumbel probability paper plot with fitted line and 95% CI band
- `IDF_Curves.png` — Full IDF curves (intensity vs. duration, colour-coded by return period)
- `ABM_Hyetograph.png` — Design storm hyetograph bar chart

---

### `05_Maps_GoogleColab.ipynb`
**🗺️ Professional Cartographic Map Suite (Google Colab)**

**What it does:**
Produces five publication-quality cartographic maps at **300 DPI** using `cartopy` for geographic projection, `matplotlib_scalebar` for scale bars, and a shared hillshade background derived from the Copernicus DEM 30 m. Each map uses consistent styling — DejaVu Serif font, DMS grid with formatted tick labels, north arrow, scale bar, and a buffered map extent — and exports as a standalone high-resolution PNG. The notebook is designed for Google Colab: users upload their 5 GeoTIFF rasters at runtime and download the output maps as a ZIP.

**Maps produced:**

| # | File | Layer | Visualisation |
|---|---|---|---|
| 1 | `01_DEM_Copernicus.png` | Copernicus DEM 30 m | Terrain colormap over hillshade, elevation colorbar |
| 2 | `02_LULC_ESA_WorldCover.png` | ESA WorldCover 2021 LULC | Categorical colour scheme per class, legend patch |
| 3 | `03_CN_Grid.png` | SCS Curve Number Grid | Diverging green→red colormap, CN colorbar |
| 4 | `04_HSG_Grid.png` | Hydrological Soil Group | Categorical A/B/C/D colours, legend patch |
| 5 | `05_Mannings_n_Grid.png` | Manning's Roughness n | Blue gradient colormap, n colorbar |

All maps share the hillshade base, UTM projection (auto-detected from input EPSG), gridlines at 0.1° intervals with degree symbols, and a configurable watershed/basin title.

**What you get:**
- Five 300-DPI PNG maps ready for report inclusion or publication
- `DA_Maps.zip` — All maps bundled for download from Colab

---

## 🔄 Recommended Workflow

```
Data Acquisition
      │
      ├─► [01] Storage_Elevation_Analysis   ← sludge survey XLSX → capacity curves + CSV
      │
      ├─► [02] DBA_Basin_HydroPrep          ← shapefile → LULC / HSG / CN / Manning rasters
      │         │
      │         └─────────────────────────────────────────┐
      ├─► [03] DamBreak_Analysis            ← DEMs + rasters → watershed polygons + stats
      │
      ├─► [04] IDF_Analysis                 ← rainfall record → design storm + IDF curves
      │
      └─► [05] Maps_GoogleColab             ← rasters → 5 publication maps
```

---

## ⚙️ Setup & Installation

### Option A — conda (recommended)

```bash
conda env create -f environment.yml
conda activate dehrang-dam
jupyter notebook
```

### Option B — pip

```bash
pip install -r requirements.txt
jupyter notebook
```

### Option C — Google Colab

All notebooks are Colab-compatible. Upload each `.ipynb` to [colab.research.google.com](https://colab.research.google.com), mount your Google Drive, and follow the in-notebook instructions. GEE authentication is required for notebooks `02`, `03`, and `05`.

---

## 📦 Data Requirements

See [`data/README.md`](data/README.md) for full instructions. Key inputs:

| File | Used by | Source |
|---|---|---|
| `SLUDGE_QNTY_10X10_DEHRANG_DAM.xlsx` | Notebook 01 | Yash Engineering Consultant (Inspection Report 2025) |
| `Dehrang_DBA_Basin.*` (shapefile set) | Notebook 02 | Survey / GIS department |
| `rasters_COP30.tar.gz` | Notebook 03 | [Copernicus DEM via OpenTopography](https://portal.opentopography.org/) |
| `rasters_SRTMGL1.tar.gz` | Notebook 03 | [SRTM via OpenTopography](https://portal.opentopography.org/) |
| Annual max rainfall CSV | Notebook 04 | IMD Daily Rainfall — Panvel Station [102187319] |
| 5 × GeoTIFF rasters | Notebook 05 | Outputs of Notebooks 02 / 03 |

---

## 📚 References

| Reference | Used in |
|---|---|
| CWC Manual on Flood Estimation (1989) | Notebooks 03, 04 |
| IS 11223 — Guidelines for Fixing Spillway Capacity | Notebook 04 |
| CDSO GUD DS-06 v1.0, June 2021 | Notebook 04 |
| Gumbel, E.J. (1958) — *Statistics of Extremes* | Notebook 04 |
| Chow, V.T. (1951) — Frequency analysis of hydrologic data | Notebook 04 |
| Chow, V.T. (1959) — *Open Channel Hydraulics* | Notebooks 02, 03 |
| USDA NRCS TR-55 / NEH-630 | Notebooks 02, 03 |
| Mishra, S.K. & Singh, V.P. (2003) — *Soil Conservation Service CN Methodology* | Notebooks 02, 03 |
| CWPRS (2018) | Notebooks 02, 03 |
| Arora et al. (2021) | Notebooks 02, 03 |
| ESA WorldCover v200 2021 (10 m) | Notebooks 02, 03, 05 |
| ISRIC SoilGrids v2 (250 m) | Notebooks 02, 03 |

---

## 📄 License

This project is released under the [MIT License](LICENSE). Data files sourced from IMD, ISRIC, ESA, and Copernicus are subject to their respective terms of use.

---

<div align="center">
<sub>Dehrang Dam · Raigad District, Maharashtra, India · 19°1′54″N 73°14′32″E</sub>
</div>
