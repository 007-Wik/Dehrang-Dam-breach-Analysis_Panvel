# Derived Output Tables & Engineering Datasets

**Dehrang Dam Break Analysis — Panvel, Maharashtra**

* **Developer & Engineer:** Satwik Kamlakar Udupi, Agriculture Er.  
* **Institution:** Centre for Climate Change and Sustainability Studies (CCCSS), Shivaji University, Kolhapur  
* **Client / Authority:** Panvel Municipal Corporation (PMC), Government of Maharashtra  
* **Project Period:** May 2025  

---

## Overview

This section provides direct viewing, documentation, and download access to the primary engineered datasets derived during the hydrological and hydraulic assessment of Dehrang Dam. All workbooks and CSV files have been calculated in compliance with **IS 11223**, **CDSO GUD DS-06 v1.0 (June 2021)**, and **CWC Flood Estimation Guidelines (1989)**.

| Dataset / Workbook | Format | Size | Description | Direct Download |
|---|---|---|---|---|
| **Dehrang Dam Storage-Elevation Table** | `.xlsx` | 16.5 KB | Survey-derived elevation, water spread area, cumulative storage capacity, and siltation capacity loss | [📥 Download Excel (XLSX)](assets/tables/Dehrang_Dam_Storage_Elevation_Table.xlsx) |
| **Dehrang Storage-Elevation Data** | `.csv` | 2.5 KB | 55 elevation intervals (78.4 to 89.2 m MSL) with original/current area, capacity, and % capacity loss | [📥 Download CSV](assets/tables/Dehrang_Storage_Elevation_Data.csv) |
| **Panvel IDF & Design Flood Workbook (Corrected)** | `.xlsx` | 153.7 KB | Complete 9-sheet hydrological frequency model: 31-yr IMD records, Gumbel EV-I, Lognormal, Grubbs outlier check, K-S GoF test, sub-daily IDF matrix, and 100-yr design storm | [📥 Download Excel (XLSX)](assets/tables/IDF_Design_Flood_Panvel_CORRECTED.xlsx) |
| **Panvel IDF Initial Calculation Sheet** | `.xlsx` | 40.2 KB | Initial baseline calculation workbook for Panvel raingauge frequency analysis | [📥 Download Excel (XLSX)](assets/tables/IDF_Design_Flood_Panvel.xlsx) |

---

## 1. Reservoir Storage-Elevation & Siltation Analysis

### 1.1 Methodology & Derivation
The reservoir storage-elevation table was derived from the pre-monsoon 2025 bathymetric/sludge survey conducted using the **10×10 m box method** (3,193 survey boxes). Incremental storage volumes were computed at 0.2 m elevation slices using the **trapezoidal integration formula**:

$$\Delta V = \frac{A_1 + A_2}{2} \times \Delta h$$

Where:
* $A_1, A_2$ are water-spread areas at successive 0.2 m elevations.
* $\Delta h = 0.2 \text{ m}$.
* Total cumulative capacity is accumulated from the lowest surveyed bed level up to the Maximum Water Level (MWL / FRL = 89.15 m MSL).

### 1.2 Key Reservoir Salient Elevations

| Salient Level | Elevation (m MSL) | Original Capacity ($10^3 \text{ m}^3$) | Current Capacity ($10^3 \text{ m}^3$) | Silt Loss ($10^3 \text{ m}^3$) | Net Storage Retention |
|---|---|---|---|---|---|
| **Lowest River Bed** | 75.40 m | 0.00 | 0.00 | 0.00 | 100.0% |
| **Survey Zero-Datum** | 78.40 m | 0.00 | 0.00 | 0.00 | 100.0% |
| **Minimum Drawdown Level (MDDL)** | 80.77 m | 114.77 | 0.00 | 114.77 | Dead storage completely silted (100% loss) |
| **Spillway Crest Level** | 86.65 m | 1,518.23 | 974.09 | 544.14 | 64.2% retained |
| **Full Reservoir Level (FRL / MWL)** | 89.15 m | 2,836.00 | 2,291.86 | 544.14 | 80.8% retained |

### 1.3 Complete Storage-Elevation Data Preview

The table below reproduces the derived storage-elevation schedule across 0.2 m increments:

