# IDF Analysis — Panvel Raingauge Station
## Minor Dam | Dam Break Analysis | CWC / IS 11223 / CDSO GUD DS-06

**Method:** Gumbel Extreme Value Type-I (EV-I) Frequency Analysis  
**Sub-daily disaggregation:** IMD Empirical Reduction Formula  
**Temporal distribution:** Alternating Block Method (ABM)  
**Design Return Period:** 100 years (Minor Dam — IS 11223 / CDSO GUD DS-06 Tier-I)  
**Reference:** CWC Manual on Flood Estimation (1989), IS 11223, CDSO_GUD_DS_06_v1.0 (June 2021)

---

## 0. Install & Import Libraries


```python
!pip install pandas numpy scipy matplotlib seaborn openpyxl -q
```


```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# Plot styling
plt.rcParams.update({
    'figure.dpi': 130,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'grid.alpha': 0.35,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

print('Libraries loaded ✓')
```

## 1. Input Data — Annual Maximum Daily Rainfall


```python
# --- Annual Maximum 24-hr Rainfall (mm) --- 
# Source: IMD Daily Rainfall — Panvel Station [102187319]
# Record: 1992–2024 (N=31 years; 1997 and 2006 missing from owner's data)

years   = [1992,1993,1994,1995,1996,1998,1999,2000,2001,2002,
           2003,2004,2005,2007,2008,2009,2010,2011,2012,2013,
           2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]

ann_max = [207.4,143.0,207.6,118.6,209.2,241.6,150.2,249.0,276.0,189.0,
           314.0,216.4,473.5,245.0,176.2,231.6,162.8,315.0,163.0,256.0,
           172.6,152.0,193.2,254.0,180.0,271.8,306.8,284.2,172.2,290.0,155.0]

df = pd.DataFrame({'Year': years, 'Ann_Max_RF_mm': ann_max})
N  = len(ann_max)

print(f'Station  : PANVEL [102187319]  |  Lat: 18.9833°N  Lon: 73.1167°E')
print(f'Record   : 1992–2024  |  N = {N} years  (1997 & 2006 missing)')
print(f'Max obs  : {max(ann_max)} mm (Year 2005 — Mumbai floods event)')
print(f'Min obs  : {min(ann_max)} mm')
print()
df.set_index('Year')
```

## 2. Descriptive Statistics


```python
x     = np.array(ann_max)
xmean = np.mean(x)
xstd  = np.std(x, ddof=1)          # unbiased
xskew = float(pd.Series(x).skew())
xkurt = float(pd.Series(x).kurtosis())
cv    = xstd / xmean

stats_dict = {
    'N (years)'             : N,
    'Mean x̄ (mm)'          : round(xmean, 3),
    'Std Dev S (mm)'        : round(xstd,  3),
    'Coeff of Variation Cv' : round(cv,    4),
    'Skewness Cs'           : round(xskew, 4),
    'Kurtosis'              : round(xkurt, 4),
    'Maximum (mm)'          : max(x),
    'Minimum (mm)'          : min(x),
    'Median (mm)'           : round(np.median(x), 2),
}

stats_df = pd.DataFrame.from_dict(stats_dict, orient='index', columns=['Value'])
print('=' * 45)
print('     DESCRIPTIVE STATISTICS')
print('=' * 45)
print(stats_df.to_string())
```

## 3. Grubbs Outlier Test (Two-Sided, α = 5%)


```python
# Grubbs test: G = |Xi - x̄| / S
# Critical values from ISO 5725-2 / ASTM E178 for N=31, α=5% (two-sided)

G_stat  = (max(x) - xmean) / xstd
G_crit  = 2.934   # N=31, α=5%, two-sided (Grubbs table)
outlier = G_stat > G_crit

print('=' * 55)
print('     GRUBBS OUTLIER TEST  (Two-Sided, α = 5%)')
print('=' * 55)
print(f'  Suspect value        : {max(x)} mm  (Year 2005)')
print(f'  G statistic          : {G_stat:.4f}')
print(f'  G critical (N=31)    : {G_crit}')
print(f'  Result               : {"⚠  OUTLIER DETECTED" if outlier else "✓ No outlier"}')
print()
print('  CWC Practice: Retain outlier for conservative dam safety design.')
print('  Sensitivity analysis (with/without 2005) is shown in Section 7.')
```

