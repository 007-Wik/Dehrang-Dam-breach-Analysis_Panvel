# Annexure IV - Froehlich (2008) Breach Parameter Derivation

Breach parameters for both failure scenarios were derived from Froehlich
(2008) empirical equations. The methodology is summarised below for
transparency and QA purposes. The Froehlich (2008) equations are based
on regression analysis of 74 documented dam failure case studies and are
recommended by CWC (2016) EAP Guidelines and CDSO (2018) for breach
parameter estimation in Indian dam safety analysis.

## A. Input Parameters

Reservoir volume at trigger WSL:

- Overtopping (WSL = 90.0 m MSL): Vw 2,351,580 m3 (gross storage at FRL
  89.15 m MSL, conservative estimate used)

- Piping (WSL = 89.15 m MSL): Vw = 2,351,580 m3 (gross storage from 2025
  survey)

Breach height Hb:

- Overtopping: Hb = Trigger WSL - Final Breach Bottom Elev = 90.0 - 81.4
  = 8.6 m

- Piping: Hb = FRL - RBL = 89.15 - 75.40 = 13.75 m

## B. Froehlich (2008) Equations and Computed Values

**Average Breach Width: Bavg = 0.1803 \* K0 \* Vw^0.32 \* Hb^0.19**

**Formation Time: tf = 0.0179 \* Vw^0.53 \* Hb^(-0.90)**

*K0 = 1.0 (overtopping); K0 = 0.7 (piping); Vw in m3; Hb in m*

| **Parameter**                      | **Overtopping (OT)**                                   | **Piping (PI)**                                        |
|------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| **Failure mode constant K0**       | 1.0                                                    | 0.7                                                    |
| **Volume of water Vw (m3)**        | 2,538,650 (at pool elevation WSL 90.0 m MSL, from EAC) | 2,238,652 (at pool elevation WSL 89.0 m MSL, from EAC) |
| **Breach height Hb (m)**           | 8.6 (90.0 - 81.4 m final breach invert, overtopping)   | 7.75 (89.15 - 81.4 m final breach invert)              |
| **Froehlich Bavg (m)**             | 32 m (model uses 34 m)                                 | 33 m                                                   |
| **Froehlich tf (hrs)**             | 1.0 hr (model uses 1.04 hrs)                           | 0.98 hrs                                               |
| **Froehlich side slope z (H:V)**   | 1.0 (overtopping)                                      | 1.0 (piping, per Froehlich 2008 for this case)         |
| **Final bottom width (model)**     | 34 m                                                   | 23 m                                                   |
| **Final bottom elevation (model)** | 81.4 m MSL                                             | 81.4 m MSL                                             |
| **Breach weir coefficient**        | 1.44                                                   | \-                                                     |
| **Piping coefficient**             | \-                                                     | 0.5                                                    |

*Annexure IV: Froehlich (2008) Breach Parameter Derivation Summary*

!!! note
    The overtopping model breach parameters (34 m bottom width,
    1.04 hr formation time, 81.4 m invert) are consistent with Froehlich
    (2008) equations and were entered as User Entered Data in HEC-RAS Plan
    DEH-OVTP-DBA. The piping scenario parameters (33 m bottom width, 0.98 hr
    formation time, 81.4 m invert, Initial Piping Elevation 81.5 m MSL) were
    derived from Froehlich (2008) using pool volume Vw=2,238,652 m3 and
    breach height Hb=7.75 m, and entered as User Entered Data in HEC-RAS
    Plan DEH-PIPG-DBA


![](assets/annexIV_inundation_hazard_map_01.jpeg)

![](assets/annexIV_inundation_hazard_map_02.jpeg)

![](assets/annexIV_inundation_hazard_map_03.jpeg)

![](assets/annexIV_inundation_hazard_map_04.jpeg)

![](assets/annexIV_inundation_hazard_map_05.jpeg)

![](assets/annexIV_inundation_hazard_map_06.jpeg)

![](assets/annexIV_inundation_hazard_map_07.jpeg)

![](assets/annexIV_inundation_hazard_map_08.jpeg)

![](assets/annexIV_inundation_hazard_map_09.jpeg)

![](assets/annexIV_inundation_hazard_map_10.jpeg)

!!! note
    The H1 hazard class is not severe and has very low pixel
    visibility because the depth values range from 0.01 to 0.05 meters.
    Therefore, the Hazard Vulnerability Index should be used only for
    preliminary planning, as the actual hazard may vary with terrain and
    other factors.

