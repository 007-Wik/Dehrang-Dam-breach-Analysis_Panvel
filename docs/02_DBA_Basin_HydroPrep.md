# 🌊 Dehrang DBA Basin — Hydrological Pre-Processing Notebook
### Curve Number Grid · Manning's Roughness · LULC from ESA WorldCover · ISRIC SoilGrids
---
**Purpose:** Prepare all hydrological raster layers required for dam break analysis  
**Data Sources:**  
- 🛰️ **ESA WorldCover 2021** (10 m) — LULC via Google Earth Engine  
- 🌍 **ISRIC SoilGrids v2** (250 m) — Soil texture via WCS REST API  
- 📐 **CN Values** — USDA TR-55 adapted for Indian conditions (Mishra & Singh 2003)  
- 💧 **Manning's n** — Chow (1959), CWPRS (2018), Arora et al. (2021)

**Outputs:** CN Grid · HSG Grid · Manning's n Grid · LULC Stats · Summary CSVs

---
> ⚠️ **Before running:** Upload all shapefile components to Google Drive or Colab Files.  
> Files needed: `.shp`, `.dbf`, `.shx`, `.prj`, `.cpg` (all Dehrang_DBA_Basin.*)

## 📦 Section 1 — Install Dependencies


```python
# Install all required packages
!pip install earthengine-api geemap geopandas rasterio numpy pandas \
             matplotlib requests pyproj shapely fiona scipy owslib \
             --quiet

print("✅ All packages installed!")
```

## 📚 Section 2 — Import Libraries


```python
import ee
import geemap
import geopandas as gpd
import rasterio
from rasterio.mask import mask as raster_mask
from rasterio.warp import reproject, Resampling
from rasterio.enums import Resampling as ResamplingEnum
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from pathlib import Path
import requests
import os, json, time, shutil, warnings

warnings.filterwarnings('ignore')
print("✅ All libraries imported!")
```

## 🔑 Section 3 — Google Earth Engine Authentication
> Run this cell **once per session**. Follow the URL that appears.


```python
# Authenticate GEE — follow the link and paste your token
ee.Authenticate()

# ⚠️ Replace 'your-project-id' with your actual GEE Cloud Project ID
GEE_PROJECT = 'your-project-id'   # <── CHANGE THIS
ee.Initialize(project=GEE_PROJECT)
print(f"✅ GEE initialized with project: {GEE_PROJECT}")
```

## 📂 Section 4 — Mount Google Drive & Set Paths
Upload your shapefile folder to Google Drive first, then update the path below.


```python
from google.colab import drive
drive.mount('/content/drive')

# ╔══════════════════════════════════════════════════════════╗
# ║         USER CONFIGURATION — EDIT THESE PATHS           ║
# ╚══════════════════════════════════════════════════════════╝

# Path to your Dehrang DBA Basin shapefile
SHAPEFILE_PATH = '/content/drive/MyDrive/Dehrang_DBA_Basin/Dehrang_DBA_Basin.shp'

# Output folder (will be created automatically)
OUTPUT_DIR = '/content/drive/MyDrive/Dehrang_DBA_Basin/outputs'
SOIL_DIR   = os.path.join(OUTPUT_DIR, 'soilgrids')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SOIL_DIR,   exist_ok=True)

print(f"📁 Shapefile : {SHAPEFILE_PATH}")
print(f"📁 Output dir: {OUTPUT_DIR}")
```

## 🗺️ Section 5 — Load AOI Shapefile


```python
# Load the basin shapefile
gdf = gpd.read_file(SHAPEFILE_PATH)
print(f"✅ Shapefile loaded")
print(f"   CRS         : {gdf.crs}")
print(f"   Features    : {len(gdf)}")
print(f"   Geometry    : {gdf.geom_type.unique()}")

# Reproject to WGS84 if needed
gdf_wgs84 = gdf.to_crs(epsg=4326) if gdf.crs.to_epsg() != 4326 else gdf.copy()

# Bounding box
bounds = gdf_wgs84.total_bounds  # [minx, miny, maxx, maxy]
BUFFER = 0.02                     # ~2 km padding
bbox_buf = [bounds[0]-BUFFER, bounds[1]-BUFFER,
            bounds[2]+BUFFER, bounds[3]+BUFFER]

print(f"\n📐 Basin bounding box (WGS84):")
print(f"   Lon: {bounds[0]:.4f} → {bounds[2]:.4f}")
print(f"   Lat: {bounds[1]:.4f} → {bounds[3]:.4f}")

# Create GEE geometry from shapefile
aoi_geojson = json.loads(gdf_wgs84.to_json())
aoi_ee = ee.FeatureCollection(aoi_geojson).geometry()
print(f"\n✅ GEE AOI geometry created")

# Quick plot
fig, ax = plt.subplots(figsize=(7, 5))
gdf_wgs84.plot(ax=ax, color='#aed6f1', edgecolor='#1a5276', linewidth=1.5, alpha=0.7)
ax.set_title('Dehrang DBA Basin — Area of Interest', fontsize=13, fontweight='bold')
ax.set_xlabel('Longitude (°E)'); ax.set_ylabel('Latitude (°N)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '00_AOI.png'), dpi=150)
plt.show()
```

## 🛰️ Section 6 — ESA WorldCover 2021 via GEE
Downloads the **ESA WorldCover v200 (2021)** at 10 m resolution, clips to basin, and exports to your Drive.


