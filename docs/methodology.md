# Methodology Notes — Dehrang Dam Hydrological & Dam Break Analysis

## 1. Dam and Project Background

**Dehrang Dam** is a minor earthen dam with an automatic gated spillway located at 19°1′54″N, 73°14′32″E in Raigad District, Maharashtra, commissioned in 1957 and operated by the Panvel Municipal Corporation. The dam stores water in the Gadhi River basin, which drains to the coastal lowlands south of Mumbai.

A Pre-monsoon 2025 inspection was carried out by Yash Engineering Consultant Pvt. Ltd. (Navi Mumbai) using the 10×10 m box method sludge survey, covering 3,193 grid boxes and measuring a total silt accumulation of 517,705.69 m³.

---

## 2. Storage-Elevation Analysis (Notebook 01)

### 2.1 Survey Data Processing
Each survey box records the bottom and top elevation of the sludge layer and the horizontal plan area of that box. The bottom elevation represents the original reservoir bed; the top elevation represents the current silt surface.

### 2.2 Area-Elevation Relationship
For each elevation h (0.2 m intervals from river bed to FRL):
- **Original area** = sum of plan areas of all boxes whose `Avg_Sludge_Bot ≤ h`
- **Current area** = sum of plan areas of all boxes whose `Avg_Sludge_Top ≤ h`

Above the maximum surveyed elevation, original area is extrapolated using a 2nd-order polynomial fitted to the survey data in the range 83.0–max_surveyed m. Current area above the maximum silt-top elevation is set equal to the original area (no silt recorded above that level).

### 2.3 Volume Integration
Cumulative storage is integrated using the trapezoidal rule:

```
V(i) = V(i-1) + (A(i-1) + A(i)) / 2 × Δh
```

where Δh = 0.2 m and A(i) is the water-spread area at elevation i.

### 2.4 Capacity Loss
Capacity loss at each elevation = Original cumulative volume − Current cumulative volume.

---

## 3. Hydrological Soil Group Classification (Notebooks 02, 03)

### 3.1 Soil Texture Data
Clay, sand, and silt fractions (g/kg) are downloaded at three depths (0–5 cm, 5–15 cm, 15–30 cm) from ISRIC SoilGrids v2 via the OGC WCS 2.0 API. Values are converted from stored integers (g/kg × 10) to percentages by dividing by 10. A depth-weighted composite is formed:

```
texture_0_30cm = (texture_0_5cm × 5 + texture_5_15cm × 10 + texture_15_30cm × 15) / 30
```

### 3.2 HSG Assignment
Each pixel is classified into USDA Hydrological Soil Group using the textural triangle:
- **Group A** (Low runoff potential): sand, loamy sand, sandy loam
- **Group B** (Moderate-low): silt loam, loam
- **Group C** (Moderate-high): sandy clay loam
- **Group D** (High runoff potential): clay loam, silty clay loam, sandy clay, silty clay, clay

---

## 4. SCS Curve Number Grid (Notebooks 02, 03)

Curve Numbers are assigned per the NRCS TR-55 (AMC II conditions) lookup table, adapted for Indian conditions per Mishra & Singh (2003). The CN for each pixel is determined by its combination of:
- LULC class (from ESA WorldCover 2021)
- HSG (A, B, C, or D)

---

## 5. Manning's Roughness Grid (Notebooks 02, 03)

Manning's n values are assigned per LULC class using:
- Open water, impervious surfaces: Chow (1959) channel values
- Forest, cropland, grassland: CWPRS (2018) and Arora et al. (2021) overland flow values

---

## 6. Watershed Delineation (Notebook 03)

### 6.1 DEM Pre-processing
1. Fill pits (single-cell depressions)
2. Fill depressions (multi-cell flat areas)
3. Resolve flats (assign drainage direction through flat areas)

### 6.2 D8 Flow Routing
Flow direction is computed using the D8 algorithm (eight-directional steepest descent). ESRI/HydroSHEDS direction codes: 64, 128, 1, 2, 4, 8, 16, 32.

### 6.3 Pour Point Snapping
Pour points are snapped to the nearest high-accumulation cell (accumulation threshold = 300 cells by default) within a configurable search radius.

### 6.4 Catchment Delineation
The catchment is delineated upstream of the snapped pour point and converted to a polygon using rasterio's polygonise function. Area is computed by reprojecting to UTM Zone 43N (EPSG:32643).

---

## 7. IDF Analysis — Gumbel EV-I Method (Notebook 04)

### 7.1 Distribution Fitting
The Gumbel Extreme Value Type-I distribution is fitted to N=31 years of annual maximum 24-hour rainfall using method-of-moments with reduced variate parameters from Gumbel (1958) tables, interpolated for N=31:

```
yₙ = 0.5362 + (1/5) × (0.5403 − 0.5362) = 0.53702
Sₙ = 1.1124 + (1/5) × (1.1285 − 1.1124) = 1.11562
```

### 7.2 Design Rainfall
For return period T:
```
yT  = −ln[−ln(1 − 1/T)]
K   = (yT − yₙ) / Sₙ
XT  = x̄ + K × S
```

95% confidence limits use the Chow (1951) formula:
```
SE = (S / Sₙ) × √[(1 + 1.1396K + 1.1K²) / N]
CL = XT ± 1.96 × SE
```

### 7.3 Sub-daily Disaggregation
The IMD Empirical Reduction Formula (CWC 1989, Appendix) is applied:
```
Pt = P24 × (t / 24)^(1/3)      [t in hours]
```

### 7.4 Design Storm — Alternating Block Method
The ABM distributes sub-period rainfall depths into a hyetograph such that the peak block is centred and subsequent blocks alternate left/right in descending order.

### 7.5 Goodness-of-Fit
- **Kolmogorov-Smirnov test** (α = 5%): D_critical = 1.36/√N
- **Chi-square test** (α = 5%, 5 equal-probability bins): df = k − 1 − p = 2

### 7.6 Design Standard
Per IS 11223 and CDSO GUD DS-06 v1.0 (June 2021), Tier-I minor dams use a **100-year return period** design flood.

---

## 8. Cartographic Maps (Notebook 05)

All maps use:
- **Projection**: UTM (EPSG auto-detected from input rasters)
- **Hillshade**: Computed from Copernicus DEM 30 m using matplotlib `LightSource` (azimuth 315°, altitude 60°, z-factor 1.0)
- **Grid**: Decimal degree gridlines at 0.1° intervals via cartopy `gridlines`
- **North arrow**: Text 'N' + triangle marker at axes upper-right
- **Scale bar**: `matplotlib_scalebar` at lower-left
- **Resolution**: 300 DPI, white background, `bbox_inches='tight'`
