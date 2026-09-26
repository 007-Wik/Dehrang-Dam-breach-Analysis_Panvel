# 🏗️ Dehrang Dam — Reservoir Storage-Elevation Analysis
## Engineering Capacity Curve Notebook
---
| Parameter | Value |
|-----------|-------|
| **Dam Name** | DEHRANG |
| **Dam Type** | Earthen Dam with Automatic Gated Spillway |
| **Owner / Operator** | Panvel Municipal Corporation |
| **State / District** | Maharashtra / Raigad |
| **Commissioned** | 1957 |
| **Latitude** | 19° 1′ 54″ N |
| **Longitude** | 73° 14′ 32″ E |
| **FRL / MWL** | **89.15 m MSL** |
| **MDDL** | **80.77 m MSL** |
| **Spillway Crest Elevation** | **86.65 m MSL** |
| **Lowest River Bed Level** | 75.40 m MSL |
| **Survey Method** | 10×10 m Box Method Sludge Survey |
| **Total Boxes Surveyed** | 3,193 |
| **Total Sludge Volume** | 517,705.69 m³ (517.706 × 1,000 m³) |
| **Inspection Report** | Premonsoon-2025, Yash Engineering Consultant Pvt. Ltd., Navi Mumbai |

---
**This notebook derives and plots the Storage-Elevation table from sludge survey data.**
It computes original (pre-siltation) and current (post-siltation) reservoir capacity curves
using the trapezoidal integration method, and exports the results as a CSV.



```python
# ── Imports ─────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from IPython.display import display
import warnings
warnings.filterwarnings("ignore")

print(f"NumPy {np.__version__} | Pandas {pd.__version__} | Matplotlib {matplotlib.__version__}")

```


```python
# ── Dam Salient Features (from Premonsoon-2025 Inspection Report) ────────
DAM = dict(
    name        = "DEHRANG DAM",
    owner       = "Panvel Municipal Corporation",
    state       = "Maharashtra",
    district    = "Raigad",
    lat         = "19° 1' 54\" N",
    lon         = "73° 14' 32\" E",
    commissioned= 1957,
    FRL         = 89.15,   # Full Reservoir Level (m MSL)
    MWL         = 89.15,   # Maximum Water Level (m MSL)
    MDDL        = 80.77,   # Minimum Draw Down Level (m MSL)
    spillway_cr = 86.65,   # Spillway Crest Elevation (m MSL)
    river_bed   = 75.40,   # Lowest River Bed Level (m MSL)
    insp_level  = 84.10,   # Reservoir level on inspection date
    survey_boxes= 3193,    # Total boxes in sludge survey
    total_silt  = 517.706, # Total silt volume (1,000 m3)
)

print("=" * 55)
print(f"  {DAM['name']} — Key Levels")
print("=" * 55)
for k,v in DAM.items():
    if isinstance(v,(int,float)) and k not in ("commissioned","survey_boxes"):
        print(f"  {k:20s}: {v:.2f} m MSL" if isinstance(v,float) else f"  {k:20s}: {v}")
print("=" * 55)

```


```python
# ── Load Sludge Survey Data ───────────────────────────────────────────────
# Upload the file: SLUDGE_QNTY_10X10_DEHRANG_DAM.xlsx
# In Colab: use files.upload() or mount Google Drive

# Uncomment the line that matches your setup:
# from google.colab import files; uploaded = files.upload()
# OR if file is in same folder:
SLUDGE_FILE = "SLUDGE_QNTY_10X10_DEHRANG_DAM.xlsx"

df = pd.read_excel(SLUDGE_FILE, header=1)
df.columns = [
    "Box_No", "Sludge_Top_Elevations", "Avg_Sludge_Top", "Top_Box_Area",
    "Sludge_Bot_Elevations", "Avg_Sludge_Bot", "Bot_Box_Area",
    "Sludge_Depth", "Sludge_Bot_Area", "Sludge_Volume_m3"
]
df = df[pd.to_numeric(df["Box_No"], errors="coerce").notna()].copy()
for col in ["Avg_Sludge_Bot", "Avg_Sludge_Top", "Top_Box_Area", "Sludge_Volume_m3"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Avg_Sludge_Bot", "Avg_Sludge_Top", "Top_Box_Area"])

print(f"Loaded {len(df):,} survey boxes")
print(f"Sludge bottom elev : {df.Avg_Sludge_Bot.min():.3f} m  to  {df.Avg_Sludge_Bot.max():.3f} m")
print(f"Sludge top elev    : {df.Avg_Sludge_Top.min():.3f} m  to  {df.Avg_Sludge_Top.max():.3f} m")
print(f"Total silt volume  : {df.Sludge_Volume_m3.sum():,.2f} m³")
display(df.head())

```