```python
# ── ESA WorldCover class definitions ──────────────────────────────────────
ESA_CLASSES = {
    10:  {'name': 'Tree cover',              'color': '#006400'},
    20:  {'name': 'Shrubland',               'color': '#ffbb22'},
    30:  {'name': 'Grassland',               'color': '#ffff4c'},
    40:  {'name': 'Cropland',                'color': '#f096ff'},
    50:  {'name': 'Built-up',                'color': '#fa0000'},
    60:  {'name': 'Bare / sparse vegetation','color': '#b4b4b4'},
    70:  {'name': 'Snow and ice',            'color': '#f0f0f0'},
    80:  {'name': 'Permanent water bodies',  'color': '#0064c8'},
    90:  {'name': 'Herbaceous wetland',      'color': '#0096a0'},
    95:  {'name': 'Mangroves',               'color': '#00cf75'},
    100: {'name': 'Moss and lichen',         'color': '#fae6a0'},
}

# ── Fetch & clip ────────────────────────────────────────────────────────────
worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().select('Map')
wc_clipped  = worldcover.clip(aoi_ee)

# ── Export to Google Drive ──────────────────────────────────────────────────
WC_FNAME = 'ESA_WorldCover_2021'
task_wc = ee.batch.Export.image.toDrive(
    image          = wc_clipped,
    description    = 'Dehrang_ESA_WorldCover_2021',
    folder         = 'Dehrang_DBA_Basin/outputs',
    fileNamePrefix = WC_FNAME,
    region         = aoi_ee,
    scale          = 10,
    crs            = 'EPSG:4326',
    maxPixels      = 1e13,
)
task_wc.start()
print(f"🚀 WorldCover export started  →  Task ID: {task_wc.id}")
print("   ⏳ Check GEE Task Manager  or  run: ee.batch.Task.list()")
print(f"   📁 File will appear in Drive → Dehrang_DBA_Basin/outputs/{WC_FNAME}.tif")
```


```python
# ── Monitor export (run after starting task) ─────────────────────────────
def monitor_task(task, poll=20):
    print(f"Monitoring task: {task.id}")
    while True:
        state = task.status()['state']
        print(f"  [{time.strftime('%H:%M:%S')}] {state}")
        if state in ('COMPLETED', 'FAILED', 'CANCELLED'):
            return state
        time.sleep(poll)

# Uncomment the line below to BLOCK until export completes:
# state = monitor_task(task_wc)
```


```python
# ── Load WorldCover locally after export completes ──────────────────────
WORLDCOVER_PATH = os.path.join(OUTPUT_DIR, f'{WC_FNAME}.tif')
WC_DRIVE_PATH   = f'/content/drive/MyDrive/Dehrang_DBA_Basin/outputs/{WC_FNAME}.tif'

if os.path.exists(WC_DRIVE_PATH) and not os.path.exists(WORLDCOVER_PATH):
    shutil.copy(WC_DRIVE_PATH, WORLDCOVER_PATH)

if os.path.exists(WORLDCOVER_PATH):
    with rasterio.open(WORLDCOVER_PATH) as src:
        print(f"✅ WorldCover loaded")
        print(f"   Resolution : {src.res[0]*111320:.1f} m × {src.res[1]*111320:.1f} m")
        print(f"   Size       : {src.width} × {src.height} px")
        print(f"   CRS        : {src.crs}")
else:
    print("⚠️  WorldCover file not yet available — wait for GEE export to complete,")
    print(f"   then re-run this cell.  Expected path: {WC_DRIVE_PATH}")
```

## 🌍 Section 7 — ISRIC SoilGrids Download (WCS API)
Downloads **clay, sand, silt** at 0–5 cm, 5–15 cm, 15–30 cm depth intervals  
and computes a depth-weighted average for the 0–30 cm profile.


```python
def download_soilgrids(variable, depth, stat, bbox, out_path, max_retries=3):
    """
    Download a SoilGrids coverage via the OGC WCS 2.0 API.

    SoilGrids scaling factors (units stored as integer):
      clay / sand / silt : stored as g/kg × 10  → divide by 10 to get %
    """
    base = 'https://maps.isric.org/mapserv'
    cov  = f'{variable}_{depth}_{stat}'
    url  = (
        f'{base}?map=/map/{variable}.map'
        f'&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage'
        f'&COVERAGEID={cov}'
        f'&FORMAT=image/tiff'
        f'&GEOTIFF:COMPRESS=DEFLATE'
        f'&SUBSETTING_CRS=http://www.opengis.net/def/crs/EPSG/0/4326'
        f'&SUBSET=X({bbox[0]},{bbox[2]})'
        f'&SUBSET=Y({bbox[1]},{bbox[3]})'
        f'&OUTPUTCRS=http://www.opengis.net/def/crs/EPSG/0/4326'
    )

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, timeout=180, stream=True)
            ct = r.headers.get('content-type', '')
            if r.status_code == 200 and ('tiff' in ct or 'octet' in ct):
                with open(out_path, 'wb') as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
                sz = os.path.getsize(out_path)/1024
                print(f"  ✅ {cov:<35}  {sz:>7.1f} KB")
                return True
            else:
                print(f"  ⚠️  {cov}  HTTP {r.status_code}  (attempt {attempt})")
        except Exception as e:
            print(f"  ❌ {cov}  Error: {e}  (attempt {attempt})")
        time.sleep(5)
    return False

# ── Download soil properties ──────────────────────────────────────────────
SOIL_VARS   = ['clay', 'sand', 'silt']
SOIL_DEPTHS = ['0-5cm', '5-15cm', '15-30cm']
# Depth weights (by actual thickness: 5 cm, 10 cm, 15 cm → total 30 cm)
DEPTH_WEIGHTS = {'0-5cm': 5/30, '5-15cm': 10/30, '15-30cm': 15/30}

soil_files = {v: {} for v in SOIL_VARS}

print("📥 Downloading ISRIC SoilGrids (clay, sand, silt) ...")
for var in SOIL_VARS:
    for depth in SOIL_DEPTHS:
        fname  = f"{var}_{depth.replace('-','_')}_mean.tif"
        fpath  = os.path.join(SOIL_DIR, fname)
        if os.path.exists(fpath):
            print(f"  ⏭  {fname} (cached)")
            soil_files[var][depth] = fpath
        else:
            ok = download_soilgrids(var, depth, 'mean', bbox_buf, fpath)
            if ok:
                soil_files[var][depth] = fpath

print("\n✅ SoilGrids download complete!")
```

