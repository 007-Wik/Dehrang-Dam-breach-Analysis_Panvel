# Chapter 3: Dam Break Analysis and Watershed Delineation

This chapter models the actual dam breach scenario and calculates the downstream flood routing.

## Objective
To delineate the catchment area and simulate the hydrological consequences of a dam failure.

## Methodology Highlights
- **DEM Pre-processing:** Pit filling, depression filling, and flat resolution.
- **D8 Flow Routing:** Flow direction computation using the D8 steepest descent algorithm.
- **Pour Point Snapping:** Aligning the dam location with the high-accumulation cells in the flow grid.
- **Catchment Delineation:** Converting the delineated upstream catchment to a vector polygon and computing the area.
- **Breach Modeling:** (Specific models depend on implementation, e.g., HEC-RAS or empirical routing equations).

## Source Code
The complete implementation and outputs are available in the repository:
[View the full Jupyter Notebook for this chapter on GitHub](https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel/blob/main/docs/notebooks/03_DamBreak_Analysis.ipynb)
