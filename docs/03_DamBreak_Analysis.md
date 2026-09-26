# 🏞️ Dehrang Dam Break Analysis — Jupyter Notebook
**Raigad District, Maharashtra, India**

| Pour Point | Purpose | Latitude | Longitude |
|---|---|---|---|
| PP1 | Dehrang Dam Catchment | 19°2′1.71″N | 73°14′31.07″E |
| PP2 | River Basin Confluence | 19°1′13.73″N | 73°9′36.06″E |

---
### Workflow
1. **Extract** local DEM tar.gz files (COP30 + SRTM)
2. **Delineate** both watersheds with pysheds (D8 routing)
3. **LULC** — ESA WorldCover 2021 via GEE *or* STAC API
4. **HSG** — SoilGrids v2 REST API (global, no auth needed)
5. **CN Grid** — AMC II (NRCS TR-55 / NEH-630)
6. **Manning's n** grid from LULC
7. **Zonal statistics** per watershed
8. **Interactive map** (folium + geemap)
9. **Export** all rasters as GeoTIFF + shapefiles



```python
# ─────────────────────────────────────────────────────────────
# CELL 0 ─ Install dependencies  (run once)
# ─────────────────────────────────────────────────────────────
import subprocess, sys

pkgs = [
    'earthengine-api', 'geemap',
    'pysheds',
    'geopandas', 'rasterio', 'rasterstats',
    'shapely', 'fiona',
    'requests', 'numpy', 'pandas', 'matplotlib',
    'folium', 'branca',
    'scipy',
]

for pkg in pkgs:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg])

print('✅ All packages installed.')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 1 ─ Imports
# ─────────────────────────────────────────────────────────────
import os, glob, tarfile, json, warnings, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import requests
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling
from rasterio import features as rio_features
import geopandas as gpd
from shapely.geometry import shape, mapping, Point, box
from shapely.ops import unary_union
import folium
from folium import plugins
import warnings
warnings.filterwarnings('ignore')

# pysheds
from pysheds.grid import Grid

print('✅ Imports OK')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 2 ─ Configuration  ← EDIT THESE PATHS
# ─────────────────────────────────────────────────────────────

# ── Pour Points (DMS → decimal) ──────────────────────────────
LAT1 = 19 + 2/60 + 1.71/3600     # 19.03381 °N  — Dehrang Dam
LON1 = 73 + 14/60 + 31.07/3600   # 73.24196 °E

LAT2 = 19 + 1/60 + 13.73/3600    # 19.02048 °N  — River Confluence
LON2 = 73 + 9/60 + 36.06/3600    # 73.16002 °E

# ── Local file paths ─────────────────────────────────────────
# Set these to the folder that contains your .tar.gz downloads
DOWNLOAD_DIR   = r'.'                    # ← Change to your downloads folder
OUTPUT_DIR     = r'dehrang_outputs'      # All outputs saved here

# Expected tar.gz filenames (adjust if yours differ)
COP30_TGZ  = os.path.join(DOWNLOAD_DIR, 'rasters_COP30.tar.gz')
SRTM_TGZ   = os.path.join(DOWNLOAD_DIR, 'rasters_SRTMGL1.tar.gz')

# GEE project (optional — only needed for WorldCover / extra layers)
GEE_PROJECT = 'your-gee-project-id'     # ← Replace or leave if skipping GEE

# ── Bounding box (auto) ──────────────────────────────────────
BUFFER  = 0.35   # degrees around pour points
BBOX    = (
    min(LON1,LON2)-BUFFER,  # west
    min(LAT1,LAT2)-BUFFER,  # south
    max(LON1,LON2)+BUFFER,  # east
    max(LAT1,LAT2)+BUFFER,  # north
)
print(f'  PP1 (Dam)        : {LAT1:.5f}°N  {LON1:.5f}°E')
print(f'  PP2 (Confluence) : {LAT2:.5f}°N  {LON2:.5f}°E')
print(f'  Bounding box     : {BBOX}')

os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f'\n✅ Output folder: {OUTPUT_DIR}/')
```

---
## 📦 Section 1 — Extract Local DEM Files


```python
# ─────────────────────────────────────────────────────────────
# CELL 3 ─ Extract tar.gz files
# ─────────────────────────────────────────────────────────────

def extract_tgz(tgz_path: str, out_dir: str) -> list:
    """Extract a .tar.gz and return list of extracted .tif paths."""
    if not os.path.exists(tgz_path):
        print(f'  ⚠️  File not found: {tgz_path}')
        return []
    print(f'  Extracting {os.path.basename(tgz_path)} …')
    with tarfile.open(tgz_path, 'r:gz') as tar:
        tar.extractall(path=out_dir)
    tifs = glob.glob(os.path.join(out_dir, '**/*.tif'), recursive=True) + \
           glob.glob(os.path.join(out_dir, '**/*.TIF'), recursive=True)
    for t in tifs:
        print(f'    → {os.path.basename(t)}')
    return tifs

cop_tifs  = extract_tgz(COP30_TGZ,  os.path.join(OUTPUT_DIR, 'cop30'))
srtm_tifs = extract_tgz(SRTM_TGZ,   os.path.join(OUTPUT_DIR, 'srtm'))

# Auto-select the first (or mosaic later if multiple tiles)
COP30_TIF  = cop_tifs[0]  if cop_tifs  else None
SRTM_TIF   = srtm_tifs[0] if srtm_tifs else None

print(f'\n  COP30 DEM  : {COP30_TIF}')
print(f'  SRTM  DEM  : {SRTM_TIF}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 4 ─ Mosaic if multiple tiles (auto)
# ─────────────────────────────────────────────────────────────
from rasterio.merge import merge

def mosaic_tifs(tif_list: list, out_path: str) -> str:
    """Merge multiple GeoTIFF tiles into one."""
    if not tif_list:
        return None
    if len(tif_list) == 1:
        return tif_list[0]   # single tile — no merge needed
    print(f'  Mosaicking {len(tif_list)} tiles → {os.path.basename(out_path)}')
    srcs = [rasterio.open(t) for t in tif_list]
    mosaic, transform = merge(srcs)
    profile = srcs[0].profile.copy()
    profile.update({'height': mosaic.shape[1], 'width': mosaic.shape[2],
                    'transform': transform, 'count': 1})
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(mosaic)
    [s.close() for s in srcs]
    return out_path

COP30_TIF = mosaic_tifs(cop_tifs,  os.path.join(OUTPUT_DIR, 'cop30_mosaic.tif'))
SRTM_TIF  = mosaic_tifs(srtm_tifs, os.path.join(OUTPUT_DIR, 'srtm_mosaic.tif'))

print(f'\n  ✅ COP30 ready : {COP30_TIF}')
print(f'  ✅ SRTM  ready : {SRTM_TIF}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 5 ─ Quick DEM preview
# ─────────────────────────────────────────────────────────────
def preview_dem(tif_path: str, title: str, ax):
    with rasterio.open(tif_path) as src:
        data = src.read(1).astype(float)
        nodata = src.nodata
        if nodata is not None:
            data[data == nodata] = np.nan
        extent = [src.bounds.left, src.bounds.right,
                  src.bounds.bottom, src.bounds.top]
    im = ax.imshow(data, cmap='terrain', extent=extent, origin='upper')
    ax.plot([LON1, LON2], [LAT1, LAT2], 'rv', ms=10, label='Pour Points')
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.colorbar(im, ax=ax, label='Elevation (m)')
    ax.legend()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
if COP30_TIF: preview_dem(COP30_TIF, 'Copernicus DEM GLO-30', axes[0])
if SRTM_TIF:  preview_dem(SRTM_TIF,  'SRTM GL1 30 m',         axes[1])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'dem_preview.png'), dpi=150)
plt.show()
```