## 🧮 Section 8 — Depth-Weighted Soil Texture (0–30 cm)


```python
def weighted_soil_array(soil_files, variable, depths, weights):
    """
    Compute depth-weighted average of a soil variable.
    Returns a float32 array in % units.
    """
    # Use first available file as spatial reference
    ref_path  = next(iter(soil_files[variable].values()))
    with rasterio.open(ref_path) as ref:
        ref_shape = (ref.height, ref.width)
        ref_meta  = ref.meta.copy()

    weighted = np.zeros(ref_shape, dtype=np.float64)
    w_total  = 0.0

    for depth in depths:
        if depth not in soil_files[variable]:
            continue
        w = weights[depth]
        with rasterio.open(soil_files[variable][depth]) as src:
            raw  = src.read(1, out_shape=ref_shape,
                            resampling=ResamplingEnum.bilinear).astype(np.float64)
            nd   = src.nodata if src.nodata is not None else -32768
            mask_ = (raw != nd) & np.isfinite(raw)
            # SoilGrids units: g/kg * 10 → divide by 10 → g/kg → same as % for these vars
            # Actually clay/sand/silt in SoilGrids are in g/kg; divide by 10 → %
            pct   = np.where(mask_, raw / 10.0, np.nan)
            valid = np.isfinite(pct)
            weighted[valid] += pct[valid] * w
            w_total += w

    result = weighted / w_total if w_total > 0 else weighted
    return result.astype(np.float32), ref_meta

# Compute for each texture fraction
ref_path = next(iter(soil_files['clay'].values()))
clay_pct, ref_meta = weighted_soil_array(soil_files, 'clay', SOIL_DEPTHS, DEPTH_WEIGHTS)
sand_pct, _        = weighted_soil_array(soil_files, 'sand', SOIL_DEPTHS, DEPTH_WEIGHTS)
silt_pct, _        = weighted_soil_array(soil_files, 'silt', SOIL_DEPTHS, DEPTH_WEIGHTS)

def stat_row(name, arr):
    v = arr[np.isfinite(arr)]
    return f"  {name:<8}: mean={np.mean(v):.1f}%  min={np.min(v):.1f}%  max={np.max(v):.1f}%  std={np.std(v):.1f}%"

print("📊 Soil texture statistics (0–30 cm weighted average):")
print(stat_row('Clay',  clay_pct))
print(stat_row('Sand',  sand_pct))
print(stat_row('Silt',  silt_pct))
```

## 🏔️ Section 9 — Hydrologic Soil Group (HSG) Classification
Uses **USDA clay-content thresholds** (Rawls et al. 1982) validated for Indian soils  
(Soil Science Society of India; IMD Classification).

| HSG | Clay (%) | Infiltration | Description |
|-----|----------|-------------|-------------|
| A   | < 10     | High        | Sand, loamy sand |
| B   | 10–20    | Moderate    | Sandy loam, loam |
| C   | 20–35    | Low         | Sandy clay loam |
| D   | ≥ 35     | Very low    | Clay loam, clay |


```python
# ── Vectorised HSG from clay % ─────────────────────────────────────────────
# Reference: Rawls et al. (1982); Mishra & Singh (2003) Table 3.2
hsg_num = np.where(~np.isfinite(clay_pct), 0,
          np.where(clay_pct < 10,           1,   # A
          np.where(clay_pct < 20,           2,   # B
          np.where(clay_pct < 35,           3,   # C
                                            4    # D
          ))))
hsg_num = hsg_num.astype(np.uint8)

HSG_META = {0:'NoData', 1:'A', 2:'B', 3:'C', 4:'D'}
HSG_COLORS = {0:'#ffffff', 1:'#27ae60', 2:'#2980b9', 3:'#e67e22', 4:'#c0392b'}

# Statistics
print("📊 HSG Distribution:")
total = hsg_num.size
for v in range(5):
    cnt = np.sum(hsg_num == v)
    if cnt:
        print(f"  HSG {HSG_META[v]:<7}: {cnt:>9,} px  ({100*cnt/total:5.1f}%)")

# Save HSG GeoTIFF
hsg_meta = ref_meta.copy()
hsg_meta.update({'dtype':'uint8', 'nodata':0, 'count':1,
                 'compress':'lzw', 'predictor':1})
HSG_PATH = os.path.join(OUTPUT_DIR, 'HSG_grid.tif')
with rasterio.open(HSG_PATH, 'w', **hsg_meta) as dst:
    dst.write(hsg_num, 1)
print(f"\n💾 HSG grid saved → {HSG_PATH}")
```