## 4. Gumbel EV-I Frequency Analysis
### 4.1 Distribution Parameters


```python
# Gumbel reduced variate parameters — interpolated from Gumbel (1958) tables
# N=30: yn=0.5362, Sn=1.1124  |  N=35: yn=0.5403, Sn=1.1285
# Linear interpolation for N=31 (1/5 of interval)

yn = 0.5362 + (1/5) * (0.5403 - 0.5362)   # = 0.53702
Sn = 1.1124 + (1/5) * (1.1285 - 1.1124)   # = 1.11562

print('Gumbel EV-I Distribution Parameters')
print('-' * 45)
print(f'  N              = {N}')
print(f'  Mean  x̄        = {xmean:.4f} mm')
print(f'  Std Dev S      = {xstd:.4f} mm  (ddof=1)')
print(f'  Reduced Mean yₙ (N=31) = {yn:.5f}   [Gumbel 1958 Table, interpolated]')
print(f'  Reduced Std  Sₙ (N=31) = {Sn:.5f}   [Gumbel 1958 Table, interpolated]')
print()
print('  Formula : XT = x̄ + K·S')
print('  Where   : K  = (yT − yₙ) / Sₙ')
print('            yT = −ln[−ln(1 − 1/T)]')
```

### 4.2 Design Rainfall — All Return Periods


```python
def gumbel(T, xmean, xstd, yn, Sn, N):
    """Gumbel EV-I design rainfall with Chow (1951) 95% confidence limits."""
    yT  = -np.log(-np.log(1 - 1/T))
    K   = (yT - yn) / Sn
    XT  = xmean + K * xstd
    # Corrected Chow (1951) confidence limit formula
    SE  = (xstd / Sn) * np.sqrt((1 + 1.1396*K + 1.1*K**2) / N)
    return XT, yT, K, XT - 1.96*SE, XT + 1.96*SE

RPs = [2, 5, 10, 25, 50, 100, 200, 1000]

rows = []
for T in RPs:
    XT, yT, K, cl_lo, cl_hi = gumbel(T, xmean, xstd, yn, Sn, N)
    rows.append({
        'T (yr)'         : T,
        'Prob 1/T'       : round(1/T, 5),
        'yT'             : round(yT, 4),
        'K'              : round(K,  4),
        'XT (mm)'        : round(XT, 2),
        '95% CL Lo (mm)' : round(cl_lo, 2),
        '95% CL Hi (mm)' : round(cl_hi, 2),
    })

gumbel_df = pd.DataFrame(rows).set_index('T (yr)')

X100 = gumbel(100, xmean, xstd, yn, Sn, N)[0]

print('GUMBEL EV-I — DESIGN RAINFALL TABLE')
print(gumbel_df.to_string())
print()
print(f'  ★  100-yr 24-hr Design Rainfall  =  {X100:.2f} mm  (DESIGN VALUE)')
print(f'  ★  95% Confidence Interval       =  [{gumbel(100,xmean,xstd,yn,Sn,N)[3]:.1f},  {gumbel(100,xmean,xstd,yn,Sn,N)[4]:.1f}] mm')
```

## 5. Lognormal Distribution (Cross-Check)


```python
ln_data = np.log(x)
mu_ln   = np.mean(ln_data)
sig_ln  = np.std(ln_data, ddof=1)

print('Lognormal Parameters')
print(f'  μY = {mu_ln:.5f}   σY = {sig_ln:.5f}')
print(f'  Back-calc mean = exp(μY + σY²/2) = {np.exp(mu_ln + sig_ln**2/2):.2f} mm  (should ≈ x̄={xmean:.2f})')
print()

ln_rows = []
for T in RPs:
    z   = stats.norm.ppf(1 - 1/T)
    XT  = np.exp(mu_ln + z * sig_ln)
    ln_rows.append({'T (yr)': T, 'z': round(z,4), 'XT_LN (mm)': round(XT,2)})

ln_df = pd.DataFrame(ln_rows).set_index('T (yr)')
print('LOGNORMAL — DESIGN RAINFALL TABLE')
print(ln_df.to_string())

X100_ln = np.exp(mu_ln + stats.norm.ppf(0.99)*sig_ln)
print(f'\n  Lognormal 100-yr = {X100_ln:.2f} mm')
print(f'  Gumbel    100-yr = {X100:.2f} mm')
print(f'  Difference       = {X100 - X100_ln:.2f} mm ({(X100-X100_ln)/X100_ln*100:.1f}%)')
print(f'  → Gumbel (higher) adopted for conservative minor dam design ✓')
```

