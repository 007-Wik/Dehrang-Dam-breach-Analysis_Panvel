# Annexure III - Alternating Block Method (ABM) Storm Distribution (Reference)

The 100-year 24-hour design storm temporal distribution was computed
using the Alternating Block Method (ABM) as a reference calculation to
verify storm structure and provide a cross-check with the SCS Type II
distribution used in HEC-HMS. The ABM (Chow, Maidment & Mays, 1988)
arranges incremental rainfall depths derived from the IDF curves in an
alternating pattern centred on Hour 12, with the largest block placed at
the storm centre.

Total storm depth = P24,100 = 486.72 mm (Gumbel EV-I, 100-year return
period). The peak block at Hour 12 = 168.74 mm = 34.67% of total depth.
The ABM distribution is provided for reference and comparison only.

| **Hour (t)** | **Incremental Rainfall (mm)** | **Intensity (mm/hr)** | **Cumulative Rainfall (mm)** | **% of Total Rainfall** | **Rank of Block** |
|--------------|-------------------------------|-----------------------|------------------------------|-------------------------|-------------------|
| 1            | 7.06                          | 7.06                  | 7.06                         | 1.45                    | 23                |
| 2            | 7.51                          | 7.51                  | 14.57                        | 1.54                    | 21                |
| 3            | 8.04                          | 8.04                  | 22.61                        | 1.65                    | 19                |
| 4            | 8.68                          | 8.68                  | 31.29                        | 1.78                    | 17                |
| 5            | 9.46                          | 9.46                  | 40.75                        | 1.94                    | 15                |
| 6            | 10.45                         | 10.45                 | 51.20                        | 2.15                    | 13                |
| 7            | 11.73                         | 11.73                 | 62.93                        | 2.41                    | 11                |
| 8            | 13.51                         | 13.51                 | 76.44                        | 2.78                    | 9                 |
| 9            | 16.17                         | 16.17                 | 92.61                        | 3.32                    | 7                 |
| 10           | 20.68                         | 20.68                 | 113.29                       | 4.25                    | 5                 |
| 11           | 30.77                         | 30.77                 | 144.06                       | 6.32                    | 3                 |
| **12**       | **168.74**                    | **168.74**            | **312.80**                   | **34.67**               | **1 \<- PEAK**    |
| 13           | 43.86                         | 43.86                 | 356.66                       | 9.01                    | 2                 |
| 14           | 24.49                         | 24.49                 | 381.15                       | 5.03                    | 4                 |
| 15           | 18.08                         | 18.08                 | 399.23                       | 3.71                    | 6                 |
| 16           | 14.69                         | 14.69                 | 413.92                       | 3.02                    | 8                 |
| 17           | 12.55                         | 12.55                 | 426.47                       | 2.58                    | 10                |
| 18           | 11.04                         | 11.04                 | 437.51                       | 2.27                    | 12                |
| 19           | 9.92                          | 9.92                  | 447.43                       | 2.04                    | 14                |
| 20           | 9.05                          | 9.05                  | 456.48                       | 1.86                    | 16                |
| 21           | 8.35                          | 8.35                  | 464.83                       | 1.71                    | 18                |
| 22           | 7.76                          | 7.76                  | 472.59                       | 1.60                    | 20                |
| 23           | 7.28                          | 7.28                  | 479.86                       | 1.49                    | 22                |
| 24           | 6.86                          | 6.86                  | 486.72                       | 1.41                    | 24                |

*Annexure III: ABM Design Storm Temporal Distribution - Reference Only
(P24,100 = 486.72 mm)*

!!! note
    Sum of all incremental blocks = 486.72 mm (CHECK PASS). This
    ABM hyetograph was NOT used as the rainfall input to HEC-HMS. HEC-HMS
    used the Hypothetical Storm with SCS Type II 24-hour distribution, which
    is the appropriate paired distribution for the SCS Unit Hydrograph
    transform method. The ABM is provided here for completeness and
    reference verification.