---
## 💧 Section 2 — Watershed Delineation (pysheds)


```python
# ─────────────────────────────────────────────────────────────
# CELL 6 ─ Core delineation function
# ─────────────────────────────────────────────────────────────

def delineate_watershed(
    dem_path     : str,
    pour_lon     : float,
    pour_lat     : float,
    label        : str,
    acc_threshold: int  = 300,
    snap_radius  : float = 0.02,   # degrees to snap pour point
) -> tuple:
    """
    Delineate a watershed polygon using pysheds D8 routing.

    Returns
    -------
    gdf      : GeoDataFrame with watershed polygon (EPSG:4326)
    area_km2 : Watershed area in km²
    acc_arr  : Flow accumulation array (for stream mapping)
    fdir_arr : Flow direction array
    grid_obj : pysheds Grid object (for further operations)
    """
    print(f'\n═══ Delineating [{label}] ═══')
    print(f'    Pour point : {pour_lat:.5f}°N  {pour_lon:.5f}°E')
    print(f'    DEM        : {os.path.basename(dem_path)}')

    grid = Grid.from_raster(dem_path)
    dem  = grid.read_raster(dem_path)

    print('    Filling pits …')
    pit_filled = grid.fill_pits(dem)
    print('    Filling depressions …')
    flooded    = grid.fill_depressions(pit_filled)
    print('    Resolving flats …')
    inflated   = grid.resolve_flats(flooded)

    # D8 direction map (ESRI/HydroSHEDS convention)
    dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
    print('    Computing D8 flow direction …')
    fdir = grid.flowdir(inflated, dirmap=dirmap)

    print('    Computing flow accumulation …')
    acc  = grid.accumulation(fdir, dirmap=dirmap)

    print('    Snapping pour point to stream …')
    x_snap, y_snap = grid.snap_to_mask(
        acc > acc_threshold,
        (pour_lon, pour_lat)
    )
    print(f'    Snapped  →  {y_snap:.5f}°N  {x_snap:.5f}°E')

    print('    Delineating catchment …')
    catch = grid.catchment(
        x=x_snap, y=y_snap,
        fdir=fdir, dirmap=dirmap,
        xytype='coordinate'
    )

    # Clip grid to watershed
    grid.clip_to(catch)

    print('    Polygonising watershed …')
    polys = [shape(g) for g, v in grid.polygonize() if v == 1]
    if not polys:
        raise RuntimeError(
            f'No polygon for [{label}]. '
            'Try lowering acc_threshold (e.g. 100) or check pour point.')

    ws_geom = unary_union(polys)
    gdf = gpd.GeoDataFrame(
        {'name': [label], 'geometry': [ws_geom]},
        crs='EPSG:4326'
    )

    # Area in km² (UTM Zone 43N for Maharashtra)
    area_km2 = gdf.to_crs('EPSG:32643').geometry.area.values[0] / 1e6
    print(f'    ✅ Watershed area : {area_km2:.2f} km²')

    # Save outputs
    base = os.path.join(OUTPUT_DIR, label)
    gdf.to_file(base + '_watershed.shp')
    gdf.to_file(base + '_watershed.geojson', driver='GeoJSON')
    print(f'    Saved → {base}_watershed.geojson')

    return gdf, area_km2, acc, fdir, grid

print('✅ delineate_watershed() defined')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 7 ─ Run delineation for BOTH pour points
# Uses Copernicus DEM (preferred); falls back to SRTM
# ─────────────────────────────────────────────────────────────

DEM_FOR_DELINEATION = COP30_TIF or SRTM_TIF
print(f'Using DEM: {DEM_FOR_DELINEATION}\n')

# ── PP1 — Dehrang Dam Catchment ──────────────────────────────
ws1, area1, acc1, fdir1, grid1 = delineate_watershed(
    dem_path      = DEM_FOR_DELINEATION,
    pour_lon      = LON1,
    pour_lat      = LAT1,
    label         = 'pp1_dam_catchment',
    acc_threshold = 300,
)

# ── PP2 — River Basin Confluence ─────────────────────────────
ws2, area2, acc2, fdir2, grid2 = delineate_watershed(
    dem_path      = DEM_FOR_DELINEATION,
    pour_lon      = LON2,
    pour_lat      = LAT2,
    label         = 'pp2_river_basin',
    acc_threshold = 300,
)

print(f'\n  PP1 Area : {area1:.2f} km²')
print(f'  PP2 Area : {area2:.2f} km²')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 8 ─ Plot both watersheds
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

def plot_watershed(ws_gdf, pp_lat, pp_lon, acc_arr, title, ax):
    ws_gdf.plot(ax=ax, facecolor='#4fc3f7', edgecolor='#0277bd',
                linewidth=1.5, alpha=0.6)
    # Stream network (flow acc > 100)
    try:
        stream_mask = acc_arr > 100
        ax.contour(np.flipud(stream_mask.astype(float)), levels=[0.5],
                   colors='#1565c0', linewidths=0.4, alpha=0.7)
    except Exception:
        pass
    ax.plot(pp_lon, pp_lat, 'r^', ms=12, zorder=5, label='Pour Point')
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend()
    ax.grid(True, alpha=0.3)

plot_watershed(ws1, LAT1, LON1, acc1, f'PP1 — Dam Catchment  ({area1:.1f} km²)', axes[0])
plot_watershed(ws2, LAT2, LON2, acc2, f'PP2 — River Basin    ({area2:.1f} km²)', axes[1])

plt.suptitle('Dehrang Dam Break — Watershed Delineation', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'watersheds.png'), dpi=150, bbox_inches='tight')
plt.show()
```