## 📋 Section 10 — Curve Number Lookup Table
CN values are assigned per **ESA WorldCover class × HSG** combination.

**References:**
- USDA TR-55 (1986) — National Engineering Handbook Section 4
- Mishra & Singh (2003) — SCS-CN Methodology, Springer
- Kumar et al. (2021) — CN from LULC for Indian river basins (J. Hydrology)
- Chandniha & Kansal (2017) — SCS-CN analysis, Jharkhand
- Rawat & Singh (2017) — LULC-based runoff, Himalayan watersheds
- Patel et al. (2009) — CN estimation, Gujarat


```python
# ── CN Lookup Table ────────────────────────────────────────────────────────
# Each entry: ESA class code → {name, HSG-A, HSG-B, HSG-C, HSG-D, notes}
CN_TABLE = {
    #  Class |  Name                      |   A    B    C    D  | Notes
    10:  dict(name='Tree cover',              A=30, B=55, C=70, D=77,
              notes='Dense forest; Mishra & Singh (2003) Table 5.3'),
    20:  dict(name='Shrubland',               A=35, B=56, C=70, D=77,
              notes='Scrub/brush; TR-55 Table 2-2c poor condition'),
    30:  dict(name='Grassland',               A=39, B=61, C=74, D=80,
              notes='Natural grass; TR-55 Table 2-2a fair condition'),
    40:  dict(name='Cropland',                A=67, B=78, C=85, D=89,
              notes='Row crops straight rows; TR-55; Patel et al. 2009'),
    50:  dict(name='Built-up',                A=77, B=85, C=90, D=92,
              notes='Urban ≥50% imperv; TR-55; Chandniha & Kansal 2017'),
    60:  dict(name='Bare/sparse vegetation',  A=77, B=86, C=91, D=94,
              notes='Degraded/rocky/fallow; TR-55 Table 2-2e'),
    70:  dict(name='Snow and ice',            A=100,B=100,C=100,D=100,
              notes='Treated as impervious; no infiltration'),
    80:  dict(name='Permanent water bodies',  A=100,B=100,C=100,D=100,
              notes='Open water = 100% runoff; TR-55'),
    90:  dict(name='Herbaceous wetland',      A=78, B=78, C=78, D=78,
              notes='Wetland uniform CN; Rawat & Singh 2017'),
    95:  dict(name='Mangroves',               A=30, B=55, C=70, D=77,
              notes='Treated as dense woodland; Bajracharya et al. 2018'),
    100: dict(name='Moss and lichen',         A=30, B=48, C=65, D=73,
              notes='Alpine/sparse; Kumar et al. 2021'),
}

cn_df = pd.DataFrame.from_dict(CN_TABLE, orient='index')
cn_df.index.name = 'ESA_Code'
cn_df = cn_df.reset_index()

print("=" * 75)
print(" CURVE NUMBER TABLE  ·  ESA WorldCover × Hydrologic Soil Group")
print(" Source: USDA TR-55 | Mishra & Singh (2003) | Kumar et al. (2021)")
print("=" * 75)
print(cn_df[['ESA_Code','name','A','B','C','D']].to_string(index=False))

CN_TABLE_PATH = os.path.join(OUTPUT_DIR, 'CN_Table_ESA_WorldCover.csv')
cn_df.to_csv(CN_TABLE_PATH, index=False)
print(f"\n💾 CN table saved → {CN_TABLE_PATH}")
```

## 🌊 Section 11 — Manning's Roughness Coefficient Table
**References from Indian literature:**
- Chow, V.T. (1959) — Open-Channel Hydraulics (Tables 5.6 & 5.7)
- CWPRS Technical Report (2018) — Roughness for Indian river systems
- Arora et al. (2021) — ESA-WorldCover based roughness mapping, Western Ghats
- Patel, D.P. et al. (2012) — Flood modelling, Gujarat rivers
- Bajracharya et al. (2018) — Land cover roughness, South Asia HEC-RAS models
- HEC-RAS Reference Manual v6 (USACE 2021) — Overland flow n values