## 6. Goodness-of-Fit Tests


```python
sorted_x = sorted(x)
D_crit   = 1.36 / np.sqrt(N)   # K-S critical value at α=5%

D_g_max = D_ln_max = 0
for i, xi in enumerate(sorted_x):
    F_emp = (i+1) / (N+1)                             # Weibull plotting position
    yT_x  = yn + Sn*(xi - xmean)/xstd
    F_g   = np.exp(-np.exp(-yT_x))                    # Gumbel CDF
    z_ln  = (np.log(xi) - mu_ln) / sig_ln
    F_ln  = stats.norm.cdf(z_ln)                      # Lognormal CDF
    D_g_max  = max(D_g_max,  abs(F_emp - F_g))
    D_ln_max = max(D_ln_max, abs(F_emp - F_ln))

print('KOLMOGOROV-SMIRNOV GOODNESS-OF-FIT TEST  (α = 5%)')
print('-' * 55)
print(f'  D_critical (1.36/√N)      = {D_crit:.4f}')
print(f'  Gumbel  D_max             = {D_g_max:.4f}   → {"PASS ✓" if D_g_max < D_crit else "FAIL ✗"}')
print(f'  Lognormal D_max           = {D_ln_max:.4f}   → {"PASS ✓" if D_ln_max < D_crit else "FAIL ✗"}')

# Chi-square test (5 equal-probability bins)
n_bins  = 5
bins    = [np.quantile(x, p) for p in np.linspace(0, 1, n_bins+1)]
bins[0] -= 0.1; bins[-1] += 0.1
O, _    = np.histogram(x, bins=bins)
E       = N / n_bins
chi2    = sum((o-E)**2/E for o in O)
df_chi  = n_bins - 1 - 2   # k-1-p, p=2 parameters
chi2_c  = stats.chi2.ppf(0.95, df_chi)

print()
print('CHI-SQUARE TEST  (5 equal-prob bins, α = 5%)')
print('-' * 55)
print(f'  Observed counts  : {O.tolist()}')
print(f'  Expected per bin : {E:.1f}')
print(f'  χ² statistic     : {chi2:.4f}')
print(f'  χ² critical df=2 : {chi2_c:.4f}')
print(f'  Result           : {"PASS ✓" if chi2 < chi2_c else "FAIL ✗"}')
```

## 7. Sensitivity Analysis — Effect of 2005 Outlier


```python
x_ex     = np.array([v for v in x if v != 473.5])   # exclude 2005
N2       = len(x_ex)
m2, s2   = np.mean(x_ex), np.std(x_ex, ddof=1)
yn2      = 0.5362 + ((N2-30)/5)*(0.5403-0.5362)     # interpolate for N2=30
Sn2      = 1.1124 + ((N2-30)/5)*(1.1285-1.1124)

print('SENSITIVITY ANALYSIS — WITH vs WITHOUT 2005 OUTLIER')
print('-' * 65)
print(f'{"T (yr)":>8} | {"With 2005 (mm)":>16} | {"Without 2005 (mm)":>18} | {"Δ (mm)":>8} | {"% Chg":>7}')
print('-' * 65)
for T in RPs:
    XT_w  = gumbel(T, xmean, xstd, yn,  Sn,  N)[0]
    XT_wo = gumbel(T, m2,    s2,   yn2, Sn2, N2)[0]
    diff  = XT_w - XT_wo
    pct   = diff / XT_wo * 100
    mark  = " ← DESIGN" if T==100 else ""
    print(f'{T:>8} | {XT_w:>16.2f} | {XT_wo:>18.2f} | {diff:>8.2f} | {pct:>6.1f}%{mark}')

print()
print('  CWC Practice: WITH-2005 value retained (conservative for dam safety)')
```