---
## 🛰️ Section 3 — ESA WorldCover 2021 LULC

> **Option A** — Google Earth Engine *(recommended; needs GEE auth)*  
> **Option B** — ESA STAC API download *(no auth, slower download)*  
> Run whichever option works for you.


```python
# ─────────────────────────────────────────────────────────────
# CELL 9 ─ Option A: GEE WorldCover export
# ─────────────────────────────────────────────────────────────
USE_GEE = True   # ← Set to False to skip GEE and use STAC instead

WORLDCOVER_TIF = os.path.join(OUTPUT_DIR, 'esa_worldcover_10m.tif')

if USE_GEE and not os.path.exists(WORLDCOVER_TIF):
    try:
        import ee, geemap
        ee.Authenticate()
        ee.Initialize(project=GEE_PROJECT)

        roi = ee.Geometry.BBox(BBOX[0], BBOX[1], BBOX[2], BBOX[3])

        wc = (ee.ImageCollection('ESA/WorldCover/v200')
              .first()
              .select('Map')
              .clip(roi))

        geemap.ee_export_image(
            wc,
            filename   = WORLDCOVER_TIF,
            scale      = 10,
            region     = roi,
            file_per_band = False,
        )
        print(f'✅ GEE WorldCover saved → {WORLDCOVER_TIF}')

    except Exception as e:
        print(f'⚠️  GEE failed: {e}')
        print('   → Falling back to STAC API (Cell 10)')
        USE_GEE = False

elif os.path.exists(WORLDCOVER_TIF):
    print(f'✅ WorldCover already exists: {WORLDCOVER_TIF}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 10 ─ Option B: ESA WorldCover via STAC API
# Downloads tiles that intersect the bounding box directly
# ─────────────────────────────────────────────────────────────
import io
from rasterio.merge import merge as rio_merge

def download_worldcover_stac(bbox: tuple, out_path: str):
    """
    Download ESA WorldCover 2021 tiles via the ESA WorldCover STAC API.
    bbox = (west, south, east, north)
    """
    if os.path.exists(out_path):
        print(f'  WorldCover already downloaded: {out_path}')
        return out_path

    print('  Querying ESA WorldCover STAC …')
    stac_url = 'https://services.terrascope.be/stac/v1/search'
    payload = {
        'collections': ['urn:eop:VITO:ESA_WorldCover_10m_2021_V2_AWS_S3'],
        'bbox': list(bbox),
        'limit': 50,
    }
    r = requests.post(stac_url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f'  STAC error {r.status_code}')
        return None

    features = r.json().get('features', [])
    print(f'  Found {len(features)} tile(s)')

    tile_paths = []
    for feat in features:
        # Get the Map band URL
        href = feat['assets'].get('Map', feat['assets'].get('map', {})).get('href', '')
        if not href:
            continue
        tile_name = os.path.join(OUTPUT_DIR, f'wc_{feat["id"]}.tif')
        if os.path.exists(tile_name):
            tile_paths.append(tile_name)
            continue
        print(f'  Downloading {os.path.basename(href)} …')
        tr = requests.get(href, timeout=120)
        if tr.status_code == 200:
            with open(tile_name, 'wb') as f:
                f.write(tr.content)
            tile_paths.append(tile_name)
        else:
            print(f'  ⚠️  Could not download tile: {tr.status_code}')

    if not tile_paths:
        print('  No tiles downloaded.')
        return None

    if len(tile_paths) == 1:
        os.rename(tile_paths[0], out_path)
        return out_path

    print('  Merging tiles …')
    srcs = [rasterio.open(t) for t in tile_paths]
    mosaic, transform = rio_merge(srcs)
    profile = srcs[0].profile.copy()
    profile.update({'height': mosaic.shape[1], 'width': mosaic.shape[2],
                    'transform': transform, 'count': 1})
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(mosaic)
    [s.close() for s in srcs]
    print(f'  ✅ Saved → {out_path}')
    return out_path

if not os.path.exists(WORLDCOVER_TIF):
    WORLDCOVER_TIF = download_worldcover_stac(BBOX, WORLDCOVER_TIF)

print(f'\n✅ WorldCover TIF: {WORLDCOVER_TIF}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 11 ─ Resample WorldCover to 30 m to match DEM
# ─────────────────────────────────────────────────────────────

LULC_30M_TIF = os.path.join(OUTPUT_DIR, 'lulc_30m.tif')

def resample_to_reference(src_tif: str, ref_tif: str, out_tif: str,
                           resample_method=Resampling.nearest) -> str:
    """Resample src_tif to the spatial reference/resolution of ref_tif."""
    with rasterio.open(ref_tif) as ref:
        ref_transform = ref.transform
        ref_width  = ref.width
        ref_height = ref.height
        ref_crs    = ref.crs
        ref_bounds = ref.bounds

    with rasterio.open(src_tif) as src:
        data = np.empty((1, ref_height, ref_width), dtype=src.dtypes[0])
        rasterio.warp.reproject(
            source      = rasterio.band(src, 1),
            destination = data,
            src_transform  = src.transform,
            src_crs        = src.crs,
            dst_transform  = ref_transform,
            dst_crs        = ref_crs,
            resampling     = resample_method,
        )
        profile = src.profile.copy()
        profile.update({
            'height': ref_height, 'width': ref_width,
            'transform': ref_transform, 'crs': ref_crs, 'count': 1,
        })
    with rasterio.open(out_tif, 'w', **profile) as dst:
        dst.write(data)
    print(f'  ✅ Resampled → {os.path.basename(out_tif)}')
    return out_tif

if WORLDCOVER_TIF and not os.path.exists(LULC_30M_TIF):
    resample_to_reference(WORLDCOVER_TIF, DEM_FOR_DELINEATION,
                          LULC_30M_TIF, Resampling.nearest)
elif os.path.exists(LULC_30M_TIF):
    print(f'✅ LULC 30 m already exists: {LULC_30M_TIF}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 12 ─ LULC class definitions & colour map
# ─────────────────────────────────────────────────────────────
WC_CLASSES = {
    10 : ('Tree cover',          '#006400'),
    20 : ('Shrubland',           '#ffbb22'),
    30 : ('Grassland',           '#ffff4c'),
    40 : ('Cropland',            '#f096ff'),
    50 : ('Built-up',            '#fa0000'),
    60 : ('Bare / sparse veg',   '#b4b4b4'),
    70 : ('Snow and ice',        '#f0f0f0'),
    80 : ('Permanent water',     '#0064c8'),
    90 : ('Herbaceous wetland',  '#0096a0'),
    95 : ('Mangroves',           '#00cf75'),
   100 : ('Moss and lichen',     '#fae6a0'),
}

if LULC_30M_TIF and os.path.exists(LULC_30M_TIF):
    with rasterio.open(LULC_30M_TIF) as src:
        lulc_arr = src.read(1)
        lulc_meta = src.meta

    # Colour-code for display
    rgb = np.zeros((lulc_arr.shape[0], lulc_arr.shape[1], 3), dtype=np.uint8)
    for cls, (name, hexcol) in WC_CLASSES.items():
        r,g,b = tuple(int(hexcol.lstrip('#')[i:i+2],16) for i in (0,2,4))
        rgb[lulc_arr == cls] = [r,g,b]

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.imshow(rgb, origin='upper')
    ax.set_title('ESA WorldCover 2021 — 30 m resampled', fontsize=12)
    patches = [mpatches.Patch(color=h, label=n)
               for c,(n,h) in WC_CLASSES.items() if c in np.unique(lulc_arr)]
    ax.legend(handles=patches, bbox_to_anchor=(1.02, 1), loc='upper left',
              fontsize=8, framealpha=0.8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'lulc_preview.png'), dpi=150, bbox_inches='tight')
    plt.show()
else:
    print('⚠️  LULC not available — skipping preview')
```

