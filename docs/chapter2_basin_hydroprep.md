# Chapter 2: Basin Hydrological Preparation

This chapter prepares the necessary spatial and hydrological datasets for the dam break analysis. 

## Objective
To assign Hydrological Soil Groups (HSG), compute SCS Curve Numbers (CN), and prepare Manning's roughness grids for the Gadhi River basin.

## Methodology Highlights
- **Soil Texture Data:** Extracts clay, sand, and silt fractions from ISRIC SoilGrids v2 and creates depth-weighted composites.
- **HSG Assignment:** Classifies pixels into USDA Hydrological Soil Groups (A, B, C, or D) using the textural triangle.
- **Curve Number Grid:** Assigns SCS Curve Numbers based on LULC class (ESA WorldCover 2021) and HSG.
- **Manning's Roughness:** Assigns roughness values for open water, impervious surfaces, forest, and cropland based on established hydraulic tables (Chow 1959, CWPRS).

## Source Code
The complete implementation and spatial processing scripts are available in the repository:
[View the full Jupyter Notebook for this chapter on GitHub](https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel/blob/main/docs/notebooks/02_DBA_Basin_HydroPrep.ipynb)
