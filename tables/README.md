# Hydrological & Dam Safety Data Tables

This directory contains tabular datasets for the Dehrang Dam Break Analysis.

## Directory Structure
- `input/`: Authoritative raw input tables directly collected from PMC surveys and IMD rainfall records.
- `output/`: Processed calculation workbooks and derived hydrological distributions.

> **Note on File Pairs:**
> Certain files in `input/` and `output/` (such as `Dehrang_Dam_Storage_Elevation_Table.xlsx`, `Dehrang_Storage_Elevation_Data.csv`, and `IDF_Design_Flood_Panvel_CORRECTED.xlsx`) currently share identical baselines. Both sets are deliberately retained: `input/` represents the static baseline data from field measurements, while `output/` provides the working target for automated re-computation scripts.