---
## 🌍 Section 4 — Hydrologic Soil Group (HSG) via SoilGrids v2

> SoilGrids is **free** and **global** (covers India). No API key needed.  
> We derive HSG from clay & sand % at 0–30 cm using USDA NRCS thresholds.


```python
# ─────────────────────────────────────────────────────────────
# CELL 13 ─ SoilGrids REST API — point query (validation)
# ─────────────────────────────────────────────────────────────

def soilgrids_point_query(lon: float, lat: float,
                           properties: list = None) -> dict:
    """Query SoilGrids v2 REST API at a single point."""
    if properties is None:
        properties = ['clay', 'sand', 'silt']
    url = 'https://rest.isric.org/soilgrids/v2.0/properties/query'
    params = {
        'lon'     : lon,
        'lat'     : lat,
        'property': properties,
        'depth'   : ['0-5cm', '5-15cm', '15-30cm'],
        'value'   : ['mean'],
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            print(f'  SoilGrids error: {r.status_code}')
            return {}
    except Exception as e:
        print(f'  SoilGrids request failed: {e}')
        return {}

def parse_soilgrids(data: dict) -> dict:
    """Extract mean clay/sand by depth from SoilGrids response."""
    result = {}
    for layer in data.get('properties', {}).get('layers', []):
        prop = layer['name']
        for d in layer['depths']:
            key = f"{prop}_{d['label']}"
            result[key] = d['values']['mean']
    return result

print('Querying SoilGrids at PP1 (dam) …')
sg1 = parse_soilgrids(soilgrids_point_query(LON1, LAT1))
print('Querying SoilGrids at PP2 (confluence) …')
sg2 = parse_soilgrids(soilgrids_point_query(LON2, LAT2))

print('\n  Property               PP1 (Dam)   PP2 (Confluence)')
print('  ─' * 28)
for k in sg1:
    print(f'  {k:<25} {sg1.get(k,"N/A"):>10}   {sg2.get(k,"N/A"):>14}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 14 ─ SoilGrids raster HSG via WCS
# Downloads clay_0-5cm, 5-15cm, 15-30cm rasters and computes HSG
# ─────────────────────────────────────────────────────────────

HSG_TIF = os.path.join(OUTPUT_DIR, 'hsg_30m.tif')

def get_soilgrids_wcs(prop: str, depth: str, bbox: tuple, out_tif: str,
                       width: int = 300, height: int = 300) -> str:
    """
    Download a SoilGrids raster via WCS.
    prop  : 'clay', 'sand', 'silt'
    depth : '0-5cm', '5-15cm', '15-30cm'
    """
    if os.path.exists(out_tif):
        return out_tif

    # SoilGrids uses Homolosine projection internally; query in EPSG:4326 bbox
    url = 'https://maps.isric.org/mapserv'
    params = {
        'map'        : f'/map/{prop}.map',
        'SERVICE'    : 'WCS',
        'VERSION'    : '2.0.1',
        'REQUEST'    : 'GetCoverage',
        'COVERAGEID' : f'{prop}_{depth}_mean',
        'FORMAT'     : 'image/tiff',
        'SUBSET'     : [
            f'long({bbox[0]},{bbox[2]})',
            f'lat({bbox[1]},{bbox[3]})',
        ],
        'SUBSETTINGCRS': 'http://www.opengis.net/def/crs/EPSG/0/4326',
        'OUTPUTCRS'    : 'http://www.opengis.net/def/crs/EPSG/0/4326',
    }
    print(f'  WCS: {prop}_{depth}_mean …', end=' ')
    try:
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(out_tif, 'wb') as f:
                f.write(r.content)
            print(f'✓ {len(r.content)/1e3:.0f} kB')
            return out_tif
        else:
            print(f'✗ ({r.status_code})')
            return None
    except Exception as e:
        print(f'✗ {e}')
        return None


def build_hsg_raster(bbox: tuple, ref_tif: str, out_tif: str) -> str:
    """
    Build Hydrologic Soil Group raster from SoilGrids clay+sand.
    Returns path to HSG GeoTIFF (values 1=A, 2=B, 3=C, 4=D).
    """
    if os.path.exists(out_tif):
        print(f'  HSG already exists: {out_tif}')
        return out_tif

    depths     = ['0-5cm', '5-15cm', '15-30cm']
    thicknesses= [5, 10, 15]
    total      = sum(thicknesses)

    clay_wt = None
    sand_wt = None
    ref_meta = None

    with rasterio.open(ref_tif) as ref:
        ref_meta = ref.meta.copy()
        ref_transform = ref.transform
        ref_crs = ref.crs
        ref_shape = (ref.height, ref.width)

    for prop, store in [('clay', 'clay_wt'), ('sand', 'sand_wt')]:
        weighted = np.zeros(ref_shape, dtype=np.float32)
        valid_sum = 0
        for depth, wt in zip(depths, thicknesses):
            tmp = os.path.join(OUTPUT_DIR, f'{prop}_{depth.replace("-","_")}_sg.tif')
            path = get_soilgrids_wcs(prop, depth, bbox, tmp)
            if path and os.path.exists(path):
                with rasterio.open(path) as src:
                    arr = np.empty(ref_shape, dtype=np.float32)
                    rasterio.warp.reproject(
                        source=rasterio.band(src,1), destination=arr,
                        src_transform=src.transform, src_crs=src.crs,
                        dst_transform=ref_transform, dst_crs=ref_crs,
                        resampling=Resampling.bilinear
                    )
                arr[arr < 0] = 0
                weighted += arr * wt
                valid_sum += wt

        if valid_sum > 0:
            if prop == 'clay': clay_wt = weighted / valid_sum / 10.0  # g/kg → %
            else: sand_wt = weighted / valid_sum / 10.0

    if clay_wt is None:
        print('  ⚠️  SoilGrids WCS failed — using default HSG=C (typical for Maharashtra)')
        clay_wt = np.full(ref_shape, 25.0)   # ~25% clay → HSG C
        sand_wt = np.full(ref_shape, 30.0)

    # USDA NRCS HSG classification
    hsg = np.full(ref_shape, 4, dtype=np.uint8)           # D default
    hsg[clay_wt < 35] = 3                                  # C
    hsg[clay_wt < 20] = 2                                  # B
    hsg[(clay_wt < 10) & (sand_wt >= 70)] = 1             # A

    ref_meta.update({'dtype': 'uint8', 'nodata': 0, 'count': 1})
    with rasterio.open(out_tif, 'w', **ref_meta) as dst:
        dst.write(hsg[np.newaxis, :, :])

    print(f'  ✅ HSG saved → {out_tif}')

    # Summary stats
    unique, counts = np.unique(hsg[hsg > 0], return_counts=True)
    total_px = counts.sum()
    hsg_names = {1:'A (High inf.)', 2:'B (Mod. inf.)', 3:'C (Low inf.)', 4:'D (Very low)'}
    print('  HSG distribution:')
    for u, c in zip(unique, counts):
        print(f'    HSG {hsg_names.get(u,u)}: {c/total_px*100:.1f}%')

    return out_tif

HSG_TIF = build_hsg_raster(BBOX, DEM_FOR_DELINEATION, HSG_TIF)
```

