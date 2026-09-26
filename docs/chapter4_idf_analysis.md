# Chapter 4: IDF Analysis (Panvel)

This chapter performs an Intensity-Duration-Frequency (IDF) analysis to determine the design storm and peak flood for the basin.

## 7. IDF Analysis — Gumbel EV-I Method (Notebook 04)

### 7.1 Distribution Fitting
The Gumbel Extreme Value Type-I distribution is fitted to N=31 years of annual maximum 24-hour rainfall using method-of-moments with reduced variate parameters from Gumbel (1958) tables, interpolated for N=31:

```
yₙ = 0.5362 + (1/5) × (0.5403 − 0.5362) = 0.53702
Sₙ = 1.1124 + (1/5) × (1.1285 − 1.1124) = 1.11562
```

### 7.2 Design Rainfall
For return period T:
```
yT  = −ln[−ln(1 − 1/T)]
K   = (yT − yₙ) / Sₙ
XT  = x̄ + K × S
```

95% confidence limits use the Chow (1951) formula:
```
SE = (S / Sₙ) × √[(1 + 1.1396K + 1.1K²) / N]
CL = XT ± 1.96 × SE
```

### 7.3 Sub-daily Disaggregation
The IMD Empirical Reduction Formula (CWC 1989, Appendix) is applied:
```
Pt = P24 × (t / 24)^(1/3)      [t in hours]
```

### 7.4 Design Storm — Alternating Block Method
The ABM distributes sub-period rainfall depths into a hyetograph such that the peak block is centred and subsequent blocks alternate left/right in descending order.

### 7.5 Goodness-of-Fit
- **Kolmogorov-Smirnov test** (α = 5%): D_critical = 1.36/√N
- **Chi-square test** (α = 5%, 5 equal-probability bins): df = k − 1 − p = 2

### 7.6 Design Standard
Per IS 11223 and CDSO GUD DS-06 v1.0 (June 2021), Tier-I minor dams use a **100-year return period** design flood.

## Source Code
The complete implementation and statistical validation scripts are available in the repository:
[View the full Jupyter Notebook for this chapter on GitHub](https://github.com/007-Wik/Dehrang-Dam-breach-Analysis_Panvel/blob/main/docs/notebooks/04_IDF_Analysis_Panvel.ipynb)