| Elevation (m MSL) | Original Area (ha) | Original Capacity ($10^3 \text{ m}^3$) | Current Area (ha) | Current Capacity ($10^3 \text{ m}^3$) | Silt Loss ($10^3 \text{ m}^3$) | Capacity Loss (%) | Notes / Key Benchmarks |
|---|---|---|---|---|---|---|---|
| 78.40 | 0.000 | 0.00 | 0.000 | 0.00 | 0.00 | 0.0% | Bed Level Datum |
| 78.60 | 0.050 | 0.05 | 0.000 | 0.00 | 0.05 | 100.0% | Silted dead pool |
| 78.80 | 1.600 | 1.70 | 0.000 | 0.00 | 1.70 | 100.0% | Silted dead pool |
| 79.00 | 2.680 | 5.98 | 0.000 | 0.00 | 5.98 | 100.0% | Silted dead pool |
| 79.20 | 3.420 | 12.08 | 0.000 | 0.00 | 12.08 | 100.0% | Silted dead pool |
| 79.40 | 4.050 | 19.55 | 0.000 | 0.00 | 19.55 | 100.0% | Silted dead pool |
| 79.60 | 4.780 | 28.38 | 0.000 | 0.00 | 28.38 | 100.0% | Silted dead pool |
| 79.80 | 5.320 | 38.48 | 0.000 | 0.00 | 38.48 | 100.0% | Silted dead pool |
| 80.00 | 6.110 | 49.91 | 0.000 | 0.00 | 49.91 | 100.0% | Silted dead pool |
| 80.20 | 6.830 | 62.85 | 0.000 | 0.00 | 62.85 | 100.0% | Silted dead pool |
| 80.40 | 7.420 | 77.10 | 0.000 | 0.00 | 77.10 | 100.0% | Silted dead pool |
| 80.60 | 8.230 | 92.75 | 0.000 | 0.00 | 92.75 | 100.0% | Silted dead pool |
| **80.77** | **9.010** | **114.77** | **0.000** | **0.00** | **114.77** | **100.0%** | **MDDL (Minimum Drawdown Level)** |
| 81.00 | 9.940 | 129.21 | 2.500 | 14.44 | 114.77 | 88.8% | Active live storage begins |
| 81.20 | 10.740 | 149.89 | 4.880 | 35.12 | 114.77 | 76.6% | Active storage |
| 81.40 | 11.600 | 172.23 | 6.940 | 57.46 | 114.77 | 66.6% | Active storage |
| 81.60 | 12.560 | 196.39 | 8.870 | 81.62 | 114.77 | 58.4% | Active storage |
| 81.80 | 13.510 | 222.46 | 10.710 | 107.69 | 114.77 | 51.6% | Active storage |
| 82.00 | 14.520 | 250.49 | 12.380 | 135.72 | 114.77 | 45.8% | Active storage |
| 82.50 | 17.150 | 329.66 | 16.500 | 214.89 | 114.77 | 34.8% | Active storage |
| 83.00 | 20.300 | 423.29 | 19.800 | 308.52 | 114.77 | 27.1% | Active storage |
| 83.50 | 23.400 | 532.54 | 22.950 | 417.77 | 114.77 | 21.6% | Active storage |
| 84.00 | 26.650 | 657.66 | 26.200 | 542.89 | 114.77 | 17.5% | Active storage |
| 84.50 | 30.150 | 799.66 | 29.750 | 684.89 | 114.77 | 14.4% | Active storage |
| 85.00 | 33.700 | 959.29 | 33.300 | 844.52 | 114.77 | 12.0% | Active storage |
| 85.50 | 37.400 | 1,137.04 | 37.000 | 1,022.27 | 114.77 | 10.1% | Active storage |
| 86.00 | 41.200 | 1,333.54 | 40.800 | 1,218.77 | 114.77 | 8.6% | Active storage |
| **86.65** | **44.820** | **1,518.23** | **44.420** | **974.09** | **544.14** | **35.8%** | **Spillway Crest Level** |
| 87.00 | 46.060 | 1,770.83 | 45.660 | 1,226.69 | 544.14 | 30.7% | Gated pool |
| 87.50 | 47.720 | 2,005.28 | 47.320 | 1,461.14 | 544.14 | 27.1% | Gated pool |
| 88.00 | 50.491 | 2,250.81 | 50.091 | 1,706.67 | 544.14 | 24.2% | Gated pool |
| 88.50 | 53.220 | 2,510.08 | 52.820 | 1,965.94 | 544.14 | 21.7% | Gated pool |
| 89.00 | 55.928 | 2,782.95 | 55.528 | 2,238.81 | 544.14 | 19.6% | Near FRL |
| **89.15** | **56.732** | **2,836.00** | **56.332** | **2,291.86** | **544.14** | **19.2%** | **Full Reservoir Level (FRL / MWL)** |
| 89.20 | 57.000 | 2,895.83 | 56.600 | 2,351.69 | 544.14 | 18.8% | Maximum surveyed level |