```python
# ── Manning's Roughness Table ──────────────────────────────────────────────
MANNINGS = {
    10:  dict(name='Tree cover',              n=0.150, n_min=0.100, n_max=0.200,
              desc='Dense forest / woodland with undergrowth',
              ref='Chow(1959); Arora et al.(2021); CWPRS(2018)'),
    20:  dict(name='Shrubland',               n=0.080, n_min=0.050, n_max=0.120,
              desc='Shrubs, scrubland, moderate stem resistance',
              ref='Chow(1959); Patel et al.(2012)'),
    30:  dict(name='Grassland',               n=0.035, n_min=0.025, n_max=0.060,
              desc='Natural short-to-medium grass; meadow',
              ref='Chow(1959); CWPRS(2018)'),
    40:  dict(name='Cropland',                n=0.040, n_min=0.025, n_max=0.055,
              desc='Agricultural fields; varies with crop season (kharif/rabi)',
              ref='Patel et al.(2012); Bajracharya et al.(2018)'),
    50:  dict(name='Built-up',                n=0.015, n_min=0.011, n_max=0.025,
              desc='Urban/paved; concrete, roads, impervious surfaces',
              ref='Chow(1959); HEC-RAS v6(2021)'),
    60:  dict(name='Bare/sparse vegetation',  n=0.025, n_min=0.015, n_max=0.040,
              desc='Rocky, gravelly, sparsely vegetated degraded land',
              ref='Chow(1959); Arora et al.(2021)'),
    70:  dict(name='Snow and ice',            n=0.010, n_min=0.008, n_max=0.020,
              desc='Smooth glacial ice, low friction surface',
              ref='Chow(1959)'),
    80:  dict(name='Permanent water bodies',  n=0.030, n_min=0.020, n_max=0.060,
              desc='Lakes, reservoirs, rivers; HEC-RAS channel value',
              ref='HEC-RAS v6(2021); CWPRS(2018)'),
    90:  dict(name='Herbaceous wetland',      n=0.070, n_min=0.050, n_max=0.100,
              desc='Reeds, sedges, emergent wetland vegetation',
              ref='Chow(1959); Patel et al.(2012)'),
    95:  dict(name='Mangroves',               n=0.150, n_min=0.100, n_max=0.250,
              desc='Dense mangrove forest; very high hydraulic resistance',
              ref='Arora et al.(2021); Bajracharya et al.(2018)'),
    100: dict(name='Moss and lichen',         n=0.070, n_min=0.050, n_max=0.100,
              desc='Alpine / tundra; moss and lichen covered rock surfaces',
              ref='Chow(1959); HEC-RAS v6(2021)'),
}

mann_df = pd.DataFrame.from_dict(MANNINGS, orient='index')
mann_df.index.name = 'ESA_Code'
mann_df = mann_df.reset_index()

print("=" * 100)
print(" MANNING'S ROUGHNESS TABLE  ·  ESA WorldCover LULC Classes")
print(" Primary sources: Chow(1959); CWPRS(2018); Arora et al.(2021)")
print("=" * 100)
print(mann_df[['ESA_Code','name','n','n_min','n_max','desc']].to_string(index=False))

MANN_PATH = os.path.join(OUTPUT_DIR, 'Mannings_n_ESA_WorldCover.csv')
mann_df.to_csv(MANN_PATH, index=False)
print(f"\n💾 Manning's table saved → {MANN_PATH}")
```

## 🗃️ Section 12 — Create CN Grid (LULC × HSG Overlay)
Resamples the HSG raster to match WorldCover 10 m resolution, then assigns CN  
values pixel-by-pixel using the lookup table above.


```python
def build_cn_grid(wc_path, hsg_arr, hsg_meta, cn_table, aoi_gdf, out_path):
    """
    Overlay ESA WorldCover LULC with HSG to produce a CN grid.
    Returns (cn_grid, out_meta).
    """
    with rasterio.open(wc_path) as wc_src:
        # Mask to AOI
        aoi_r   = aoi_gdf.to_crs(wc_src.crs)
        shapes  = [g.__geo_interface__ for g in aoi_r.geometry]
        wc_arr, wc_tf = raster_mask(wc_src, shapes, crop=True, nodata=0)
        wc_arr  = wc_arr[0]
        out_meta = wc_src.meta.copy()
        out_meta.update({'height': wc_arr.shape[0], 'width': wc_arr.shape[1],
                         'transform': wc_tf, 'dtype':'float32',
                         'nodata':-9999, 'count':1, 'compress':'lzw'})

    # Resample HSG to WorldCover grid (nearest-neighbour)
    hsg_10m = np.zeros(wc_arr.shape, dtype=np.uint8)
    reproject(
        source      = hsg_arr,
        destination = hsg_10m,
        src_transform  = hsg_meta['transform'],
        src_crs        = hsg_meta['crs'],
        dst_transform  = wc_tf,
        dst_crs        = out_meta['crs'],
        resampling     = Resampling.nearest
    )

    # Build CN grid
    cn = np.full(wc_arr.shape, -9999.0, dtype=np.float32)
    HSG_KEY = {1:'A', 2:'B', 3:'C', 4:'D'}
    for cls, vals in cn_table.items():
        lm = (wc_arr == cls)
        if not np.any(lm):
            continue
        for hn, hl in HSG_KEY.items():
            mask_ = lm & (hsg_10m == hn)
            if np.any(mask_):
                cn[mask_] = float(vals[hl])

    # Mask no-data
    cn[(wc_arr == 0) | (hsg_10m == 0)] = -9999.0

    with rasterio.open(out_path, 'w', **out_meta) as dst:
        dst.write(cn, 1)

    valid = cn[cn != -9999]
    print(f"📊 CN Grid Statistics:")
    print(f"   Mean   : {np.mean(valid):.2f}")
    print(f"   Median : {np.median(valid):.2f}")
    print(f"   Min    : {np.min(valid):.2f}")
    print(f"   Max    : {np.max(valid):.2f}")
    print(f"   Std    : {np.std(valid):.2f}")
    return cn, out_meta

CN_PATH = os.path.join(OUTPUT_DIR, 'CN_Grid.tif')

if os.path.exists(WORLDCOVER_PATH):
    cn_grid, cn_meta = build_cn_grid(
        WORLDCOVER_PATH, hsg_num, hsg_meta,
        CN_TABLE, gdf_wgs84, CN_PATH
    )
    print(f"\n💾 CN Grid saved → {CN_PATH}")
else:
    print("⚠️  WorldCover raster not found — complete GEE export (Section 6) first.")
    cn_grid = None
```

## 🔢 Section 13 — Manning's Roughness Grid