```python
# ── Build Elevation Grid & Compute Area–Elevation Relationship ────────────
INTV   = 0.2   # Elevation interval (m)
e_min  = np.floor(df.Avg_Sludge_Bot.min() * 5) / 5
e_max  = DAM["FRL"]
elevs  = np.round(np.arange(e_min, e_max + INTV/2, INTV), 2)

survey_max_bot = df.Avg_Sludge_Bot.max()
survey_max_top = df.Avg_Sludge_Top.max()

# Area at each elevation from survey data
orig_area = np.array([df.loc[df.Avg_Sludge_Bot <= h, "Top_Box_Area"].sum() for h in elevs])
curr_area = np.array([df.loc[df.Avg_Sludge_Top <= h, "Top_Box_Area"].sum() for h in elevs])

# Extrapolate original area above survey using 2nd-order polynomial
fit_mask = (elevs >= 83.0) & (elevs <= survey_max_bot)
poly_coef = np.polyfit(elevs[fit_mask], orig_area[fit_mask], 2)
for i, h in enumerate(elevs):
    if h > survey_max_bot:
        orig_area[i] = max(orig_area[elevs <= survey_max_bot][-1],
                           np.polyval(poly_coef, h))

# Above max silt top: current = original (no silt recorded there)
for i, h in enumerate(elevs):
    if h > survey_max_top:
        curr_area[i] = orig_area[i]

# ── Trapezoidal Volume Integration ────────────────────────────────────────
orig_vol = np.zeros(len(elevs)); curr_vol = np.zeros(len(elevs))
inc_orig  = np.zeros(len(elevs)); inc_curr  = np.zeros(len(elevs))
for i in range(1, len(elevs)):
    d_ov = (orig_area[i-1] + orig_area[i]) / 2 * INTV
    d_cv = (curr_area[i-1] + curr_area[i]) / 2 * INTV
    orig_vol[i] = orig_vol[i-1] + d_ov
    curr_vol[i] = curr_vol[i-1] + d_cv
    inc_orig[i]  = d_ov; inc_curr[i]  = d_cv

# Convert to 1,000 m³
orig_tcm  = np.round(orig_vol  / 1000, 3)
curr_tcm  = np.round(curr_vol  / 1000, 3)
loss_tcm  = np.round(orig_tcm - curr_tcm, 3)
loss_pct  = np.where(orig_tcm > 0,
                     np.round(loss_tcm / orig_tcm * 100, 1), 0.0)
orig_ha   = np.round(orig_area / 10000, 3)
curr_ha   = np.round(curr_area / 10000, 3)

print(f"Elevation range : {elevs[0]:.1f} m  to  {elevs[-1]:.1f} m MSL")
print(f"Total rows      : {len(elevs)}")
print(f"Orig. cap @ FRL : {orig_tcm[-1]:,.1f}  x 1,000 m³")
print(f"Curr. cap @ FRL : {curr_tcm[-1]:,.1f}  x 1,000 m³")
print(f"Cap. lost       : {loss_tcm[-1]:,.1f}  x 1,000 m³  ({loss_pct[-1]:.1f}%)")

```


