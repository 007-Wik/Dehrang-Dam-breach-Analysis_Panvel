# Chapter 5: Cartographic Maps and Visualization

This final chapter focuses on creating high-quality, professional cartographic maps of the study area, hazard zones, and flood extents.

## Objective
To generate publication-ready maps presenting the results of the hydrological and dam break analyses.

## Methodology Highlights
- **Map Projections:** Maps are projected to UTM (EPSG auto-detected from input rasters) to preserve area and distance measurements.
- **Topographic Styling:** Applies hillshade computed from the Copernicus 30 m DEM using proper azimuth and altitude parameters.
- **Cartographic Elements:** Standardized grids (decimal degrees), north arrows, scale bars, and legends are added using libraries like `cartopy` and `matplotlib_scalebar`.
- **Output:** High-resolution 300 DPI outputs with optimized bounding boxes.

## Source Code
The complete implementation for rendering these maps is available in the repository:
[View the full Jupyter Notebook for this chapter on GitHub](https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel/blob/main/docs/notebooks/05_Maps_GoogleColab.ipynb)