```python
def build_mannings_grid(wc_path, mannings, aoi_gdf, out_path):
    with rasterio.open(wc_path) as wc_src:
        aoi_r   = aoi_gdf.to_crs(wc_src.crs)
        shapes  = [g.__geo_interface__ for g in aoi_r.geometry]
        wc_arr, wc_tf = raster_mask(wc_src, shapes, crop=True, nodata=0)
        wc_arr  = wc_arr[0]
        meta    = wc_src.meta.copy()
        meta.update({'height':wc_arr.shape[0], 'width':wc_arr.shape[1],
                     'transform':wc_tf, 'dtype':'float32',
                     'nodata':-9999.0, 'count':1, 'compress':'lzw'})

    n_grid = np.full(wc_arr.shape, -9999.0, dtype=np.float32)
    for cls, vals in mannings.items():
        mask_ = wc_arr == cls
        if np.any(mask_):
            n_grid[mask_] = float(vals['n'])

    with rasterio.open(out_path, 'w', **meta) as dst:
        dst.write(n_grid, 1)

    valid = n_grid[n_grid != -9999]
    print(f"📊 Manning's n Statistics:")
    print(f"   Mean : {np.mean(valid):.4f}")
    print(f"   Min  : {np.min(valid):.4f}")
    print(f"   Max  : {np.max(valid):.4f}")
    return n_grid

MANN_GRID_PATH = os.path.join(OUTPUT_DIR, 'Mannings_n_Grid.tif')

if os.path.exists(WORLDCOVER_PATH):
    mann_grid = build_mannings_grid(WORLDCOVER_PATH, MANNINGS, gdf_wgs84, MANN_GRID_PATH)
    print(f"\n💾 Manning's n grid saved → {MANN_GRID_PATH}")
else:
    print("⚠️  WorldCover raster not found — complete GEE export first.")
    mann_grid = None
```

## 📊 Section 14 — LULC Area Statistics & Basin Summary


```python
if os.path.exists(WORLDCOVER_PATH):
    with rasterio.open(WORLDCOVER_PATH) as wc_src:
        aoi_r   = gdf_wgs84.to_crs(wc_src.crs)
        shapes  = [g.__geo_interface__ for g in aoi_r.geometry]
        wc_stat, wc_tf = raster_mask(wc_src, shapes, crop=True, nodata=0)
        wc_stat = wc_stat[0]
        # Pixel area in km²  (WGS84 degrees → approx metres)
        res_deg = abs(wc_src.res[0])
        mid_lat = (bounds[1] + bounds[3]) / 2
        m_per_deg_lon = 111320 * np.cos(np.radians(mid_lat))
        m_per_deg_lat = 110574
        px_km2  = (res_deg * m_per_deg_lon) * (res_deg * m_per_deg_lat) / 1e6

    total_px = np.sum(wc_stat > 0)
    rows = []
    for code, info in ESA_CLASSES.items():
        cnt = int(np.sum(wc_stat == code))
        if cnt == 0:
            continue
        rows.append({
            'ESA_Code':    code,
            'LULC_Name':   info['name'],
            'Pixels':      cnt,
            'Area_km2':    round(cnt * px_km2, 3),
            'Area_pct':    round(100 * cnt / total_px, 2),
            'CN_HSG_B':    CN_TABLE.get(code, {}).get('B', '-'),
            'Mannings_n':  MANNINGS.get(code, {}).get('n', '-'),
        })

    lulc_stats = pd.DataFrame(rows).sort_values('Area_km2', ascending=False)
    print("=" * 80)
    print(" LULC AREA STATISTICS — Dehrang DBA Basin")
    print("=" * 80)
    print(lulc_stats.to_string(index=False))

    total_area = lulc_stats['Area_km2'].sum()
    print(f"\n  📐 Total Basin Area : {total_area:.2f} km²")

    LULC_STATS_PATH = os.path.join(OUTPUT_DIR, 'LULC_Area_Statistics.csv')
    lulc_stats.to_csv(LULC_STATS_PATH, index=False)
    print(f"  💾 Saved → {LULC_STATS_PATH}")
else:
    print("⚠️  WorldCover not available yet.")
```

## 📐 Section 15 — Area-Weighted CN & AMC Adjustment
Computes basin-wide **CN-II** and adjusts for **AMC-I** (dry) and **AMC-III** (wet) using  
Mishra & Singh (2003) equations — standard for Indian conditions.


```python
if 'lulc_stats' in dir():
    cn_b = lulc_stats['CN_HSG_B'].astype(float)
    area = lulc_stats['Area_km2']
    cn2  = (cn_b * area).sum() / area.sum()

    # AMC adjustment — Mishra & Singh (2003), Eqs. 3.19–3.20
    cn1 = cn2 / (2.281 - 0.01281 * cn2)
    cn3 = cn2 / (0.427  + 0.00573 * cn2)

    # SCS-CN storage
    S_mm = 25.4 * (1000.0 / cn2 - 10)   # Potential max retention (mm)
    Ia   = 0.2  * S_mm                   # Initial abstraction (mm)  [Indian std λ=0.2]
    Ia_alt = 0.1 * S_mm                  # Alternative λ=0.1 (Mishra & Singh)

    print("=" * 55)
    print(" SCS-CN BASIN SUMMARY — Dehrang DBA Basin")
    print("=" * 55)
    print(f"  AMC-I  (Dry)    CN =  {cn1:.2f}")
    print(f"  AMC-II (Normal) CN =  {cn2:.2f}  ← Design value")
    print(f"  AMC-III (Wet)   CN =  {cn3:.2f}")
    print(f"  Max Retention S     = {S_mm:.2f} mm")
    print(f"  Ia (λ=0.2, USDA)   = {Ia:.2f} mm")
    print(f"  Ia (λ=0.1, M&S)    = {Ia_alt:.2f} mm")

    summary = pd.DataFrame({
        'Parameter': ['AMC-I CN','AMC-II CN','AMC-III CN',
                      'S_mm','Ia_lambda_0.2_mm','Ia_lambda_0.1_mm'],
        'Value':     [round(cn1,2), round(cn2,2), round(cn3,2),
                      round(S_mm,2), round(Ia,2), round(Ia_alt,2)]
    })
    SUM_PATH = os.path.join(OUTPUT_DIR, 'CN_Summary.csv')
    summary.to_csv(SUM_PATH, index=False)
    print(f"\n  💾 Saved → {SUM_PATH}")
```

