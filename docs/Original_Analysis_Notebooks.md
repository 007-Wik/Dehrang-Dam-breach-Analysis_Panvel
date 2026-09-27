# Original Analysis Notebooks & Engineering Scripts

**Dehrang Dam Break Analysis — Panvel, Maharashtra**

* **Developer & Engineer:** Satwik Kamlakar Udupi, Agriculture Er.  
* **Institution:** Centre for Climate Change and Sustainability Studies (CCCSS), Shivaji University, Kolhapur  
* **Client / Authority:** Panvel Municipal Corporation (PMC), Government of Maharashtra  
* **Study Period:** May 2025  

---

## Sanitization & Security Assurance

> [!NOTE]
> **Data Security & Credential Hygiene:**  
> All analysis notebooks and Python scripts in this repository have been audited and sanitized:
> 
> 1. **No Hardcoded API Keys or Secrets:** All sensitive credentials, access tokens, and private keys have been completely removed.
> 2. **Generic Project Placeholders:** Cloud provider settings (such as Google Earth Engine) use standardized placeholders (`GEE_PROJECT = 'your-project-id'`).
> 3. **Clean Relative Paths:** Internal machine drive paths (e.g. local Windows drive letters) have been replaced with repository-relative path resolution (`os.path.join(repo_root, ...)`).
> 4. **Public & Scientific Repositories:** External geospatial layers utilize open-access scientific endpoints (ISRIC SoilGrids OGC WCS, ESA WorldCover, OpenTopography) without embedding proprietary credentials.

---

## 📓 Original Analysis Jupyter Notebooks

Below is the complete suite of original analysis notebooks used to perform the reservoir capacity calculations, geospatial basin pre-processing, watershed delineation, rainfall frequency analysis, and cartographic map generation.

```
docs/assets/notebooks/
├── 01_Storage_Elevation_Analysis.ipynb    (24.7 KB)
├── 02_DBA_Basin_HydroPrep.ipynb           (46.1 KB)
├── 03_DamBreak_Analysis.ipynb             (66.4 KB)
├── 04_IDF_Analysis_Panvel.ipynb           (30.1 KB)
└── 05_Maps_GoogleColab.ipynb              (6.3 MB)
```

---

### Notebook 01: Reservoir Storage-Elevation & Siltation Analysis

* **Filename:** `01_Storage_Elevation_Analysis.ipynb`  
* **Runtime:** Local Python / Jupyter or Google Colab  
* **Primary Inputs:** Pre-monsoon 2025 sludge survey spreadsheet (`SLUDGE_QNTY_10X10_DEHRANG_DAM.xlsx`, 3,193 survey boxes, 10×10 m grid)  
* **Key Libraries:** `pandas`, `numpy`, `matplotlib`, `scipy`  
* **Downloads:** [📥 Download Notebook (.ipynb)](assets/notebooks/01_Storage_Elevation_Analysis.ipynb) | [📥 Download Derived CSV](assets/tables/Dehrang_Storage_Elevation_Data.csv) | [📥 Download Derived Excel](assets/tables/Dehrang_Dam_Storage_Elevation_Table.xlsx)

#### Workflow & Implementation
1. **Survey Ingestion & Slicing:** Ingests 3,193 bathymetric survey cells and groups bed levels into 0.2 m elevation slices from 75.40 m MSL up to 89.20 m MSL.
2. **Surface Area Integration:** Calculates original (pre-siltation) and current (post-siltation) water spread area (ha) at each elevation.
3. **Trapezoidal Capacity Calculation:** Integrates storage volume between contour planes using $\Delta V = \frac{A_1 + A_2}{2} \Delta h$.
4. **Siltation Quantification:** Evaluates dead storage loss below MDDL (80.77 m MSL, 100% loss = $114.77 \times 10^3 \text{ m}^3$) and active storage loss up to FRL (89.15 m MSL, cumulative silt = $544.14 \times 10^3 \text{ m}^3$).
5. **Engineering Plotting:** Generates millimeter-accurate Elevation-Area and Elevation-Capacity engineering curves with watermark annotations.

---

### Notebook 02: Dam Break Basin — Hydrological Pre-Processing

