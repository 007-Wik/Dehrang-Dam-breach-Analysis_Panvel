# 6. HEC-RAS Breach Simulation Methodology

This section details the complete 2D hydraulic model setup in HEC-RAS
6.6, including mesh construction, terrain and roughness assignment,
breach parameterisation using Froehlich (2008) empirical equations, and
simulation execution procedures for both failure scenarios.

## 6.1 2D Hydraulic Model Overview

The HEC-RAS model for Dehrang Dam comprises two primary hydraulic
elements: a Storage Area (SA) representing the reservoir and an
unstructured 2D Flow Area (2D FA) covering the downstream floodplain
from the dam toe to the tidal influence boundary near Panvel Creek.
These are connected via an SA-to-2D Area hydraulic structure (SA2D
Conn 1) at which the breach is specified.

### 6.1.1 Model Domain and Mesh

The 2D Flow Area mesh was constructed from the hydrologically
conditioned Copernicus GLO-30 DEM. The computational mesh covers the
Gadhi River valley from the dam toe through all downstream settlements
likely to be impacted by dam breach flows. Mesh refinement was applied
in areas of higher hydraulic complexity including the channel thalweg,
road embankments acting as flow constrictions, and the immediate dam toe
area where the breach outflow undergoes rapid expansion.

- Terrain: Copernicus DEM GLO-30 (30 m horizontal resolution, WGS84 UTM
  Zone 43N)

- Mesh type: Unstructured (mixed triangular and quadrilateral elements)

- Solver: 2D Unsteady Diffusion Wave Equation Set (Fastest Mode); 8
  solver cores; 1-second computational time step; 10-minute output
  intervals

- Computational time step: 10 seconds (adaptive during breach phase)

### 6.1.2 Boundary Conditions

The following boundary conditions were applied consistently across both
simulation plans:

- Upstream (SA Inflow): HEC-HMS design flood hydrograph (600.4 m3/s
  peak) for the overtopping scenario; constant 3 m3/s baseflow for the
  piping scenario

- Downstream (2D FA outlet): Normal depth boundary using the DEM-derived
  longitudinal water surface slope at the downstream domain boundary

- Initial condition: Reservoir at FRL = 89.15 m MSL (piping plan) or at
  90.0 m MSL (overtopping plan, consistent with rising storm conditions)

- Dry land initial conditions applied to the 2D flow area (no
  pre-existing flood water in floodplain)

### 6.1.3 Land Cover and Manning's Roughness

Manning's roughness coefficient (n) values were spatially distributed
across the 2D mesh based on the ESRI Living Atlas LULC classification.
The roughness assignment follows standard HEC guidance for 2D models.
Values used are summarised in Table 14.

| ESA_Code | name                   | **n** |
|----------|------------------------|-------|
| 10       | Tree cover             | 0.15  |
| 20       | Shrubland              | 0.08  |
| 30       | Grassland              | 0.035 |
| 40       | Cropland               | 0.045 |
| 50       | Built-up               | 0.015 |
| 60       | Bare/sparse vegetation | 0.025 |
| 70       | Snow and ice           | 0.01  |
| 80       | Permanent water bodies | 0.03  |

*Table 14: Manning's Roughness Coefficients by LULC Class*

The channel thalweg of the Gadhi River was assigned a roughness value of
n = 0.035 (natural channel with gravel bed and minimal vegetation),
consistent with its steep gradient and cobble-gravel substrate typical
of Western Ghats hill streams. Densely vegetated floodplain areas use n
= 0.16 which substantially attenuates flood wave propagation in the
riparian zone.

## 6.2 Breach Parameterisation - Froehlich (2008) Method

Breach parameters for both failure scenarios were derived using the
Froehlich (2008) empirical regression equations, the standard method
recommended by CWC (2016) and CDSO (2018) for Indian dam safety
analysis. Froehlich (2008) developed equations based on 74 case studies
of dam failures, relating breach geometry and formation time to
reservoir volume and breach height:

$$ B_{avg} = 0.1803 \cdot K_0 \cdot V_w^{0.32} \cdot H_b^{0.19} \quad (\text{m}) $$

$$ t_f = 0.0179 \cdot V_w^{0.53} \cdot H_b^{-0.90} \quad (\text{hr}) $$

*where: K0 = 1.0 (overtopping) or 0.7 (piping); Vw = volume of water
(m3); Hb = breach height (m)*

For Dehrang Dam, the key input parameters are: **V<sub>w</sub>** =
2,351,580 m3 (gross storage at FRL from 2025 survey); for overtopping,
Hb = 90.0 - 81.4 = 8.6 m (water surface above final breach invert); for
piping, Hb = 89.15 - 75.40 = 13.75 m (full head from FRL to riverbed).
Computed values closely match the entered model parameters as detailed
below.

