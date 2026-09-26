# Chapter 4: IDF Analysis (Panvel)

This chapter performs an Intensity-Duration-Frequency (IDF) analysis to determine the design storm and peak flood for the basin.

## Objective
To establish design rainfall depths and intensity for different return periods using extreme value statistical distributions.

## Methodology Highlights
- **Distribution Fitting:** Fits the Gumbel Extreme Value Type-I distribution to 31 years of annual maximum 24-hour rainfall data using the method of moments.
- **Design Rainfall:** Computes expected rainfall for a given return period and calculates 95% confidence limits using Chow's formula.
- **Sub-daily Disaggregation:** Applies the IMD Empirical Reduction Formula to disaggregate 24-hour rainfall into shorter durations.
- **Design Storm:** Employs the Alternating Block Method to generate a design hyetograph.
- **Goodness-of-Fit:** Uses the Kolmogorov-Smirnov test and Chi-square test to validate the statistical model.
- **Design Standard:** Follows IS 11223 and CDSO guidelines, applying a 100-year return period design flood for this minor dam.

## Source Code
The complete implementation and statistical validation scripts are available in the repository:
[View the full Jupyter Notebook for this chapter on GitHub](https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel/blob/main/docs/notebooks/04_IDF_Analysis_Panvel.ipynb)