* **Filename:** `02_DBA_Basin_HydroPrep.ipynb`  
* **Runtime:** Google Colab with GEE (Google Earth Engine) Integration  
* **Primary Inputs:** Catchment boundary shapefile (`Dehrang_DBA_Basin.shp`)  
* **Key Libraries:** `ee` (Earth Engine API), `rasterio`, `geopandas`, `requests`, `numpy`  
* **Downloads:** [📥 Download Notebook (.ipynb)](assets/notebooks/02_DBA_Basin_HydroPrep.ipynb)

#### Workflow & Implementation
1. **GEE Authentication & Cloud Export:** Initializes Earth Engine (`GEE_PROJECT = 'your-project-id'`) and clips ESA WorldCover 2021 (10 m) land cover to the basin extent.
2. **SoilGrids OGC WCS Retrieval:** Programmatically queries ISRIC SoilGrids v2 REST API to download clay, silt, and sand percentages for 0–5 cm, 5–15 cm, and 15–30 cm soil horizons at 250 m resolution.
3. **Hydrological Soil Group (HSG) Classification:** Assembles depth-weighted soil texture profiles and categorizes each cell into USDA HSG classes (A, B, C, D) using Indian adaptations (Mishra & Singh, 2003).
4. **SCS Curve Number (CN) Matrix:** Intersects the 10 m LULC raster with the HSG grid to assign AMC II Curve Numbers according to USDA TR-55 standards.
5. **Manning's Roughness Raster:** Translates land cover classes to overland surface roughness coefficients ($n$) based on Chow (1959) and CWPRS standards.

---

### Notebook 03: Watershed Delineation & Multi-Pour-Point Characterisation

* **Filename:** `03_DamBreak_Analysis.ipynb`  
* **Runtime:** Local Workstation / Conda / Colab  
* **Primary Inputs:** Copernicus DEM 30 m & SRTM 30 m tiles, Pour point coordinates (Dam axis: PP1, Confluence: PP2)  
* **Key Libraries:** `pysheds`, `rasterio`, `geopandas`, `folium`, `shapely`  
* **Downloads:** [📥 Download Notebook (.ipynb)](assets/notebooks/03_DamBreak_Analysis.ipynb)

#### Workflow & Implementation
1. **DEM Conditioning:** Ingests COP30 and SRTM tiles, performs depression filling, flat area routing, and flow direction calculation using the D8 algorithm.
2. **Stream Network & Pour Point Snapping:** Computes flow accumulation, extracts stream raster lines, and snaps field coordinates of the dam axis and downstream confluence to high-accumulation channels.
3. **Catchment Delineation:** Extracts high-precision boundary polygons for the upstream Dehrang reservoir catchment ($19.2 \text{ km}^2$) and downstream flood reach.
4. **Zonal Statistical Extraction:** Calculates mean Curve Number, slope, elevation, and land cover percentages across both delineations.
5. **Interactive Folium Web Map:** Produces a self-contained leaflet web map (`dehrang_interactive_map.html`) displaying boundary shapefiles, stream networks, and dam axes.

---

### Notebook 04: Panvel IMD Rainfall Frequency & Design Storm Analysis

* **Filename:** `04_IDF_Analysis_Panvel.ipynb`  
* **Runtime:** Local Jupyter / Colab  
* **Primary Inputs:** IMD Panvel Raingauge daily series (1992–2024, $N=31$ years)  
* **Key Libraries:** `pandas`, `scipy.stats`, `numpy`, `matplotlib`  
* **Downloads:** [📥 Download Notebook (.ipynb)](assets/notebooks/04_IDF_Analysis_Panvel.ipynb) | [📥 Download Complete IDF Workbook (Excel)](assets/tables/IDF_Design_Flood_Panvel_CORRECTED.xlsx)

#### Workflow & Implementation
1. **Rainfall Record Verification:** Loads 31 annual maximum daily rainfall observations; validates data completeness (identifying missing years 1997 and 2006).
2. **Grubbs Outlier Screening:** Identifies the historic 26 July 2005 storm (473.5 mm) as a statistical outlier ($G = 3.46 > G_{\text{crit}} = 2.93$), evaluating both retained and excluded sensitivity. Per CWC dam safety guidelines, the outlier is retained.
3. **Extreme Value Fitting:** Fits Gumbel EV-I via Chow's method using interpolated sample coefficients ($y_n = 0.53702, S_n = 1.11562$) and fits Lognormal distribution as a comparative check.
4. **Goodness-of-Fit Testing:** Executes Kolmogorov-Smirnov ($D$) tests confirming statistical validity ($D = 0.0722 < D_{\text{crit}} = 0.2443$).
5. **IDF Matrix & ABM Hyetograph:** Applies the IMD empirical reduction equation $P_t = P_{24} (t/24)^{1/3}$ to generate sub-daily intensities (15 min to 24 hr) and computes the 24-hr Alternating Block Method (ABM) temporal distribution.