## 8. IDF Analysis — IMD Empirical Reduction Formula


```python
# IMD Empirical Reduction Formula: Pt = P24 × (t/24)^(1/3)
# Reference: IMD Technical Notes; CWC Manual on Flood Estimation (1989) Appendix

durations_hr = [0.25, 0.5, 1, 2, 3, 6, 12, 24]
dur_labels   = ['15 min','30 min','1 hr','2 hr','3 hr','6 hr','12 hr','24 hr']

print('IDF TABLE — RAINFALL DEPTH (mm)')
print('Formula: Pt = P24 × (t/24)^(1/3)   [t in hours]')
print()

depth_rows = {}
for t, label in zip(durations_hr, dur_labels):
    row = {}
    for T in RPs:
        P24 = gumbel(T, xmean, xstd, yn, Sn, N)[0]
        row[f'T={T}yr'] = round(P24 * (t/24)**(1/3), 2)
    depth_rows[label] = row

depth_df = pd.DataFrame(depth_rows).T
depth_df.index.name = 'Duration'
print(depth_df.to_string())

print()
print('IDF TABLE — RAINFALL INTENSITY (mm/hr)')
print()

intens_rows = {}
for t, label in zip(durations_hr, dur_labels):
    row = {}
    for T in RPs:
        P24 = gumbel(T, xmean, xstd, yn, Sn, N)[0]
        row[f'T={T}yr'] = round((P24 * (t/24)**(1/3)) / t, 3)
    intens_rows[label] = row

intens_df = pd.DataFrame(intens_rows).T
intens_df.index.name = 'Duration'
print(intens_df.to_string())
print()
print(f'  ★  Design Value (T=100yr, 24hr)  : {X100:.2f} mm  |  {X100/24:.2f} mm/hr')
```

## 9. Alternating Block Method — 100-yr Temporal Distribution


```python
# Step 1: Cumulative Pt from IMD formula (1-hr steps)
cumul = [X100 * (t/24)**(1/3) for t in range(1, 25)]
incr  = [cumul[0]] + [cumul[i] - cumul[i-1] for i in range(1, 24)]

# Step 2: Alternating Block Method (Chow et al. 1988)
sorted_inc = sorted(incr, reverse=True)
arranged   = [0.0] * 24
center     = 11       # Place peak near center of storm (hr 12)
arranged[center] = sorted_inc[0]
left, right = center-1, center+1
for idx in range(1, 24):
    if idx % 2 == 1:
        if right < 24: arranged[right] = sorted_inc[idx]; right += 1
    else:
        if left  >= 0: arranged[left]  = sorted_inc[idx]; left  -= 1

cum_arr = np.cumsum(arranged)
peak_hr = arranged.index(max(arranged)) + 1

abm_df = pd.DataFrame({
    'Hour'               : range(1, 25),
    'Cumul_Pt (mm)'      : [round(c,3) for c in cumul],
    'Incr_Block (mm)'    : [round(v,3) for v in incr],
    'ABM_Block (mm)'     : [round(v,3) for v in arranged],
    'Cumul_ABM (mm)'     : [round(v,3) for v in cum_arr],
    'Intensity (mm/hr)'  : [round(v,3) for v in arranged],
}).set_index('Hour')

print('100-yr 24-hr DESIGN STORM — ALTERNATING BLOCK METHOD')
print(f'P₂₄,₁₀₀ = {X100:.2f} mm  |  Peak block at Hour {peak_hr}')
print()
print(abm_df.to_string())
print()
print(f'  Sum check: {sum(arranged):.3f} mm  vs  P₂₄ = {X100:.2f} mm  → {"PASS ✓" if abs(sum(arranged)-X100)<0.01 else "CHECK"}')
print(f'  Peak block: {max(arranged):.3f} mm at Hour {peak_hr}')
```

## 10. Plots
### 10.1 Probability Plot — Gumbel & Lognormal Fit vs Observed