```python
# ── Assemble Storage-Elevation Table ─────────────────────────────────────
result = pd.DataFrame({
    "Elevation_m_MSL"          : elevs,
    "Original_Area_ha"         : orig_ha,
    "Original_IncrVol_1000m3"  : np.round(inc_orig / 1000, 3),
    "Original_CumCapacity_1000m3": orig_tcm,
    "Current_Area_ha"          : curr_ha,
    "Current_IncrVol_1000m3"   : np.round(inc_curr / 1000, 3),
    "Current_CumCapacity_1000m3": curr_tcm,
    "CapacityLoss_1000m3"      : loss_tcm,
    "CapacityLoss_pct"         : loss_pct,
})

# Mark key levels
key_elev = {DAM["MDDL"]:"MDDL", DAM["spillway_cr"]:"Spillway Crest",
            DAM["FRL"]:"FRL/MWL", DAM["insp_level"]:"Inspection Level"}
result["Key_Level"] = result.Elevation_m_MSL.apply(
    lambda h: next((v for k,v in key_elev.items() if abs(h-k)<0.001), ""))

print(result.to_string(index=False))

```


```python
# ── Export as CSV ─────────────────────────────────────────────────────────
CSV_FILE = "Dehrang_Dam_Storage_Elevation.csv"
result.to_csv(CSV_FILE, index=False)
print(f"CSV saved: {CSV_FILE}  ({len(result)} rows)")

# Download in Colab (uncomment if needed)
# from google.colab import files
# files.download(CSV_FILE)

```

## 📊 Engineering Plots
### Plot 1 — Area–Elevation Curve (Water Spread Area)


```python
# ── PLOT 1: Area–Elevation Curve ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 11), dpi=120)

# Graph-paper background
ax.set_facecolor("#F7F9FF")
fig.patch.set_facecolor("#FFFFFF")
ax.grid(which="major", color="#3060B0", linewidth=0.5, alpha=0.4)
ax.grid(which="minor", color="#9BB8E0", linewidth=0.2, alpha=0.3)
ax.minorticks_on()
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

# Curves
ax.plot(orig_ha, elevs, color="#1B5E20", lw=2.2, label="Original Area (Pre-Siltation)")
ax.plot(curr_ha, elevs, color="#E65100", lw=2.2, ls="--", label="Current Area (Post-Siltation)")
ax.fill_betweenx(elevs, curr_ha, orig_ha, color="#FFCCBC", alpha=0.45, label="Area Lost to Siltation")

# Key horizontal level lines
kl = [(DAM["MDDL"],    "#1565C0", "--",  "MDDL = 80.77 m"),
      (DAM["insp_level"],"#558B2F",":",  "Inspection Level = 84.10 m"),
      (DAM["spillway_cr"],"#6A1B9A","-.","Spillway Crest = 86.65 m"),
      (DAM["FRL"],      "#B71C1C", "-",  "FRL / MWL = 89.15 m")]
for elev, color, ls, label in kl:
    ax.axhline(elev, color=color, lw=1.3, ls=ls, alpha=0.85)
    ax.text(ax.get_xlim()[1]*0.98 if ax.get_xlim()[1]>0 else 55,
            elev+0.1, label, ha="right", va="bottom",
            fontsize=7.5, color=color, fontweight="bold")

# Axis labels
ax.set_xlabel("Water Spread Area  (ha)", fontsize=11, fontweight="bold", labelpad=8)
ax.set_ylabel("Elevation  (m MSL)", fontsize=11, fontweight="bold", labelpad=8)
ax.set_title(f"DEHRANG DAM\nWater Spread Area – Elevation Curve\n"
             f"Lat: 19°1'54"N  |  Long: 73°14'32"E  |  Owner: Panvel Municipal Corporation",
             fontsize=11, fontweight="bold", pad=12)

ax.legend(loc="lower right", fontsize=9, framealpha=0.9, edgecolor="#555")
ax.set_ylim(e_min - 0.5, DAM["FRL"] + 0.5)
ax.tick_params(axis="both", which="major", labelsize=9)

# Survey/extrap annotation
ax.axhline(survey_max_top, color="#888", lw=0.8, ls=":", alpha=0.6)
ax.text(5, survey_max_top+0.15, "▲ Survey Limit | Extrapolation above",
        fontsize=7, color="#777", style="italic")

# Border
for spine in ax.spines.values():
    spine.set_linewidth(1.5); spine.set_color("#333")

plt.tight_layout()
plt.savefig("Dehrang_Area_Elevation_Curve.png", dpi=150, bbox_inches="tight")
plt.show()
print("Plot 1 saved.")

```

### Plot 2 — Capacity–Elevation Curve (Original vs Current)