---
## 📊 Section 5 — Curve Number Grid (AMC II)


```python
# ─────────────────────────────────────────────────────────────
# CELL 15 ─ CN lookup table (NRCS TR-55 / NEH-630)
# {ESA class: [CN_A, CN_B, CN_C, CN_D]}
# ─────────────────────────────────────────────────────────────

CN_TABLE = {
    10 : [30,  55,  70,  77],   # Tree cover         (good condition forest)
    20 : [35,  56,  70,  77],   # Shrubland
    30 : [30,  58,  71,  78],   # Grassland          (meadow, good condition)
    40 : [67,  78,  85,  89],   # Cropland           (row crops, contoured)
    50 : [98,  98,  98,  98],   # Built-up           (impervious)
    60 : [77,  86,  91,  94],   # Bare / sparse veg  (fallow)
    70 : [100, 100, 100, 100],  # Snow and ice
    80 : [100, 100, 100, 100],  # Permanent water
    90 : [78,  78,  78,  78],   # Herbaceous wetland
    95 : [78,  78,  78,  78],   # Mangroves
   100 : [30,  58,  71,  78],   # Moss and lichen
}

MANNINGS_TABLE = {
    10 : 0.120,   # Tree cover (dense forest)
    20 : 0.060,   # Shrubland
    30 : 0.035,   # Grassland
    40 : 0.050,   # Cropland
    50 : 0.014,   # Built-up (concrete/asphalt)
    60 : 0.025,   # Bare / sparse veg
    70 : 0.010,   # Snow / ice
    80 : 0.028,   # Open water
    90 : 0.070,   # Herbaceous wetland
    95 : 0.085,   # Mangroves
   100 : 0.040,   # Moss and lichen
}

print(f'  {"ESA Class":<28} {"CN_A":>5} {"CN_B":>5} {"CN_C":>5} {"CN_D":>5}   n')
print('  ' + '─'*55)
for cls, (a,b,c,d) in CN_TABLE.items():
    name = WC_CLASSES.get(cls, ('?',''))[0]
    n    = MANNINGS_TABLE.get(cls, 0)
    print(f'  {name:<28} {a:>5} {b:>5} {c:>5} {d:>5}   {n:.3f}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 16 ─ Build CN grid (AMC II) and Manning's n grid
# ─────────────────────────────────────────────────────────────

CN_TIF        = os.path.join(OUTPUT_DIR, 'cn_amc2_30m.tif')
CN_I_TIF      = os.path.join(OUTPUT_DIR, 'cn_amc1_30m.tif')
CN_III_TIF    = os.path.join(OUTPUT_DIR, 'cn_amc3_30m.tif')
MANNINGS_TIF  = os.path.join(OUTPUT_DIR, 'mannings_n_30m.tif')

def build_cn_mannings(lulc_tif: str, hsg_tif: str,
                       cn_table: dict, n_table: dict):
    """Build pixel-wise CN (AMC I/II/III) and Manning's n from LULC + HSG."""

    with rasterio.open(lulc_tif) as src:
        lulc = src.read(1).astype(np.int16)
        meta = src.meta.copy()

    with rasterio.open(hsg_tif) as src:
        hsg_raw = src.read(1).astype(np.int16)

    # Resample HSG to LULC shape if they differ
    if hsg_raw.shape != lulc.shape:
        hsg = np.empty(lulc.shape, dtype=np.float32)
        with rasterio.open(hsg_tif) as src:
            rasterio.warp.reproject(
                source=rasterio.band(src,1), destination=hsg,
                src_transform=src.transform, src_crs=src.crs,
                dst_transform=meta['transform'], dst_crs=meta['crs'],
                resampling=Resampling.nearest
            )
        hsg = hsg.astype(np.int16)
    else:
        hsg = hsg_raw

    # Default HSG = C (3) where soil data is missing
    hsg[hsg == 0] = 3
    hsg = np.clip(hsg, 1, 4)

    cn  = np.full(lulc.shape, 75.0, dtype=np.float32)  # default CN
    n_arr = np.full(lulc.shape, 0.035, dtype=np.float32)

    for cls, (cn_a, cn_b, cn_c, cn_d) in cn_table.items():
        mask = (lulc == cls)
        cn_vals = np.array([cn_a, cn_b, cn_c, cn_d])
        cn[mask] = cn_vals[hsg[mask] - 1]

    for cls, n_val in n_table.items():
        n_arr[lulc == cls] = n_val

    cn = np.clip(cn, 1, 100)

    # AMC I and AMC III (Chow et al. 1988)
    cn_i   = (4.2 * cn) / (10 - 0.058 * cn)
    cn_iii = (23 * cn)  / (10 + 0.13  * cn)
    cn_i   = np.clip(cn_i,   1, 100)
    cn_iii = np.clip(cn_iii, 1, 100)

    float_meta = meta.copy()
    float_meta.update({'dtype': 'float32', 'nodata': -9999, 'count': 1})

    def save(arr, path):
        with rasterio.open(path, 'w', **float_meta) as dst:
            dst.write(arr[np.newaxis, :, :])
        print(f'  ✅ {os.path.basename(path)}')

    save(cn,     CN_TIF)
    save(cn_i,   CN_I_TIF)
    save(cn_iii, CN_III_TIF)
    save(n_arr,  MANNINGS_TIF)

    return cn, cn_i, cn_iii, n_arr

if (LULC_30M_TIF and os.path.exists(LULC_30M_TIF) and
    HSG_TIF and os.path.exists(HSG_TIF)):
    cn_arr, cn1_arr, cn3_arr, n_arr = build_cn_mannings(
        LULC_30M_TIF, HSG_TIF, CN_TABLE, MANNINGS_TABLE
    )
else:
    print('⚠️  LULC or HSG not available — skipping CN/Manning build')
    cn_arr = cn1_arr = cn3_arr = n_arr = None
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 17 ─ Plot CN and Manning's n
# ─────────────────────────────────────────────────────────────
if cn_arr is not None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    im1 = axes[0].imshow(cn_arr, cmap='RdYlGn_r', vmin=30, vmax=100, origin='upper')
    axes[0].set_title('Curve Number — AMC II', fontsize=11)
    plt.colorbar(im1, ax=axes[0], label='CN')

    im2 = axes[1].imshow(n_arr, cmap='Blues', vmin=0.01, vmax=0.14, origin='upper')
    axes[1].set_title("Manning's n Roughness", fontsize=11)
    plt.colorbar(im2, ax=axes[1], label="Manning's n")

    plt.suptitle('Dehrang Dam — CN (AMC II) and Manning\'s n', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'cn_mannings_preview.png'),
                dpi=150, bbox_inches='tight')
    plt.show()

    mean_cn = np.nanmean(cn_arr[cn_arr > 0])
    mean_n  = np.nanmean(n_arr[n_arr > 0])
    print(f'  Domain mean CN  (AMC II): {mean_cn:.1f}')
    print(f'  Domain mean Manning\'s n : {mean_n:.4f}')
```

