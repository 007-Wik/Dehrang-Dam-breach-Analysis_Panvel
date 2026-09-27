# Hydrological & Dam Safety Data Tables

**Dehrang Dam Break Analysis — Panvel, Maharashtra**

* **Developer & Engineer:** Satwik Kamlakar Udupi, Agriculture Er.
* **Institution:** Centre for Climate Change and Sustainability Studies (CCCSS), Shivaji University, Kolhapur
* **Client / Sponsoring Authority:** Panvel Municipal Corporation, Government of Maharashtra

---

## Directory Structure

* **`output/`**: Derived engineering calculation workbooks and hydrological tables:
  * `Dehrang_Dam_Storage_Elevation_Table.xlsx` (16.5 KB) — Reservoir capacity and siltation analysis derived from 10×10 m sludge survey (3,193 boxes).
  * `Dehrang_Storage_Elevation_Data.csv` (2.5 KB) — 55 elevation increments (78.4 to 89.2 m MSL) with original/current area, volume, and percentage capacity loss.
  * `IDF_Design_Flood_Panvel_CORRECTED.xlsx` (153.7 KB) — Full 9-sheet hydrological frequency workbook: 31-yr IMD series (1992–2024), Gumbel EV-I, Lognormal, Grubbs outlier analysis, Kolmogorov-Smirnov test, sub-daily IDF matrix (15 min to 24 hr), and 100-yr design storm.
* **`input/`**: Authoritative raw input tables collected from PMC surveys and IMD rainfall records.

> **Note on File Pairs:**  
> Files in `output/` represent the validated engineering outputs derived from field measurements and statistical modeling, while `input/` retains the unedited raw field records. Both are preserved to ensure end-to-end scientific reproducibility.