---

## 2. Panvel Rainfall Frequency Analysis & IDF Workbook

The derived workbook `IDF_Design_Flood_Panvel_CORRECTED.xlsx` contains 9 interconnected calculation sheets. Below are the key engineering summaries.

### 2.1 Frequency Analysis Summary & Statistical Indicators

* **Station:** Panvel [ID: 102187319], Lat: 18.9833°N, Lon: 73.1167°E
* **Record Period:** 1992–2024 ($N = 31$ valid years; 1997 & 2006 excluded due to missing records)
* **Mean Annual Maximum 24-hr Rainfall ($\bar{X}$):** $225.06 \text{ mm}$
* **Standard Deviation ($S$):** $71.84 \text{ mm}$
* **Coefficient of Variation ($C_v$):** $0.319$
* **Skewness Coefficient ($C_s$):** $1.357$
* **Gumbel Reduced Mean ($y_n$, $N=31$):** $0.53702$
* **Gumbel Reduced Std Dev ($S_n$, $N=31$):** $1.11562$

### 2.2 Goodness-of-Fit & Quality Assurance Checks

| Statistical Check | Test Type | Computed Value | Critical Value ($\alpha = 0.05$) | Evaluation / Verdict |
|---|---|---|---|---|
| **Gumbel EV-I Fit** | Kolmogorov-Smirnov ($D$) | $D = 0.0722$ | $D_{\text{crit}} = 0.2443$ | **PASS ✓** Excellent fit to extreme rainfall series |
| **Lognormal Fit** | Kolmogorov-Smirnov ($D$) | $D = 0.0695$ | $D_{\text{crit}} = 0.2443$ | **PASS ✓** Valid alternative distribution |
| **Outlier Detection** | Grubbs Two-Sided Test ($G$) | $G = 3.46$ (Year 2005: 473.5 mm) | $G_{\text{crit}} = 2.93$ | **Outlier Confirmed ⚠** Retained per CWC guidelines |
| **Sensitivity Impact** | Excluding 2005 Extreme | 100-yr $P_{24} = 421.51 \text{ mm}$ | Baseline: $486.72 \text{ mm}$ | Difference = $65.21 \text{ mm}$ (retained value is conservative) |

### 2.3 100-Year Design Rainfall Depth Comparison

| Distribution | 100-Year 24-hr Rainfall ($P_{24}$) | 95% Confidence Interval | Engineering Adoption |
|---|---|---|---|
| **Gumbel EV-I (Chow 1951)** | **486.72 mm** | **[386.04 mm, 587.40 mm]** | **ADOPTED AS DESIGN BASIS** (Mandated by CWC & IS 11223) |
| **Lognormal Distribution** | 430.95 mm | [352.10 mm, 527.45 mm] | Used as secondary cross-check |

---

## 3. Sub-Daily Intensity-Duration-Frequency (IDF) Matrix

Using the authoritative **IMD Empirical Short-Duration Reduction Formula**:

$$P_t = P_{24} \times \left(\frac{t}{24}\right)^{1/3}$$

Where $t$ is duration in hours, $P_{24}$ is the 24-hr rainfall depth for the given return period, and $P_t$ is the corresponding sub-daily depth in mm.

### 3.1 Design Rainfall Depth $P_t$ (mm)

