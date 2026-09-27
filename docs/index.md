# Dam Break Analysis of Dehrang Dam, Panvel

**Report on Dam Break Analysis of Dehrang Dam, Panvel, Dist. Raigad, Maharashtra**

* **Developer & Engineer:** Satwik Kamlakar Udupi, Agriculture Er.
* **Institution:** Centre for Climate Change and Sustainability Studies (CCCSS), Shivaji University, Kolhapur
* **Client / Authority:** Panvel Municipal Corporation, Government of Maharashtra
* **Date:** May 2025

---

## Executive Summary & Navigation

This documentation portal presents the complete, unabridged hydraulic and hydrologic assessment of the Dehrang Dam break scenarios (Overtopping and Piping) simulated using HEC-HMS and HEC-RAS 2D (6.6).

Navigate through the core chapters, technical annexures, derived datasets, and analysis notebooks:

| Section | Description | Direct Link |
|---|---|---|
| **Chapter 1** | General background, objectives, scope of work, and project limitations | [1. Introduction](01_Introduction.md) |
| **Chapter 2** | Dehrang dam salient features (Table 1), spillway, and reservoir system | [2. Description of the Dam / Reservoir System](02_Description_of_the_Dam_Reservoir_System.md) |
| **Chapter 3** | IMD 31-yr rainfall frequency analysis (Gumbel/Lognormal), IDF curves, ABM, and SCS Type II distribution | [3. IDF Analysis and Design Storm](03_IDF_Analysis_and_Design_Storm.md) |
| **Chapter 4** | Watershed delineation, CN parameters, Muskingum reach routing, and HEC-HMS inflow hydrographs | [4. Hydrology and HEC-HMS Methodology](04_Hydrology_and_HEC-HMS_Methodology.md) |
| **Chapter 5** | 2D hydraulic model selection, terrain DEM, ESA WorldCover, Manning's $n$, and failure scenarios | [5. Dam-Break Analysis](05_Dam-Break_Analysis.md) |
| **Chapter 6** | 2D mesh configuration, Froehlich (2008) breach equations, and hazard classification thresholds | [6. HEC-RAS Breach Simulation Methodology](06_HEC-RAS_Breach_Simulation_Methodology.md) |
| **Chapter 7** | Inundation analysis, flood wave propagation, volume accounting, and full-resolution hazard maps | [7. Results and Discussion](07_Results_and_Discussion.md) |
| **Annexure I** | Reservoir Elevation-Area-Capacity (EAC) curve and survey capacity table | [Annexure I - Reservoir EAC Table](Annexure_I_Reservoir_Elevation_Area_Capacity_Table.md) |
| **Annexure II** | 31-year IMD rainfall records, Weibull plotting positions, and Gumbel EV-I calculation tables | [Annexure II - IDF Computation Tables](Annexure_II_IDF_Computation_Tables.md) |
| **Annexure III** | Complete 24-hour Alternating Block Method (ABM) design storm temporal distribution | [Annexure III - ABM Storm Distribution](Annexure_III_Alternating_Block_Method_Storm_Distribution.md) |
| **Annexure IV** | Froehlich (2008) parameter derivations and the complete 10-map inundation & hazard portfolio | [Annexure IV - Froehlich Breach Parameter Derivation](Annexure_IV_Froehlich_2008_Breach_Parameter_Derivation.md) |
| **Output Datasets** | View & download derived Storage-Elevation tables (.xlsx, .csv) and 9-sheet IDF workbook (.xlsx) | [Output Tables & Datasets](Output_Tables_and_Datasets.md) |
| **Scripts & Notebooks**| View, download, and execute sanitized Jupyter notebooks (.ipynb) and standalone Python scripts | [Original Analysis Notebooks](Original_Analysis_Notebooks.md) |

---

## Report Table of Contents