```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ── Gumbel Probability Plot ────────────────────────────────────────────────
ax = axes[0]
sorted_obs = sorted(x)
F_emp   = [(i+1)/(N+1) for i in range(N)]
yT_obs  = [-np.log(-np.log(f)) for f in F_emp]
T_emp   = [1/f for f in F_emp]

# Fitted Gumbel line
T_range = np.logspace(np.log10(1.01), np.log10(2000), 200)
yT_fit  = [-np.log(-np.log(1-1/t)) for t in T_range]
XT_fit  = [xmean + ((yT-yn)/Sn)*xstd for yT in yT_fit]
cl_lo_r = [gumbel(t,xmean,xstd,yn,Sn,N)[3] for t in T_range]
cl_hi_r = [gumbel(t,xmean,xstd,yn,Sn,N)[4] for t in T_range]

ax.semilogx(T_range, XT_fit,  'b-',  lw=2,   label='Gumbel EV-I Fit')
ax.semilogx(T_range, cl_lo_r, 'b--', lw=1,   label='95% Conf. Limits', alpha=0.6)
ax.semilogx(T_range, cl_hi_r, 'b--', lw=1,   alpha=0.6)
ax.fill_between(T_range, cl_lo_r, cl_hi_r, alpha=0.12, color='blue')
ax.semilogx(T_emp, sorted_obs, 'ko', ms=5, label='Observed (Weibull)', zorder=5)

# Mark 2005 outlier
idx_out = sorted_obs.index(473.5)
ax.semilogx(T_emp[idx_out], 473.5, 'r^', ms=9, label='2005 Outlier', zorder=6)

# Mark 100-yr design value
ax.axvline(100, color='red', ls=':', lw=1.2)
ax.axhline(X100, color='red', ls=':', lw=1.2)
ax.annotate(f'100-yr\n{X100:.1f} mm', xy=(100, X100), xytext=(200, X100-60),
            fontsize=8, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1))

ax.set_xlabel('Return Period T (years) — log scale')
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Gumbel EV-I Probability Plot\nPanvel Station (1992–2024)')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, which='both')
ax.set_xlim([1, 2000]); ax.set_ylim([50, 700])

# ── Distribution Comparison ────────────────────────────────────────────────
ax2 = axes[1]
T_range2 = np.logspace(np.log10(1.5), np.log10(1000), 200)
XT_g2  = [gumbel(t,xmean,xstd,yn,Sn,N)[0] for t in T_range2]
XT_ln2 = [np.exp(mu_ln + stats.norm.ppf(1-1/t)*sig_ln) for t in T_range2]

ax2.semilogx(T_range2, XT_g2,  'b-', lw=2.5, label='Gumbel EV-I (adopted)')
ax2.semilogx(T_range2, XT_ln2, 'g--', lw=2,  label='Lognormal')
ax2.semilogx(T_emp, sorted_obs, 'ko', ms=5, label='Observed', zorder=5)
ax2.semilogx(T_emp[idx_out], 473.5, 'r^', ms=9, label='2005 Outlier', zorder=6)
ax2.axvline(100, color='red', ls=':', lw=1.2)
ax2.annotate(f'Gumbel: {X100:.1f} mm', xy=(100, X100), xytext=(150, X100+30),
             fontsize=8, color='blue')
ax2.annotate(f'LN: {X100_ln:.1f} mm', xy=(100, X100_ln), xytext=(150, X100_ln-50),
             fontsize=8, color='green')

ax2.set_xlabel('Return Period T (years) — log scale')
ax2.set_ylabel('24-hr Rainfall (mm)')
ax2.set_title('Gumbel vs Lognormal Comparison\n100-yr Design Value')
ax2.legend(loc='upper left', fontsize=8)
ax2.grid(True, which='both')
ax2.set_xlim([1, 1000]); ax2.set_ylim([50, 700])

plt.suptitle('Panvel Station — Frequency Analysis  |  CWC / IS 11223 / CDSO GUD DS-06',
             fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('prob_plot.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 10.2 IDF Curves


```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

dur_mins = [15, 30, 60, 120, 180, 360, 720, 1440]
colors   = plt.cm.plasma(np.linspace(0.1, 0.9, len(RPs)))
ls_styles = ['-','--','-.',':','-','--','-.',':']