```python
# ── PLOT 2: Capacity–Elevation Curve ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 11), dpi=120)

ax.set_facecolor("#F7F9FF"); fig.patch.set_facecolor("#FFFFFF")
ax.grid(which="major", color="#3060B0", linewidth=0.5, alpha=0.4)
ax.grid(which="minor", color="#9BB8E0", linewidth=0.2, alpha=0.3)
ax.minorticks_on()
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

ax.plot(orig_tcm, elevs, color="#1B5E20", lw=2.4, label="Original Capacity (Pre-Siltation)")
ax.plot(curr_tcm, elevs, color="#E65100", lw=2.4, ls="--", label="Current Capacity (Post-Siltation)")
ax.fill_betweenx(elevs, curr_tcm, orig_tcm, color="#FFCCBC", alpha=0.45, label="Capacity Lost to Siltation")

for elev, color, ls, label in kl:
    ax.axhline(elev, color=color, lw=1.3, ls=ls, alpha=0.85)
    cap_at = float(orig_tcm[np.argmin(np.abs(elevs - elev))])
    ax.text(cap_at * 1.01, elev + 0.1, f"{label}\n({cap_at:,.0f}×10³m³)",
            ha="left", va="bottom", fontsize=7.2, color=color, fontweight="bold")

ax.set_xlabel("Cumulative Storage Capacity  (×1,000 m³)", fontsize=11, fontweight="bold", labelpad=8)
ax.set_ylabel("Elevation  (m MSL)", fontsize=11, fontweight="bold", labelpad=8)
ax.set_title(f"DEHRANG DAM\nReservoir Capacity – Elevation Curve\n"
             f"Lat: 19°1'54"N  |  Long: 73°14'32"E  |  Owner: Panvel Municipal Corporation",
             fontsize=11, fontweight="bold", pad=12)

ax.legend(loc="lower right", fontsize=9, framealpha=0.9, edgecolor="#555")
ax.set_ylim(e_min - 0.5, DAM["FRL"] + 0.5)
ax.tick_params(axis="both", which="major", labelsize=9)

ax.axhline(survey_max_top, color="#888", lw=0.8, ls=":", alpha=0.6)
ax.text(50, survey_max_top + 0.15, "▲ Survey Limit | Extrapolation above",
        fontsize=7, color="#777", style="italic")

for spine in ax.spines.values():
    spine.set_linewidth(1.5); spine.set_color("#333")

plt.tight_layout()
plt.savefig("Dehrang_Capacity_Elevation_Curve.png", dpi=150, bbox_inches="tight")
plt.show()
print("Plot 2 saved.")

```

### Plot 3 — Combined Engineering Sheet (Area + Capacity Side-by-Side)