| Number | Description | Original Report Page No. |
|---|---|---|
| **1** | [**Introduction**](01_Introduction.md) | 4 |
| 1.1 | [General](01_Introduction.md#11-general) | 4 |
| 1.2 | [Objective](01_Introduction.md#12-objective) | 5 |
| 1.3 | [Scope](01_Introduction.md#13-scope) | 6 |
| 1.4 | [Limitations](01_Introduction.md#14-limitations) | 6 |
| **2** | [**Description of the Dam / Reservoir System**](02_Description_of_the_Dam_Reservoir_System.md) | 7 |
| **3** | [**IDF Analysis and Design Storm**](03_IDF_Analysis_and_Design_Storm.md) | 9 |
| 3.1 | [Rainfall Data and Station Details](03_IDF_Analysis_and_Design_Storm.md#31-rainfall-data-and-station-details) | 9 |
| 3.2 | [Frequency Analysis - Gumbel EV-I and Lognormal](03_IDF_Analysis_and_Design_Storm.md#32-frequency-analysis-gumbel-ev-i-and-lognormal) | 9 |
| 3.3 | [100-Year Design Rainfall](03_IDF_Analysis_and_Design_Storm.md#33-100-year-design-rainfall) | 10 |
| 3.4 | [IDF Curves](03_IDF_Analysis_and_Design_Storm.md#34-idf-curves) | 10 |
| 3.5 | [Design Storm Temporal Distribution](03_IDF_Analysis_and_Design_Storm.md#35-design-storm-temporal-distribution) | 11 |
| 3.5.1 | [ABM - Reference Computation](03_IDF_Analysis_and_Design_Storm.md#351-alternating-block-method-abm-reference-computation) | 11 |
| 3.5.2 | [SCS Type II Distribution - Used in HEC-HMS](03_IDF_Analysis_and_Design_Storm.md#352-scs-type-ii-distribution-design-storm-used-in-hec-hms) | 13 |
| **4** | [**Hydrology and HEC-HMS Methodology**](04_Hydrology_and_HEC-HMS_Methodology.md) | 14 |
| 4.1 | [Overview of Hydrologic Assessment](04_Hydrology_and_HEC-HMS_Methodology.md#41-overview-of-hydrologic-assessment) | 14 |
| 4.2 | [HEC-HMS Model Configuration](04_Hydrology_and_HEC-HMS_Methodology.md#42-hec-hms-model-configuration) | 14 |
| 4.3 | [Watershed Physical Characteristics](04_Hydrology_and_HEC-HMS_Methodology.md#43-watershed-physical-characteristics) | 15 |
| 4.3.1 | [Subbasin Physical Parameters](04_Hydrology_and_HEC-HMS_Methodology.md#431-subbasin-physical-parameters) | 15 |
| 4.3.2 | [SCS Curve Number and Initial Abstraction](04_Hydrology_and_HEC-HMS_Methodology.md#432-scs-curve-number-and-initial-abstraction) | 15 |
| 4.3.3 | [Reach Routing - Muskingum Parameters](04_Hydrology_and_HEC-HMS_Methodology.md#433-reach-routing-muskingum-parameters) | 16 |
| 4.4 | [Rainfall Input and Design Storm](04_Hydrology_and_HEC-HMS_Methodology.md#44-rainfall-input-and-design-storm) | 16 |
| 4.5 | [Time of Concentration and SCS Lag Time](04_Hydrology_and_HEC-HMS_Methodology.md#45-time-of-concentration-and-scs-lag-time) | 16 |
| 4.6 | [Inflow Hydrograph Results](04_Hydrology_and_HEC-HMS_Methodology.md#46-inflow-hydrograph-results) | 17 |
| 4.7 | [Interpretation for Dam Break Analysis](04_Hydrology_and_HEC-HMS_Methodology.md#47-interpretation-for-dam-break-analysis) | 19 |
| **5** | [**Dam-Break Analysis**](05_Dam-Break_Analysis.md) | 20 |
| 5.1 | [Model Selection - HEC-RAS 6.6 (2D)](05_Dam-Break_Analysis.md#51-model-selection-hec-ras-66-2d) | 20 |
| 5.2 | [Dam-Breach Scenarios](05_Dam-Break_Analysis.md#52-dam-breach-scenarios) | 20 |
| 5.2.1 | [Scenario A - Overtopping Failure](05_Dam-Break_Analysis.md#521-scenario-a-overtopping-failure-flood-induced) | 21 |
| 5.2.2 | [Scenario B - Piping Failure](05_Dam-Break_Analysis.md#522-scenario-b-piping-failure-fair-weather-structural) | 21 |
| 5.3 | [Data Inputs for the Hydraulic Model](05_Dam-Break_Analysis.md#53-data-inputs-for-the-hydraulic-model) | 21 |
| **6** | [**HEC-RAS Breach Simulation Methodology**](06_HEC-RAS_Breach_Simulation_Methodology.md) | 25 |
| 6.1 | [2D Hydraulic Model Overview](06_HEC-RAS_Breach_Simulation_Methodology.md#61-2d-hydraulic-model-overview) | 25 |
| 6.2 | [Breach Parameterisation - Froehlich (2008)](06_HEC-RAS_Breach_Simulation_Methodology.md#62-breach-parameterisation-froehlich-2008-method) | 26 |
| 6.2.1 | [Overtopping Failure](06_HEC-RAS_Breach_Simulation_Methodology.md#621-overtopping-failure-plan-deh-ovtp-pl) | 26 |
| 6.2.2 | [Piping Failure](06_HEC-RAS_Breach_Simulation_Methodology.md#622-piping-failure-plan-deh-pipg-dba) | 27 |
| 6.3 | [Simulation Controls and Execution](06_HEC-RAS_Breach_Simulation_Methodology.md#63-simulation-controls-and-execution) | 28 |
| 6.4 | [Flood Hazard Vulnerability Classification](06_HEC-RAS_Breach_Simulation_Methodology.md#64-flood-hazard-vulnerability-classification) | 29 |
| **7** | [**Results and Discussion**](07_Results_and_Discussion.md) | 30 |
| 7.1 | [Inundation Due to Overtopping Failure](07_Results_and_Discussion.md#71-inundation-due-to-overtopping-failure-scenario-a) | 30 |
| 7.1.1 | [Breach Outflow and Reservoir Drawdown - OT](07_Results_and_Discussion.md#711-breach-outflow-and-reservoir-drawdown) | 30 |
| 7.1.2 | [Flood Wave Behaviour - Overtopping](07_Results_and_Discussion.md#712-flood-wave-behaviour-overtopping) | 30 |
| 7.2 | [Inundation Due to Piping Failure](07_Results_and_Discussion.md#72-inundation-due-to-piping-failure-scenario-b) | 31 |
| 7.2.1 | [Breach Outflow and Reservoir Drawdown - PI](07_Results_and_Discussion.md#721-breach-outflow-and-reservoir-drawdown-piping) | 31 |
| 7.2.2 | [Flood Wave Behaviour - Piping](07_Results_and_Discussion.md#722-flood-wave-behaviour-piping) | 32 |
| 7.3 | [Computation Log and Volume Accounting](07_Results_and_Discussion.md#73-computation-log-and-volume-accounting) | 33 |
| 7.3.1 | [Overtopping Scenario - Computation Summary](07_Results_and_Discussion.md#731-overtopping-scenario-computation-summary) | 33 |
| 7.3.2 | [Volume Accounting Log - Overtopping](07_Results_and_Discussion.md#732-volume-accounting-log-overtopping-deh-ovtp-dbabco01) | 34 |
| 7.3.3 | [Piping Scenario - Computation Summary](07_Results_and_Discussion.md#733-piping-scenario-computation-summary) | 35 |
| 7.4.4 | [Volume Accounting Log - Piping](07_Results_and_Discussion.md#744-volume-accounting-log-piping-deh-pipg-dbabco01) | 35 |
| 7.4 | [Discussion of Flood Inundation Mapping](07_Results_and_Discussion.md#74-discussion-of-flood-inundation-mapping-dehrang-dam-break-analysis) | 36 |
| 7.5 | [Comparative Summary and EAP Implications](07_Results_and_Discussion.md#75-comparative-summary-and-eap-implications) | 45 |
| 7.5.1 | [Scenario Comparison](07_Results_and_Discussion.md#751-scenario-comparison) | 45 |
| 7.5.2 | [Hazard / Vulnerability Maps](07_Results_and_Discussion.md#752-hazard-vulnerability-maps) | 46 |
| — | [**Annexure I - Reservoir Elevation-Area-Capacity Table**](Annexure_I_Reservoir_Elevation_Area_Capacity_Table.md) | 47-48 |
| — | [**Annexure II - IDF Computation Tables**](Annexure_II_IDF_Computation_Tables.md) | 49-51 |
| — | [**Annexure III - Alternating Block Method Storm Distribution**](Annexure_III_Alternating_Block_Method_Storm_Distribution.md) | 52-53 |
| — | [**Annexure IV - Froehlich (2008) Breach Parameter Derivation**](Annexure_IV_Froehlich_2008_Breach_Parameter_Derivation.md) | 54 |
| — | [**Derived Output Tables & Engineering Datasets**](Output_Tables_and_Datasets.md) | Derived Workbooks |
| — | [**Original Analysis Notebooks & Scripts**](Original_Analysis_Notebooks.md) | Computation Scripts |