---
## 📐 Section 6 — Zonal Statistics per Watershed


```python
# ─────────────────────────────────────────────────────────────
# CELL 18 ─ Zonal stats (CN, n, LULC area) per watershed
# ─────────────────────────────────────────────────────────────
from rasterstats import zonal_stats

def watershed_summary(ws_gdf: gpd.GeoDataFrame, label: str,
                       area_km2: float) -> dict:
    stats = {'label': label, 'area_km2': round(area_km2, 2)}

    # Mean CN AMC II
    if os.path.exists(CN_TIF):
        z = zonal_stats(ws_gdf, CN_TIF, stats=['mean','min','max'],
                        all_touched=True)
        stats.update({'CN_mean': round(z[0]['mean'],1),
                      'CN_min':  round(z[0]['min'],1),
                      'CN_max':  round(z[0]['max'],1)})

    # Mean Manning's n
    if os.path.exists(MANNINGS_TIF):
        z = zonal_stats(ws_gdf, MANNINGS_TIF, stats=['mean'],
                        all_touched=True)
        stats['n_mean'] = round(z[0]['mean'], 4)

    # LULC breakdown
    if LULC_30M_TIF and os.path.exists(LULC_30M_TIF):
        z = zonal_stats(ws_gdf, LULC_30M_TIF, categorical=True,
                        all_touched=True)
        cat = z[0]
        total = sum(cat.values()) or 1
        lulc_pct = {
            WC_CLASSES.get(int(k),('Unknown',''))[0]: round(v/total*100,1)
            for k,v in cat.items() if k is not None
        }
        stats['lulc_pct'] = lulc_pct

    # DEM stats
    z = zonal_stats(ws_gdf, DEM_FOR_DELINEATION,
                    stats=['mean','min','max'], all_touched=True)
    stats.update({'elev_mean_m': round(z[0]['mean'],1),
                  'elev_min_m':  round(z[0]['min'],1),
                  'elev_max_m':  round(z[0]['max'],1)})

    return stats

st1 = watershed_summary(ws1, 'PP1 — Dam Catchment', area1)
st2 = watershed_summary(ws2, 'PP2 — River Basin',   area2)

for st in [st1, st2]:
    print(f'\n  ════ {st["label"]} ════')
    print(f'  Area           : {st["area_km2"]} km²')
    print(f'  Elevation      : {st.get("elev_min_m","?")} – {st.get("elev_max_m","?")} m  '
          f'(mean {st.get("elev_mean_m","?")})' )
    print(f'  Mean CN AMC II : {st.get("CN_mean","N/A")}')
    print(f'  Mean Manning n : {st.get("n_mean","N/A")}')
    if 'lulc_pct' in st:
        print('  LULC breakdown :')
        for cls, pct in sorted(st['lulc_pct'].items(), key=lambda x: -x[1]):
            bar = '█' * int(pct/3)
            print(f'    {cls:<28} {pct:>5.1f}%  {bar}')
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 19 ─ Save summary to CSV
# ─────────────────────────────────────────────────────────────
rows = []
for st in [st1, st2]:
    row = {k: v for k, v in st.items() if k != 'lulc_pct'}
    if 'lulc_pct' in st:
        for cls, pct in st['lulc_pct'].items():
            row[f'LULC_{cls}_%'] = pct
    rows.append(row)

df_stats = pd.DataFrame(rows)
csv_path = os.path.join(OUTPUT_DIR, 'watershed_summary.csv')
df_stats.to_csv(csv_path, index=False)
print(f'✅ Summary saved → {csv_path}')
df_stats
```