## 🖼️ Section 16 — Publication-Quality Visualisation


```python
fig, axes = plt.subplots(1, 3, figsize=(22, 8), facecolor='#1c1c1c')
fig.suptitle('Dehrang DBA Basin — Hydrological Pre-Processing',
             fontsize=16, fontweight='bold', color='white', y=1.01)

# ── Helper: display a raster array ────────────────────────────────────────
def show_raster(ax, arr, cmap, title, vmin=None, vmax=None,
                nodata=-9999, label='', legend=None):
    display = np.where(arr == nodata, np.nan, arr) if nodata else arr.astype(float)
    im = ax.imshow(display, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto',
                   interpolation='nearest')
    ax.set_title(title, color='white', fontsize=11, fontweight='bold', pad=10)
    ax.axis('off')
    if legend:
        ax.legend(handles=legend, loc='lower left', fontsize=7,
                  facecolor='#2c2c2c', labelcolor='white',
                  edgecolor='gray', title_fontsize=8)
    else:
        cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=label)
        cb.ax.yaxis.label.set_color('white')
        cb.ax.tick_params(colors='white')
    return im

# ── Panel 1: ESA WorldCover LULC ──────────────────────────────────────────
if os.path.exists(WORLDCOVER_PATH):
    with rasterio.open(WORLDCOVER_PATH) as src:
        aoi_r  = gdf_wgs84.to_crs(src.crs)
        shapes = [g.__geo_interface__ for g in aoi_r.geometry]
        wc_v, _ = raster_mask(src, shapes, crop=True, nodata=0)
        wc_v    = wc_v[0]

    rgba = np.zeros((*wc_v.shape, 4))
    for cls, info in ESA_CLASSES.items():
        m = wc_v == cls
        rgba[m] = list(mcolors.to_rgba(info['color']))
    rgba[wc_v == 0] = [0,0,0,0]
    axes[0].imshow(rgba, aspect='auto', interpolation='nearest')
    axes[0].set_title('ESA WorldCover 2021\n(10 m)', color='white',
                      fontsize=11, fontweight='bold', pad=10)
    axes[0].axis('off')
    legend = [mpatches.Patch(color=v['color'],
                             label=f"{k}: {v['name'][:18]}")
              for k, v in ESA_CLASSES.items()]
    axes[0].legend(handles=legend, loc='lower left', fontsize=6.5,
                   facecolor='#2c2c2c', labelcolor='white',
                   edgecolor='gray', title='LULC Class', title_fontsize=7)

# ── Panel 2: HSG ──────────────────────────────────────────────────────────
hsg_rgba = np.zeros((*hsg_num.shape, 4))
for val, col in HSG_COLORS.items():
    m = hsg_num == val
    hsg_rgba[m] = list(mcolors.to_rgba(col))
axes[1].imshow(hsg_rgba, aspect='auto', interpolation='nearest')
axes[1].set_title('Hydrologic Soil Group\n(ISRIC SoilGrids 250 m)',
                  color='white', fontsize=11, fontweight='bold', pad=10)
axes[1].axis('off')
hsg_leg = [mpatches.Patch(color=HSG_COLORS[i],
                           label=f"HSG {HSG_META[i]}")
           for i in [1,2,3,4]]
axes[1].legend(handles=hsg_leg, loc='lower left', fontsize=9,
               facecolor='#2c2c2c', labelcolor='white', edgecolor='gray')

# ── Panel 3: CN Grid ──────────────────────────────────────────────────────
if cn_grid is not None:
    show_raster(axes[2], cn_grid, 'RdYlGn_r',
                'Curve Number Grid\n(ESA WorldCover × ISRIC HSG)',
                vmin=30, vmax=100, label='Curve Number (CN)')
else:
    axes[2].text(0.5, 0.5, 'CN Grid\nNot yet available\n(Run Section 12)',
                 ha='center', va='center', color='white', fontsize=12,
                 transform=axes[2].transAxes)
    axes[2].set_facecolor('#2c2c2c'); axes[2].axis('off')

plt.tight_layout()
VIZ_PATH = os.path.join(OUTPUT_DIR, 'Hydrological_Overview.png')
plt.savefig(VIZ_PATH, dpi=200, bbox_inches='tight', facecolor='#1c1c1c')
plt.show()
print(f"💾 Figure saved → {VIZ_PATH}")
```

## 🎯 Section 17 — Reproject to UTM for Dam Break Analysis
HEC-RAS 2D requires **projected coordinates** (metres) for accurate area/velocity calcs.  
For the Dehrang basin, determine the correct UTM zone and reproject all outputs.