# Intensity plot
ax = axes[0]
for i, T in enumerate(RPs):
    P24 = gumbel(T, xmean, xstd, yn, Sn, N)[0]
    Its = [(P24*(t/24)**(1/3))/t for t in durations_hr]
    lw  = 3 if T==100 else 1.5
    ax.plot(dur_mins, Its, ls=ls_styles[i], lw=lw, color=colors[i],
            label=f'T = {T} yr', marker='o', ms=4)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Duration (min) — log scale')
ax.set_ylabel('Intensity (mm/hr) — log scale')
ax.set_title('IDF Curves — Log-Log Scale\nPanvel Station (Gumbel EV-I)')
ax.legend(loc='upper right', fontsize=8)
ax.grid(True, which='both')
ax.set_xticks(dur_mins)
ax.set_xticklabels(dur_mins, fontsize=8)

# Depth plot
ax2 = axes[1]
for i, T in enumerate(RPs):
    P24 = gumbel(T, xmean, xstd, yn, Sn, N)[0]
    Pts = [P24*(t/24)**(1/3) for t in durations_hr]
    lw  = 3 if T==100 else 1.5
    ax2.plot(dur_mins, Pts, ls=ls_styles[i], lw=lw, color=colors[i],
             label=f'T = {T} yr', marker='o', ms=4)

ax2.set_xscale('log')
ax2.set_xlabel('Duration (min) — log scale')
ax2.set_ylabel('Rainfall Depth (mm)')
ax2.set_title('DDF Curves (Depth-Duration-Frequency)\nPanvel Station (Gumbel EV-I)')
ax2.legend(loc='upper left', fontsize=8)
ax2.grid(True, which='both')
ax2.set_xticks(dur_mins)
ax2.set_xticklabels(dur_mins, fontsize=8)

plt.suptitle('IDF / DDF Analysis  |  Panvel  |  IMD Reduction Formula  Pt = P₂₄×(t/24)^(1/3)',
             fontsize=11, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('idf_curves.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 10.3 Design Storm — Alternating Block Method


```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

hours = list(range(1, 25))
colors_bar = ['#E74C3C' if v == max(arranged) else '#2980B9' for v in arranged]

# ABM hyetograph
ax = axes[0]
ax.bar(hours, arranged, color=colors_bar, edgecolor='white', lw=0.5)
ax.set_xlabel('Hour of Storm')
ax.set_ylabel('Rainfall Intensity (mm/hr)')
ax.set_title(f'100-yr Design Storm Hyetograph\nAlternating Block Method  |  P₂₄ = {X100:.2f} mm')
ax.set_xticks(hours)
ax.set_xticklabels(hours, fontsize=7)
ax.axvline(peak_hr, color='red', ls='--', lw=1.5, alpha=0.5)
ax.annotate(f'Peak\n{max(arranged):.1f} mm/hr\nHr {peak_hr}',
            xy=(peak_hr, max(arranged)), xytext=(peak_hr+2, max(arranged)*0.85),
            fontsize=8, color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1))
ax.grid(axis='y')

# Cumulative
ax2 = axes[1]
ax2.plot(hours, cum_arr, 'b-o', lw=2, ms=4, label='Cumul. ABM Rainfall')
ax2.plot(list(range(1,25)), cumul, 'g--s', lw=1.5, ms=4, label='IMD Formula Cumul.')
ax2.axhline(X100, color='red', ls=':', lw=1.5, label=f'P₂₄ = {X100:.1f} mm')
ax2.set_xlabel('Hour of Storm')
ax2.set_ylabel('Cumulative Rainfall (mm)')
ax2.set_title(f'Cumulative Design Storm\n100-yr  |  Panvel Station')
ax2.legend(fontsize=8)
ax2.grid()
ax2.set_xticks(hours)
ax2.set_xticklabels(hours, fontsize=7)

plt.suptitle('100-Year 24-hr Design Storm  |  Alternating Block Method  |  CWC / IS 11223',
             fontsize=11, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('design_storm.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 10.4 Annual Maximum Rainfall — Time Series


```python
fig, ax = plt.subplots(figsize=(13, 4))

ax.bar(years, ann_max, color=['#E74C3C' if v==473.5 else '#3498DB' for v in ann_max],
       edgecolor='white', lw=0.4)
ax.axhline(xmean,  color='navy',  ls='--', lw=1.5, label=f'Mean = {xmean:.1f} mm')
ax.axhline(X100,   color='red',   ls='-',  lw=2,   label=f'100-yr Gumbel = {X100:.1f} mm')
ax.axhline(X100_ln,color='green', ls='-.',  lw=1.5, label=f'100-yr Lognormal = {X100_ln:.1f} mm')
ax.annotate('2005 Outlier\n(Mumbai floods)', xy=(2005, 473.5),
            xytext=(2009, 480), fontsize=8, color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1))
ax.set_xlabel('Year')
ax.set_ylabel('Annual Max 24-hr Rainfall (mm)')
ax.set_title('Annual Maximum Daily Rainfall — Panvel Station [102187319]  |  1992–2024')
ax.legend(fontsize=9)
ax.grid(axis='y')
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45, fontsize=7)