### 6.2.1 Overtopping Failure - Plan: DEH-OVTP-PL

The overtopping breach was configured in HEC-RAS Plan DEH-OVTP-DBA. The
SA-to-2D connection (SA2D Conn 1) represents the full 335 m dam
alignment; the breach is centred at Station 159 m, corresponding to the
lowest section of the earthen bund adjacent to the concrete spillway
structure. Breach parameters are tabulated in Table 15.

| **Parameter**               | **Value**                                  |
|-----------------------------|--------------------------------------------|
| **SA Connection**           | SA2D Conn 1                                |
| **Breach Centre Station**   | 159 m                                      |
| **Final Bottom Width**      | 34 m                                       |
| **Final Bottom Elevation**  | 81.4 m MSL                                 |
| **Left Side Slope (H:V)**   | 1.0                                        |
| **Right Side Slope (H:V)**  | 1.0                                        |
| **Breach Weir Coefficient** | 1.44                                       |
| **Breach Formation Time**   | 1.04 hrs                                   |
| **Failure Mode**            | Overtopping                                |
| **Trigger WSE**             | 90.0 m MSL (WS Elev trigger)               |
| **Starting Water Surface**  | 90.0 m MSL                                 |
| **Parameterization Method** | User Entered Data (Froehlich 2008 derived) |

*Table 15: Breach Parameters - Overtopping Failure Scenario (Plan:
DEH-OVTP-PL)*

The overtopping breach triggers when the reservoir WSE reaches 90.0 m
MSL (configured as a WS Elevation trigger in HEC-RAS). The breach erodes
from the dam crest downward to the final bottom elevation of 81.4 m
MSL - well above the riverbed - reflecting the typical behaviour of
earthen dam overtopping failure where the breach is limited by the
erosion-resistant core or by the extent of embankment material
available. The 1.04-hour formation time reflects the rapid erosion
expected under sustained overtopping of this compact embankment.

### 6.2.2 Piping Failure - Plan: DEH-PIPG-DBA

The piping failure breach was configured in a separate HEC-RAS plan
(DEH-PIPG-DBA) using the same SA-2D connection geometry. The piping
mechanism is modelled using the User Entered Data breach method, with
Froehlich (2008) empirical equations applied to compute breach
parameters at the pool elevation of 89.15 m MSL (FRL). Initial piping
initiates at elevation 81.5 m MSL, and the breach erodes to a final
bottom elevation of 81.4 m MSL. The reservoir is pre-set at FRL (89.15 m
MSL) with a constant baseflow of 3 m3/s and the breach trigger is set to
initiate at 01 January 2025 01:00. Parameters are derived from Froehlich
(2008) equations and are tabulated in Table 16.

| **Parameter**                | **Value**                                                              |
|------------------------------|------------------------------------------------------------------------|
| **SA Connection**            | SA2D Conn 1 (separate piping plan)                                     |
| **Breach Centre Station**    | 159 m                                                                  |
| **Failure Mode**             | Piping (Internal Erosion)                                              |
| **Initial Piping Elevation** | 81.5 m MSL (initial piping elevation, mid-embankment)                  |
| **Final Bottom Elevation**   | 81.4 m MSL (embankment base erosion limit)                             |
| **Final Bottom Width**       | 33 m (Froehlich 2008: K0=0.7, Vw=2238.652x10^3 m3, Hb=7.75 m)          |
| **Left Side Slope (H:V)**    | 1.4                                                                    |
| **Right Side Slope (H:V)**   | 1.4                                                                    |
| **Piping Coefficient**       | 0.5                                                                    |
| **Breach Formation Time**    | 0.98 hrs (Froehlich 2008, Vw=2238.652x10^3 m3, Hb=7.75 m)              |
| **Trigger**                  | WS Elevation trigger at 89.15 m MSL (FRL); constant baseflow of 3 m3/s |
| **Starting Water Surface**   | 89.15 m MSL (FRL)                                                      |
| **Parameterization Method**  | Froehlich (2008) Empirical Equations                                   |

*Table 16: Breach Parameters - Piping Failure Scenario (Plan:
DEH-PIPG-DBA, Froehlich 2008 Derived)*

The piping breach initiates at elevation 81.5 m MSL and erodes to a
final invert of 81.4 m MSL, with a final bottom width of 33 m and 1H:1V
side slopes. The breach formation time of 0.98 hours (per Froehlich
2008) is comparable to the overtopping case. Unlike the overtopping
scenario, the piping failure initiates under fair-weather conditions
from FRL (89.15 m MSL) without any storm forcing, making it more
dangerous from an emergency warning perspective.

