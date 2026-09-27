# 1. Introduction

## 1.1 General

Dehrang Dam is an earthen dam with a gated spillway, constructed in 1957
across the Gadhi River in the Raigad District of Maharashtra. Owned and
operated by the Panvel Municipal Corporation (PMC), the dam serves as
the primary source of raw water supply for the Panvel urban
agglomeration and surrounding areas at a design rate of 150 LPCD.
Situated approximately 18 km from Panvel, the dam is strategically
located at Latitude 19 deg 01' 54" N and Longitude 73 deg 14' 32" E. The
structure commands a catchment area of 27 km2 over a hydrologically
active portion of the Western Ghats foothills, characterised by steep
slopes, dense forest cover, and extremely high annual rainfall ranging
from 1,720 mm (minimum) to 4,417 mm (maximum), with an average of
approximately 2,000 mm.

The dam has a total length of 335 m and is equipped with 11 Godbole-type
Automatic Tilting Gates (each 8.70 m x 2.50 m), providing a total gated
spillway length of 111 m. The Full Reservoir Level (FRL) and Maximum
Water Level (MWL) are both set at 89.15 m MSL, with the Top Bund Level
(TBL) at 91.65 m MSL providing a freeboard of 2.50 m above the FRL. The
spillway gate sill level is 86.65 m MSL. Due to decades of siltation,
the gross storage capacity at FRL has reduced from an original 11.01
MCum to approximately 2.70 MCum at present, as confirmed by a
pre-monsoon sludge survey conducted by Yash Engineering Consultant Pvt.
Ltd. in April 2025.

Downstream of the dam, the Gadhi River flows through a mixed landscape
of agricultural land, rural settlements, and expanding peri-urban areas
en route to the Panvel Creek and Ulwe River systems. The Panvel
Municipal Corporation has therefore commissioned this Dam Break Analysis
(DBA) in compliance with the Guidelines for Developing Emergency Action
Plans for Dams (CWC, 2016) and the Dam Safety Act, 2021 and associated
CDSO Guidelines (2018).

The technical assessment employs an integrated hydrologic-hydraulic
modelling framework. Intensity-Duration-Frequency (IDF) curves are
developed from 31 years of IMD daily rainfall data (1992-2024) using
Gumbel EV-I frequency analysis. HEC-HMS 4.13 transforms the design storm
into a reservoir inflow hydrograph, which serves as the upstream
boundary condition for dam breach simulations in HEC-RAS 6.6 (2D
unsteady flow). Two failure mechanisms - Overtopping and Internal
Erosion (Piping) - are evaluated using Froehlich's (2008) empirical
breach parameters.

## 1.2 Objective

The primary objective of this Dam Break Analysis is to establish a
scientifically robust, model-driven safety assessment framework for the
Dehrang reservoir under extreme hydrologic and structural loading
conditions. Specific objectives are:

1.  To develop IDF curves for the Panvel region using 31 years of IMD
    daily rainfall data and Gumbel EV-I frequency analysis, and to
    derive the 100-year 24-hour design storm using the Alternating Block
    Method (ABM).

2.  To quantify the hydrologic inflow into the Dehrang reservoir using
    HEC-HMS 4.13, incorporating SCS Curve Number loss methodology and
    SCS Unit Hydrograph transformation.

3.  To simulate dam breach behaviour under Overtopping and Internal
    Erosion (Piping) failure modes using a calibrated 2D unsteady flow
    model in HEC-RAS 6.6.

4.  To generate breach hydrographs and downstream inundation mapping,
    including water surface elevations, maximum depths, flow velocities,
    wave arrival times, and hazard classifications.

5.  To identify vulnerable downstream settlements, key infrastructure,
    and safe shelter locations to support preparation of an Emergency
    Action Plan (EAP).

## 1.3 Scope

The present study encompasses a complete hydrologic-hydraulic assessment
of breach scenarios for Dehrang Dam. The scope includes:

1.  Compilation and analysis of dam features including TBL, MWL, FRL,
    MDDL, spillway geometry, gate configuration, and storage
    characteristics from the 2025 pre-monsoon inspection report.

2.  Statistical frequency analysis of 31-year annual maximum daily
    rainfall series using Gumbel EV-I and Lognormal distributions, with
    K-S and Chi-square goodness-of-fit tests.

3.  Development of IDF curves and the 24-hour 100-year design storm
    using the IMD empirical reduction formula and the Alternating Block
    Method (ABM).

4.  Hydrologic modelling in HEC-HMS 4.13 using the SCS-CN loss method
    and SCS Unit Hydrograph transform.

5.  Two-dimensional hydraulic modelling in HEC-RAS 6.6, including 2D
    mesh construction, Copernicus 30m DEM integration, LULC-based
    Manning's roughness, and simulation of both overtopping and piping
    failure scenarios.

6.  Breach parameter development using Froehlich (2008) empirical
    method, consistent with CDSO and CWC guidance.

7.  Computation of flood depths, velocities, arrival times, hazard
    zones, and inundation extents for downstream areas.

8.  Preparation of inundation maps and hazard/vulnerability maps
    identifying shelter points and evacuation routes.

## 1.4 Limitations

Despite rigorous modelling, certain inherent limitations apply to this
study:

1.  DEM Resolution Constraints: Terrain representation is based on the
    Copernicus DEM at 30 m horizontal resolution. Narrow drains,
    culverts, embankments, and micro-topographic relief may not be fully
    resolved.

2.  Assumption of Homogeneous Roughness: Manning's n values are assigned
    based on LULC classes derived from satellite imagery. Intra-class
    variability and seasonal changes may influence local conveyance.

3.  Rainfall Data Limitations: Two years of data (1997 and 2006) are
    missing from the 31-year record. The 2005 outlier event (473.5 mm)
    has been retained conservatively per CWC guidance.

4.  Simplified Representation of Hydraulic Structures: Smaller field
    structures including local bunds, culverts, and road crossings may
    be approximated or excluded.

5.  Uncertainty in Breach Parameters: Breach width, side slopes, and
    formation time are based on Froehlich (2008) empirical equations.
    Actual breach development may differ from modelled behaviour.

6.  Dynamic Land-Use Changes: Ongoing urbanisation in the Panvel-Navi
    Mumbai corridor may alter future flood propagation characteristics.

7.  Model Dependency: Results rely on HEC-HMS and HEC-RAS computation
    engines; inherent numerical tolerances and solver assumptions apply.