```python
# ── Determine UTM zone from basin centroid ────────────────────────────────
centroid_lon = (bounds[0] + bounds[2]) / 2
centroid_lat = (bounds[1] + bounds[3]) / 2
utm_zone     = int((centroid_lon + 180) / 6) + 1
hemisphere   = 'N' if centroid_lat >= 0 else 'S'
epsg_utm     = 32600 + utm_zone if hemisphere == 'N' else 32700 + utm_zone

print(f"📐 Basin centroid: {centroid_lat:.4f}°N, {centroid_lon:.4f}°E")
print(f"📐 UTM Zone: {utm_zone}{hemisphere}  →  EPSG:{epsg_utm}")

def reproject_raster(src_path, dst_path, target_epsg, resampling_method=Resampling.nearest):
    """Reproject a GeoTIFF to a target CRS."""
    from rasterio.warp import calculate_default_transform
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, f'EPSG:{target_epsg}', src.width, src.height, *src.bounds)
        meta = src.meta.copy()
        meta.update({'crs': f'EPSG:{target_epsg}',
                     'transform': transform,
                     'width': width, 'height': height})
        with rasterio.open(dst_path, 'w', **meta) as dst:
            for i in range(1, src.count + 1):
                reproject(source=rasterio.band(src, i),
                          destination=rasterio.band(dst, i),
                          src_transform=src.transform,
                          src_crs=src.crs,
                          dst_transform=transform,
                          dst_crs=f'EPSG:{target_epsg}',
                          resampling=resampling_method)
    print(f"  ✅ Reprojected → {os.path.basename(dst_path)}")

UTM_DIR = os.path.join(OUTPUT_DIR, f'UTM_{utm_zone}{hemisphere}')
os.makedirs(UTM_DIR, exist_ok=True)

files_to_reproject = {
    CN_PATH:        ('CN_Grid_UTM.tif',        Resampling.bilinear),
    MANN_GRID_PATH: ('Mannings_n_Grid_UTM.tif', Resampling.nearest),
    HSG_PATH:       ('HSG_Grid_UTM.tif',        Resampling.nearest),
}
if os.path.exists(WORLDCOVER_PATH):
    files_to_reproject[WORLDCOVER_PATH] = ('ESA_WorldCover_UTM.tif', Resampling.nearest)

print("\n🔄 Reprojecting all grids to UTM ...")
for src_p, (fname, res_method) in files_to_reproject.items():
    if os.path.exists(src_p):
        reproject_raster(src_p, os.path.join(UTM_DIR, fname), epsg_utm, res_method)
    else:
        print(f"  ⚠️  Skipped {fname} (source not found)")

print(f"\n✅ All UTM rasters saved in: {UTM_DIR}")
```

## ✅ Section 18 — Final Output Summary & Report


```python
print("=" * 70)
print(" DEHRANG DBA BASIN — HYDROLOGICAL PRE-PROCESSING COMPLETE")
print("=" * 70)
print()
print("OUTPUT FILES:")
print("-" * 70)
for root, dirs, files in os.walk(OUTPUT_DIR):
    level = root.replace(OUTPUT_DIR, '').count(os.sep)
    indent = '  ' * level
    subdir = os.path.basename(root)
    if level > 0:
        print(f"{indent}📁 {subdir}/")
    for fname in sorted(files):
        fpath = os.path.join(root, fname)
        sz    = os.path.getsize(fpath) / 1024
        unit  = 'KB' if sz < 1024 else 'MB'
        sz    = sz if sz < 1024 else sz/1024
        sub   = '  ' * (level + 1)
        print(f"{sub}📄 {fname:<45} {sz:>7.1f} {unit}")

print()
print("REFERENCES:")
print("-" * 70)
refs = [
    "[1] Mishra, S.K. & Singh, V.P. (2003). SCS-CN Methodology. Springer.",
    "[2] Arora, A. et al. (2021). ESA-WorldCover LULC for Indian hydrology.",
    "[3] CWPRS Technical Report (2018). Manning's n for Indian river systems.",
    "[4] Patel, D.P. et al. (2012). Extreme flood assessment, Gujarat.",
    "[5] Chow, V.T. (1959). Open-Channel Hydraulics. McGraw-Hill.",
    "[6] USDA (1986). TR-55 Urban Hydrology for Small Watersheds.",
    "[7] Kumar, R. et al. (2021). SCS-CN with ESA WorldCover, India.",
    "[8] Chandniha & Kansal (2017). SCS-CN, Jharkhand watershed.",
    "[9] Rawat & Singh (2017). LULC-based runoff, Himalayan watershed.",
    "[10] Bajracharya et al. (2018). HEC-RAS modelling, South Asia.",
    "[11] HEC-RAS Reference Manual v6.3 (USACE 2021).",
]
for r in refs:
    print(f"  {r}")

print()
print("NEXT STEPS FOR DAM BREAK ANALYSIS:")
print("-" * 70)
steps = [
    "1. Import CN_Grid_UTM.tif into HEC-HMS as SCS curve number layer",
    "2. Import Mannings_n_Grid_UTM.tif into HEC-RAS 2D terrain preprocessing",
    "3. Import ESA_WorldCover_UTM.tif as land cover layer in HEC-RAS",
    "4. Use CN Summary (AMC-II) to compute design storm runoff hydrograph",
    "5. Set up HEC-RAS 2D unsteady flow with dam breach hydrograph",
    "6. Validate Manning's n with observed gauge data if available",
]
for s in steps:
    print(f"  {s}")
print("=" * 70)
```