```python
# ── PLOT 3: Combined Engineering Sheet ───────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 13), dpi=120,
                                 gridspec_kw={"wspace": 0.35})

for ax in (ax1, ax2):
    ax.set_facecolor("#F4F6FF"); fig.patch.set_facecolor("#FAFAFA")
    ax.grid(which="major", color="#2050A0", lw=0.55, alpha=0.35)
    ax.grid(which="minor", color="#8AAAD0", lw=0.2,  alpha=0.25)
    ax.minorticks_on()
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.set_ylim(e_min - 0.3, DAM["FRL"] + 0.5)
    ax.tick_params(axis="both", which="major", labelsize=9)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5); spine.set_color("#222")
    for elev, color, ls, _ in kl:
        ax.axhline(elev, color=color, lw=1.2, ls=ls, alpha=0.8)

# ─ Panel 1: Area ─
ax1.plot(orig_ha, elevs, "#1B5E20", lw=2.2, label="Original (Pre-Silt.)")
ax1.plot(curr_ha, elevs, "#E65100", lw=2.2, ls="--", label="Current (Post-Silt.)")
ax1.fill_betweenx(elevs, curr_ha, orig_ha, color="#FFCCBC", alpha=0.5)
ax1.set_xlabel("Water Spread Area  (ha)", fontsize=10, fontweight="bold")
ax1.set_ylabel("Elevation  (m MSL)",      fontsize=10, fontweight="bold")
ax1.set_title("Area – Elevation Curve", fontsize=11, fontweight="bold", pad=8)
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))

# Level labels on ax1
for elev, color, ls, lbl in kl:
    ax1.text(0.98, elev, lbl, transform=ax1.get_yaxis_transform(),
             ha="right", va="bottom", fontsize=7, color=color, fontweight="bold")

# ─ Panel 2: Capacity ─
ax2.plot(orig_tcm, elevs, "#1B5E20", lw=2.2, label="Original (Pre-Silt.)")
ax2.plot(curr_tcm, elevs, "#E65100", lw=2.2, ls="--", label="Current (Post-Silt.)")
ax2.fill_betweenx(elevs, curr_tcm, orig_tcm, color="#FFCCBC", alpha=0.5, label="Capacity Lost")
ax2.set_xlabel("Cumulative Capacity  (×1,000 m³)", fontsize=10, fontweight="bold")
ax2.set_ylabel("Elevation  (m MSL)",               fontsize=10, fontweight="bold")
ax2.set_title("Capacity – Elevation Curve",        fontsize=11, fontweight="bold", pad=8)
ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))

for elev, color, ls, lbl in kl:
    ax2.text(0.98, elev, lbl, transform=ax2.get_yaxis_transform(),
             ha="right", va="bottom", fontsize=7, color=color, fontweight="bold")

# Shared legend
legend_elems = [
    Line2D([0],[0], color="#1B5E20", lw=2,     label="Original (Pre-Siltation)"),
    Line2D([0],[0], color="#E65100", lw=2, ls="--", label="Current (Post-Siltation)"),
    Patch(fc="#FFCCBC", alpha=0.7,                 label="Lost Capacity / Area"),
    Line2D([0],[0], color="#1565C0", lw=1.2, ls="--", label="MDDL = 80.77 m"),
    Line2D([0],[0], color="#558B2F", lw=1.2, ls=":",  label="Inspection Level = 84.10 m"),
    Line2D([0],[0], color="#6A1B9A", lw=1.2, ls="-.", label="Spillway Crest = 86.65 m"),
    Line2D([0],[0], color="#B71C1C", lw=1.2, ls="-",  label="FRL / MWL = 89.15 m"),
]
fig.legend(handles=legend_elems, loc="lower center", ncol=4,
           fontsize=8.5, framealpha=0.95, edgecolor="#444",
           bbox_to_anchor=(0.5, -0.01))

# Super title
fig.suptitle(
    f"DEHRANG DAM  ·  RESERVOIR STORAGE-ELEVATION ANALYSIS\n"
    f"Owner: Panvel Municipal Corporation  |  Lat: 19°1'54"N, Long: 73°14'32"E  |  "
    f"FRL: 89.15 m  |  MDDL: 80.77 m  |  Data: 10×10 m Sludge Survey (3,193 boxes)",
    fontsize=10.5, fontweight="bold", y=1.01)

plt.savefig("Dehrang_Combined_Engineering_Curves.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
print("Plot 3 saved.")

```

## 📋 Summary Statistics


```python
# ── Print Summary Statistics ─────────────────────────────────────────────
def cap_at(elev):
    idx = np.argmin(np.abs(elevs - elev))
    return orig_tcm[idx], curr_tcm[idx], loss_tcm[idx], loss_pct[idx]

check_levels = [
    ("MDDL",             DAM["MDDL"]),
    ("Inspection Level", DAM["insp_level"]),
    ("Spillway Crest",   DAM["spillway_cr"]),
    ("FRL / MWL",        DAM["FRL"]),
]
print(f"{"Level":<22} {"Elev (m)":>9} {"Orig (×10³m³)":>15} {"Curr (×10³m³)":>15} {"Lost (×10³m³)":>15} {"Loss%":>7}")
print("-"*87)
for name, elev in check_levels:
    o,c,l,p = cap_at(elev)
    print(f"{name:<22} {elev:>9.2f} {o:>15,.1f} {c:>15,.1f} {l:>15,.1f} {p:>6.1f}%")
print("-"*87)
print(f"\n  Total Silt Volume (Survey) : {DAM['total_silt']:.3f} × 1,000 m³  =  {DAM['total_silt']*1000:,.0f} m³")

```