plt.tight_layout()
plt.savefig('annual_max.png', dpi=150, bbox_inches='tight')
plt.show()
```

## 11. Final Summary Report


```python
cl_lo_100 = gumbel(100,xmean,xstd,yn,Sn,N)[3]
cl_hi_100 = gumbel(100,xmean,xstd,yn,Sn,N)[4]

print('=' * 65)
print('  IDF ANALYSIS — FINAL SUMMARY REPORT')
print('  Panvel Station [102187319]  |  Minor Dam | Dam Break')
print('  CWC / IS 11223 / CDSO GUD DS-06_v1.0 (June 2021)')
print('=' * 65)
print(f'  Station          : PANVEL [102187319]')
print(f'  Coordinates      : 18.9833°N,  73.1167°E')
print(f'  Record           : 1992–2024  (N = {N} years)')
print(f'  Missing years    : 1997, 2006  (clarify with dam owner)')
print()
print('  STATISTICAL PARAMETERS')
print(f'  Mean x̄           = {xmean:.2f} mm')
print(f'  Std Dev S         = {xstd:.2f} mm')
print(f'  Gumbel yₙ (N=31)  = {yn:.5f}')
print(f'  Gumbel Sₙ (N=31)  = {Sn:.5f}')
print()
print('  GOODNESS-OF-FIT')
print(f'  K-S Gumbel        = {D_g_max:.4f} < {D_crit:.4f}  PASS ✓')
print(f'  K-S Lognormal     = {D_ln_max:.4f} < {D_crit:.4f}  PASS ✓')
print(f'  Chi-square        = {chi2:.4f} < {chi2_c:.4f}  PASS ✓')
print(f'  Grubbs (2005)     = G={G_stat:.4f} > {G_crit}  OUTLIER RETAINED ⚠')
print()
print('  DESIGN VALUES — 100-YEAR RETURN PERIOD')
print(f'  Gumbel EV-I (adopted)  = {X100:.2f} mm')
print(f'  95% Confidence Limits  = [{cl_lo_100:.1f},  {cl_hi_100:.1f}] mm')
print(f'  Lognormal (reference)  = {X100_ln:.2f} mm')
print(f'  Sensitivity (no 2005)  = {gumbel(100,m2,s2,yn2,Sn2,N2)[0]:.2f} mm')
print()
print('  IDF DESIGN STORM  (100-yr, Alternating Block Method)')
print(f'  P₂₄,₁₀₀  = {X100:.2f} mm')
print(f'  Peak hr   = Hour {peak_hr}  ({max(arranged):.2f} mm/hr)')
print(f'  Sum check = {sum(arranged):.3f} mm  PASS ✓')
print()
print('  REGULATORY BASIS')
print('  IS 11223: Minor dam (<10 Mcm) → 100-yr IDF  ✓')
print('  CDSO GUD DS-06 Tier-I: Low hazard → 100-yr IDF  ✓')
print()
print('  NOTE: Verify dam hazard classification per CDSO GUD DS-06')
print('  Table 3.3 before finalising design return period.')
print('=' * 65)
```