---
## 🗺️ Section 7 — Interactive Folium Map


```python
# ─────────────────────────────────────────────────────────────
# CELL 20 ─ Build interactive Folium map
# ─────────────────────────────────────────────────────────────
import folium
from folium import plugins, raster_layers
import base64
import io as _io

map_center = [(LAT1+LAT2)/2, (LON1+LON2)/2]
m = folium.Map(location=map_center, zoom_start=11,
               tiles='CartoDB positron')

# Add basemap options
folium.TileLayer('OpenStreetMap',  name='OpenStreetMap').add_to(m)
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='Google Satellite'
).add_to(m)

# ── Watershed polygons ────────────────────────────────────────
folium.GeoJson(
    ws1.__geo_interface__,
    name='PP1 — Dam Catchment',
    style_function=lambda x: {
        'fillColor': '#4fc3f7', 'color': '#0277bd',
        'weight': 2.5, 'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(['name'])
).add_to(m)

folium.GeoJson(
    ws2.__geo_interface__,
    name='PP2 — River Basin',
    style_function=lambda x: {
        'fillColor': '#ef9a9a', 'color': '#c62828',
        'weight': 2.5, 'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(['name'])
).add_to(m)

# ── Pour point markers ────────────────────────────────────────
pp1_popup = folium.Popup(
    f'<b>PP1 — Dehrang Dam</b><br>'
    f'Lat: {LAT1:.5f}°N<br>Lon: {LON1:.5f}°E<br>'
    f'Area: {area1:.2f} km²<br>'
    f'Mean CN: {st1.get("CN_mean","N/A")}<br>'
    f'Mean n: {st1.get("n_mean","N/A")}',
    max_width=220
)
folium.Marker(
    [LAT1, LON1], popup=pp1_popup, tooltip='PP1 — Dam',
    icon=folium.Icon(color='red', icon='tint', prefix='fa')
).add_to(m)

pp2_popup = folium.Popup(
    f'<b>PP2 — River Confluence</b><br>'
    f'Lat: {LAT2:.5f}°N<br>Lon: {LON2:.5f}°E<br>'
    f'Area: {area2:.2f} km²<br>'
    f'Mean CN: {st2.get("CN_mean","N/A")}<br>'
    f'Mean n: {st2.get("n_mean","N/A")}',
    max_width=220
)
folium.Marker(
    [LAT2, LON2], popup=pp2_popup, tooltip='PP2 — Confluence',
    icon=folium.Icon(color='blue', icon='tint', prefix='fa')
).add_to(m)

# ── LULC legend ───────────────────────────────────────────────
legend_html = '''
<div style="position: fixed; bottom:30px; right:30px; z-index:9999;
            background:white; padding:10px; border-radius:8px;
            border:1px solid #ccc; font-size:11px; line-height:1.6">
<b>ESA WorldCover</b><br>
'''
for cls, (name, color) in WC_CLASSES.items():
    legend_html += f'<span style="background:{color};display:inline-block;width:12px;height:12px;margin-right:4px;"></span>{name}<br>'
legend_html += '</div>'
m.get_root().html.add_child(folium.Element(legend_html))

# ── Summary table popup ───────────────────────────────────────
folium.LayerControl(collapsed=False).add_to(m)
plugins.MeasureControl(position='topleft').add_to(m)
plugins.MousePosition().add_to(m)
plugins.Fullscreen().add_to(m)

map_path = os.path.join(OUTPUT_DIR, 'dehrang_dam_interactive_map.html')
m.save(map_path)
print(f'✅ Interactive map saved → {map_path}')
m   # Display inline in Jupyter
```

---
## 🌐 Section 8 — Optional: GEE Extra Layers (geemap)

Run this cell only if you have a GEE project. It adds slope, hillshade, and flow accumulation layers.