---

### Notebook 05: Professional Cartographic Map Suite

* **Filename:** `05_Maps_GoogleColab.ipynb`  
* **Runtime:** Google Colab with High-RAM  
* **Primary Inputs:** Clipped GeoTIFF rasters (DEM, LULC, HSG, CN, Manning's $n$)  
* **Key Libraries:** `cartopy`, `matplotlib`, `rasterio`, `matplotlib_scalebar`  
* **Downloads:** [📥 Download Notebook (.ipynb)](assets/notebooks/05_Maps_GoogleColab.ipynb)

#### Cartographic Outputs (300 DPI)
* **Map 1:** Copernicus 30 m DEM elevation contours with hillshade relief.
* **Map 2:** ESA WorldCover 2021 10 m LULC thematic distribution.
* **Map 3:** Hydrological Soil Groups (HSG A, B, C, D) spatial distribution.
* **Map 4:** SCS AMC II Curve Number (CN) composite raster.
* **Map 5:** Manning's roughness coefficient ($n$) spatial distribution.

---

## 🐍 Standalone Python Scripts

In addition to Jupyter Notebooks, two modular Python scripts are provided in the repository's `scripts/` directory:

| Script File | Purpose | Key Output | Direct Download |
|---|---|---|---|
| `scripts/idf_gumbel_analysis.py` | Reference standalone Python implementation of Gumbel EV-I, Lognormal, K-S test, IDF table, and ABM hyetograph | Terminal summary of design rainfalls & sub-daily IDF matrix | [📥 Download idf_gumbel_analysis.py](assets/scripts/idf_gumbel_analysis.py) |
| `scripts/generate_map.py` | Standalone Folium script generating interactive multi-layer Leaflet GIS maps from shapefiles | `docs/map_overview.html` | [📥 Download generate_map.py](assets/scripts/generate_map.py) |

### 1. `scripts/idf_gumbel_analysis.py`

This script can be executed directly without Jupyter:

```bash
python scripts/idf_gumbel_analysis.py
```

```python
"""
Reference implementation of the IDF / Design-Storm methodology described in
Chapter 3 of the Dehrang Dam Dam-Break Analysis report.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy import stats

def gumbel_ev1_frequency_analysis(series: list[float], return_periods: list[int]):
    x = np.asarray(series, dtype=float)
    n = len(x)
    x_bar = x.mean()
    s = x.std(ddof=1)
    yn, sn = 0.5370, 1.1156  # N=31
    design_values = {}
    for t in return_periods:
        y_t = -math.log(math.log(t / (t - 1)))
        k = (y_t - yn) / sn
        design_values[t] = x_bar + k * s
    return design_values
```

### 2. `scripts/generate_map.py`

Generates an interactive web map using GeoPandas and Folium, resolved relative to repository directories:

```python
import folium
import geopandas as gpd
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path = os.path.join(repo_root, "data", "processed")

shapefiles = {
    "Basin": os.path.join(base_path, "BasinSHP", "Dehrang_DBA_Basin.shp"),
    "Damwall": os.path.join(base_path, "Damwall", "Damwall.shp"),
    "River Centerline": os.path.join(base_path, "RIver line & Buffer", "Rivercentreline .shp"),
    "River Buffer 50m": os.path.join(base_path, "RIver line & Buffer", "Riverline_Buffer_50m.shp"),
    "Reservoir Submergence": os.path.join(base_path, "Submergence", "Reservoir_Submergence_Dehrang.shp")
}
```

---

## 🛠️ Reproduction & Execution Guide

To run the notebooks locally on your machine:

```bash
# Clone the repository
git clone https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel.git
cd Dehrang-Dam-breach-Analysis_Panvel

# Create virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Lab / Notebook
jupyter lab
```