| Duration | $T = 2 \text{ yr}$ | $T = 5 \text{ yr}$ | $T = 10 \text{ yr}$ | $T = 25 \text{ yr}$ | $T = 50 \text{ yr}$ | $T = 100 \text{ yr}$ (Design) | $T = 200 \text{ yr}$ | $T = 1000 \text{ yr}$ |
|---|---|---|---|---|---|---|---|---|
| **15 min** (0.25 hr) | 46.75 | 62.70 | 73.25 | 86.58 | 96.48 | **106.30** | 116.08 | 138.75 |
| **30 min** (0.50 hr) | 58.91 | 78.99 | 92.29 | 109.09 | 121.55 | **133.93** | 146.25 | 174.81 |
| **1 hr** (1.00 hr) | 74.22 | 99.52 | 116.28 | 137.44 | 153.15 | **168.74** | 184.27 | 220.24 |
| **2 hr** (2.00 hr) | 93.51 | 125.39 | 146.50 | 173.17 | 192.96 | **212.59** | 232.16 | 277.49 |
| **3 hr** (3.00 hr) | 107.04 | 143.54 | 167.70 | 198.23 | 220.88 | **243.36** | 265.76 | 317.65 |
| **6 hr** (6.00 hr) | 134.86 | 180.84 | 211.29 | 249.75 | 278.29 | **306.61** | 334.84 | 400.21 |
| **12 hr** (12.00 hr) | 169.92 | 227.85 | 266.21 | 314.67 | 350.62 | **386.31** | 421.87 | 504.23 |
| **24 hr** (24.00 hr) | 214.08 | 287.07 | 335.40 | 396.46 | 441.76 | **486.72** | 531.52 | 635.29 |

### 3.2 Design Rainfall Intensity $I_t$ (mm/hr)

$$\text{Intensity } I_t = \frac{P_t}{t}$$

| Duration | $T = 2 \text{ yr}$ | $T = 5 \text{ yr}$ | $T = 10 \text{ yr}$ | $T = 25 \text{ yr}$ | $T = 50 \text{ yr}$ | $T = 100 \text{ yr}$ (Design) | $T = 200 \text{ yr}$ | $T = 1000 \text{ yr}$ |
|---|---|---|---|---|---|---|---|---|
| **15 min** | 186.99 | 250.79 | 293.02 | 346.33 | 385.90 | **425.18** | 464.31 | 555.01 |
| **30 min** | 117.81 | 157.99 | 184.59 | 218.17 | 243.10 | **267.85** | 292.50 | 349.63 |
| **1 hr** | 74.22 | 99.52 | 116.28 | 137.44 | 153.15 | **168.74** | 184.27 | 220.24 |
| **2 hr** | 46.75 | 62.70 | 73.25 | 86.58 | 96.48 | **106.30** | 116.08 | 138.75 |
| **3 hr** | 35.68 | 47.85 | 55.90 | 66.08 | 73.63 | **81.12** | 88.59 | 105.88 |
| **6 hr** | 22.48 | 30.14 | 35.21 | 41.62 | 46.38 | **51.10** | 55.81 | 66.70 |
| **12 hr** | 14.16 | 18.99 | 22.18 | 26.22 | 29.22 | **32.19** | 35.16 | 42.02 |
| **24 hr** | 8.92 | 11.96 | 13.97 | 16.52 | 18.41 | **20.28** | 22.15 | 26.47 |

---

## 4. Engineering Verification & Citation

These output files represent the authoritative basis for:
1. **Hydrological Inflow Modelling:** HEC-HMS 4.10 catchment routing and peak design hydrograph generation (Peak Inflow = $186.4 \text{ m}^3/\text{s}$).
2. **2D Hydraulic Dam Break Simulation:** HEC-RAS 2D breach propagation, peak flood wave routing, and hazard zonation under Overtopping ($Q_{\text{peak}} = 277.62 \text{ m}^3/\text{s}$) and Piping ($Q_{\text{peak}} = 221.78 \text{ m}^3/\text{s}$) failure modes.
3. **Emergency Action Planning (EAP):** Panvel city flood warning thresholds, inundation maps, and evacuation routes.

For any queries regarding the computations, contact:
* **Satwik Kamlakar Udupi**, Agriculture Er., CCCSS, Shivaji University, Kolhapur.