```python
# ─────────────────────────────────────────────────────────────
# CELL 21 ─ GEE geemap advanced layers (OPTIONAL)
# ─────────────────────────────────────────────────────────────
GEE_MAP_ENABLED = False   # ← Set True if you have GEE access

if GEE_MAP_ENABLED:
    import ee, geemap
    try:
        ee.Authenticate()
        ee.Initialize(project=GEE_PROJECT)

        roi = ee.Geometry.BBox(BBOX[0], BBOX[1], BBOX[2], BBOX[3])
        MAP_CENTER = [(LAT1+LAT2)/2, (LON1+LON2)/2]

        gMap = geemap.Map(center=MAP_CENTER, zoom=11)
        gMap.add_basemap('HYBRID')

        # DEMs
        srtm     = ee.Image('USGS/SRTMGL1_003').select('elevation').clip(roi)
        cop_dem  = ee.ImageCollection('COPERNICUS/DEM/GLO30').select('DEM').mosaic().clip(roi)
        slope    = ee.Terrain.slope(srtm).clip(roi)
        hillshade= ee.Terrain.hillshade(srtm).clip(roi)

        # HydroSHEDS
        flow_acc  = ee.Image('WWF/HydroSHEDS/03ACC').clip(roi)
        streams   = flow_acc.gte(500).selfMask()

        # WorldCover
        worldcover = ee.ImageCollection('ESA/WorldCover/v200').first().clip(roi)

        VIS_DEM   = {'min':0,'max':900,'palette':
                     ['#313695','#4575b4','#74add1','#abd9e9',
                      '#ffffbf','#fdae61','#f46d43','#d73027','#a50026']}
        VIS_SLOPE = {'min':0,'max':50,
                     'palette':['white','#ffffb2','#fd8d3c','#bd0026']}

        gMap.addLayer(cop_dem,  VIS_DEM,   'Copernicus DEM GLO-30', True)
        gMap.addLayer(srtm,     VIS_DEM,   'SRTM 30 m', False)
        gMap.addLayer(slope,    VIS_SLOPE, 'Slope (°)', False)
        gMap.addLayer(hillshade,{'min':0,'max':255},'Hillshade', False)
        gMap.addLayer(flow_acc.log10(),
                      {'min':0,'max':4,'palette':['white','#6baed6','#084594']},
                      'Flow Accumulation (log10)', False)
        gMap.addLayer(streams,  {'palette':['0000FF']},'Streams (FA≥500)', True)
        gMap.addLayer(worldcover,{}, 'ESA WorldCover 2021', True)

        # Pour points
        gMap.addLayer(ee.Geometry.Point([LON1, LAT1]),
                      {'color':'FF0000'}, 'PP1 — Dam')
        gMap.addLayer(ee.Geometry.Point([LON2, LAT2]),
                      {'color':'0000FF'}, 'PP2 — Confluence')

        gMap.addLayerControl()
        gMap

    except Exception as e:
        print(f'⚠️  GEE map failed: {e}')
else:
    print('GEE map skipped (GEE_MAP_ENABLED=False)')
```

---
## 📤 Section 9 — Final Outputs & HEC-HMS / HEC-RAS Prep


```python
# ─────────────────────────────────────────────────────────────
# CELL 22 ─ Slope raster from local DEM
# ─────────────────────────────────────────────────────────────
from scipy.ndimage import generic_gradient_magnitude, gaussian_filter

SLOPE_TIF = os.path.join(OUTPUT_DIR, 'slope_deg_30m.tif')

def compute_slope_local(dem_tif: str, out_tif: str) -> str:
    """Compute slope in degrees from a DEM GeoTIFF."""
    if os.path.exists(out_tif):
        print(f'  Slope already exists: {out_tif}')
        return out_tif
    with rasterio.open(dem_tif) as src:
        dem_data = src.read(1).astype(np.float32)
        cell_size = abs(src.transform.a)  # degrees per pixel
        meta = src.meta.copy()
        nodata = src.nodata

    if nodata is not None:
        dem_data[dem_data == nodata] = np.nan

    # Convert cell size from degrees to metres (~111 km/degree at equator)
    cell_m = cell_size * 111_000

    dy, dx = np.gradient(dem_data, cell_m, cell_m)
    slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))
    slope = np.clip(slope, 0, 90).astype(np.float32)

    meta.update({'dtype': 'float32', 'nodata': -9999, 'count': 1})
    with rasterio.open(out_tif, 'w', **meta) as dst:
        dst.write(slope[np.newaxis, :, :])
    print(f'  ✅ Slope → {out_tif}')
    return out_tif

SLOPE_TIF = compute_slope_local(DEM_FOR_DELINEATION, SLOPE_TIF)
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 23 ─ HEC-HMS parameter summary
# ─────────────────────────────────────────────────────────────
print('═' * 62)
print('  HEC-HMS INPUT PARAMETERS')
print('═' * 62)

for label, st, area, ws_gdf in [
    ('PP1 — Dam Catchment', st1, area1, ws1),
    ('PP2 — River Basin',   st2, area2, ws2),
]:
    # Lag time (minutes) — SCS method: tlag = 0.6 * tc
    # Kirpich formula: tc = 0.0195 * L^0.77 * S^-0.385  (L in m, S unitless)
    # We use a simplified estimate here — refine with actual channel data
    elev_diff = st.get('elev_max_m', 400) - st.get('elev_min_m', 50)
    L_m       = math.sqrt(area * 1e6)   # approx basin length
    S_frac    = elev_diff / L_m
    tc_hr     = 0.0195 * (L_m**0.77) * max(S_frac, 1e-4)**-0.385 / 3600
    tlag_min  = 0.6 * tc_hr * 60

    print(f'\n  [{label}]')
    print(f'    Basin area          : {area:.2f} km²  ({area*100:.0f} ha)')
    print(f'    Elev range          : {st.get("elev_min_m","?")} – '
          f'{st.get("elev_max_m","?")} m')
    print(f'    Mean CN (AMC II)    : {st.get("CN_mean","N/A")}')
    print(f'    Estimated tc        : {tc_hr*60:.1f} min  ({tc_hr:.2f} hr)')
    print(f'    SCS Lag time        : {tlag_min:.1f} min')
    print(f'    Mean Manning\'s n   : {st.get("n_mean","N/A")}')

print('\n  Note: tc is estimated via Kirpich formula.')
print('        Validate with actual stream length and survey data.')
print('═' * 62)
```


```python
# ─────────────────────────────────────────────────────────────
# CELL 24 ─ List all output files
# ─────────────────────────────────────────────────────────────
print(f'\n📁  OUTPUT FILES  →  {OUTPUT_DIR}/')
print('─' * 60)
for f in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, f)
    size  = os.path.getsize(fpath)
    unit  = 'kB' if size < 1e6 else 'MB'
    val   = size/1e3 if size < 1e6 else size/1e6
    print(f'  {f:<45}  {val:6.1f} {unit}')

print('─' * 60)
print('''
NEXT STEPS — HEC-HMS
  • Import DEM (cop30 / srtm) into HEC-HMS GeoHMS plugin
  • Import watershed shapefiles as basin boundaries
  • Use Mean CN (AMC II) for SCS Curve Number loss method
  • Use Lag Time estimate for SCS Unit Hydrograph
  • Set IDF / design storm for return period (25yr / 100yr)

NEXT STEPS — HEC-RAS 2D
  • Import Copernicus DEM as terrain
  • Set Manning's n from mannings_n_30m.tif (land cover)
  • Define 2D flow area over inundation domain
  • Input dam break breach parameters:
      - Breach width, side slopes, formation time
      - Initial pool elevation from dam survey
  • Run unsteady 2D simulation → inundation map
''')
```