## 6.3 Simulation Controls and Execution

Both simulation plans were executed with consistent computational
settings to enable direct comparison of results:

- Overtopping scenario: 31 May 2025 2400 to 02 June 2025 1200 (36
  hours); Piping scenario: 01 January 2025 0100 to 03 January 2025 0100
  (48 hours). Both simulation windows are sufficient to capture full
  flood wave propagation through the study domain and reservoir
  drawdown.

- Computational time step: 1 second (fixed); this fine time step ensures
  numerical stability and accurate capture of the rapidly varying breach
  hydrograph during breach formation and peak outflow phases

- Mapping output interval: 10 minutes (for all spatial raster outputs)

- Time series output interval: 10 minutes (for hydrograph and stage
  time-series extraction at all monitoring locations and SA connections)

- 2D solver: 2D Unsteady Diffusion Wave Equation Set (fastest mode)
  applied uniformly across the entire 2D mesh domain, consistent with
  the Diffusion Wave approximation of the shallow water equations. This
  solver neglects the convective acceleration terms in the momentum
  equation, providing computationally efficient and stable solutions for
  dam-break flood routing where flow is predominantly driven by pressure
  and gravity gradients.

- Warmup period: 2-hour pre-breach simulation to establish steady
  initial conditions before breach trigger

Output products generated for each simulation plan:

1.  Maximum Water Surface Elevation (WSE) raster (m MSL)

2.  Maximum Water Depth raster (m above ground)

3.  Maximum Depth-Averaged Velocity raster (m/s)

4.  Flood Wave Arrival Time raster (hours from breach initiation)

5.  Depth x Velocity (D x V) product raster for hazard classification

6.  Inundation boundary polygon (shapefile) at 0.1 m depth threshold

7.  Time-series hydrographs at key downstream cross-sections and
    settlement boundaries

## 6.4 Flood Hazard Vulnerability Classification

Flood hazard maps were produced for both breach scenarios using the
Depth x Velocity (D x V) product methodology, which integrates both
depth and dynamic force of floodwaters into a single hazard indicator.
This approach is standard in CWC (2016) EAP guidance and is consistent
with international dam safety practice (ACER, 1988; ANCOLD, 2003). The
six-tier hazard classification applied is presented in Table 17.

| **Hazard Class** | **Description**                                                          | **D x V Limit** | **Limiting Depth (m)** | **Limiting Velocity (m/s)** |
|------------------|--------------------------------------------------------------------------|-----------------|------------------------|-----------------------------|
| **H1**           | Generally safe for vehicles and people                                   | D x V \< 0.3    | 0.3 m                  | 2.0 m/s                     |
| **H2**           | Unsafe for small vehicles                                                | D x V \< 0.6    | 0.5 m                  | 2.0 m/s                     |
| **H3**           | Unsafe for vehicles, children and the elderly                            | D x V \< 0.6    | 1.2 m                  | 2.0 m/s                     |
| **H4**           | Unsafe for vehicles and people                                           | D x V \< 1.0    | 2.0 m                  | 2.0 m/s                     |
| **H5**           | Unsafe for vehicles and people; less robust buildings subject to failure | D x V \< 4.0    | 4.0 m                  | 4.0 m/s                     |
| **H6**           | All building types considered vulnerable to failure                      | D x V \> 4.0    | \-                     | \-                          |

*Table 17: Flood Hazard Vulnerability Classification - D x V Thresholds*

The hazard class H1 (D x V \< 0.3) defines zones that are generally safe
for orderly evacuation of vehicles and ambulatory adults. Class H2 (D x
V \< 0.6) is unsafe for small vehicles and should be evacuated before
flood arrival. Classes H3 and H4 are dangerous to all people and
represent the primary evacuation priority zone in an Emergency Action
Plan. Classes H5 and H6 represent catastrophic flood conditions where
structural failure of buildings is likely and survival without
evacuation is improbable.

The D x V raster was computed as a cell-by-cell product of the Maximum
Depth and Maximum Velocity rasters from each simulation. Hazard class
boundaries were applied using GIS reclassification. Areas where maximum
depth was less than 0.1 m were excluded from the hazard mapping as no
significant hazard is posed.

!!! note
    Hazard classes should be interpreted in conjunction with
    flood wave arrival times. An area classified H4 that has a 4-hour
    arrival time is more manageable for evacuation than the same hazard
    class with a 30-minute arrival time. EAP preparation must account for
    both hazard severity and available warning time.

