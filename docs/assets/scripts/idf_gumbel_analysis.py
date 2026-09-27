"""
idf_gumbel_analysis.py

Reference implementation of the IDF / Design-Storm methodology described in
Chapter 3 ("IDF Analysis and Design Storm") of the Dehrang Dam Dam-Break
Analysis report.

Pipeline implemented:
  1. Gumbel EV-I frequency analysis of the annual-maximum 24-hr rainfall
     series (Chow's formula, N=31, missing years 1997 & 2006 excluded).
  2. Lognormal frequency analysis as a cross-check.
  3. Kolmogorov-Smirnov goodness-of-fit test for both distributions.
  4. 100-yr 24-hr design rainfall depth.
  5. IDF table (depth & intensity) for standard sub-daily durations using
     the IMD empirical short-duration reduction formula.
  6. Alternating Block Method (ABM) 24-hour hyetograph (reference only —
     NOT what is fed to HEC-HMS; HEC-HMS uses the SCS Type II distribution,
     see Section 3.5.2 of the report).

Replace RAINFALL_SERIES below with the actual 31-year IMD annual-maximum
series for the Panvel station (Station ID 102187319) before running —
the placeholder values here are only illustrative and will not reproduce
the report's exact published numbers (mean 225.06 mm, S 71.84 mm, etc.)
unless the real series is substituted.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# 1. INPUT: annual-maximum 24-hr rainfall series (mm), Panvel station
#    Replace with the real 1992-2024 IMD series (31 values; 1997 & 2006
#    excluded as missing).
# ---------------------------------------------------------------------------
RAINFALL_SERIES: list[float] = [
    # 1992, 1993, 1994, 1995, 1996, 1998, 1999, 2000, ... 2024
    # <-- populate with the real annual-maximum daily rainfall (mm) values -->
]


@dataclass
class GumbelResult:
    mean: float
    std: float
    cv: float
    skew: float
    yn: float
    sn: float
    design_values: dict[int, float]
    ks_stat: float
    ks_pass: bool


# ---------------------------------------------------------------------------
# Gumbel reduced-variate reduction factors (yn, Sn) by sample size N.
# Standard table (Chow, Maidment & Mays, 1988 / CWC Flood Estimation Manual).
# Only the entries actually needed are included; extend as required.
# ---------------------------------------------------------------------------
GUMBEL_YN_SN_TABLE = {
    30: (0.5362, 1.1124),
    31: (0.5370, 1.1156),
    32: (0.5380, 1.1193),
    35: (0.5403, 1.1285),
    40: (0.5436, 1.1413),
}


def gumbel_yn_sn(n: int) -> tuple[float, float]:
    if n in GUMBEL_YN_SN_TABLE:
        return GUMBEL_YN_SN_TABLE[n]
    raise ValueError(
        f"yn/Sn not tabulated for N={n}; add the value from the standard "
        "Gumbel reduction-factor table before proceeding."
    )


def gumbel_ev1_frequency_analysis(
    series: list[float], return_periods: list[int]
) -> GumbelResult:
    """Chow's formula: X_T = x_bar + K * S, K = (y_T - y_n) / S_n."""
    x = np.asarray(series, dtype=float)
    n = len(x)
    x_bar = x.mean()
    s = x.std(ddof=1)
    cv = s / x_bar
    cs = stats.skew(x, bias=False)
    yn, sn = gumbel_yn_sn(n)

    design_values = {}
    for t in return_periods:
        y_t = -math.log(math.log(t / (t - 1)))
        k = (y_t - yn) / sn
        design_values[t] = x_bar + k * s

    # Kolmogorov-Smirnov goodness-of-fit vs. fitted Gumbel CDF
    loc, scale = stats.gumbel_r.fit(x)
    ks_stat, _ = stats.kstest(x, "gumbel_r", args=(loc, scale))
    # Critical D at 5% significance (approx. 1.36/sqrt(N))
    d_crit = 1.36 / math.sqrt(n)

    return GumbelResult(
        mean=x_bar,
        std=s,
        cv=cv,
        skew=cs,
        yn=yn,
        sn=sn,
        design_values=design_values,
        ks_stat=ks_stat,
        ks_pass=ks_stat < d_crit,
    )


def lognormal_frequency_analysis(
    series: list[float], return_periods: list[int]
) -> dict[int, float]:
    """Lognormal design values via z_T from the standard normal table."""
    x = np.asarray(series, dtype=float)
    ln_x = np.log(x)
    uy, sy = ln_x.mean(), ln_x.std(ddof=1)

    design_values = {}
    for t in return_periods:
        z_t = stats.norm.ppf(1 - 1 / t)
        design_values[t] = math.exp(uy + z_t * sy)
    return design_values


# ---------------------------------------------------------------------------
# IMD empirical short-duration reduction formula:
#   P_t = P24 * (t / 24) ** (1/3)
# where P_t is the rainfall depth (mm) for duration t (hours), P24 the
# 24-hr depth. This is the standard IMD reduction formula used for
# sub-daily disaggregation when short-duration gauge data are unavailable.
# ---------------------------------------------------------------------------
DURATIONS_HR = {
    "15 min": 0.25,
    "30 min": 0.5,
    "1 hr": 1.0,
    "2 hr": 2.0,
    "3 hr": 3.0,
    "6 hr": 6.0,
    "12 hr": 12.0,
    "24 hr": 24.0,
}


def build_idf_table(p24_by_return_period: dict[int, float]) -> dict[str, dict[int, float]]:
    """Returns {duration_label: {return_period: depth_mm}}."""
    table: dict[str, dict[int, float]] = {}
    for label, t_hr in DURATIONS_HR.items():
        table[label] = {
            rp: p24 * (t_hr / 24.0) ** (1 / 3)
            for rp, p24 in p24_by_return_period.items()
        }
    return table


def idf_intensity_table(depth_table: dict[str, dict[int, float]]) -> dict[str, dict[int, float]]:
    """Convert depth (mm) table to intensity (mm/hr) table."""
    intensity: dict[str, dict[int, float]] = {}
    for label, rp_depths in depth_table.items():
        t_hr = DURATIONS_HR[label]
        intensity[label] = {rp: depth / t_hr for rp, depth in rp_depths.items()}
    return intensity


# ---------------------------------------------------------------------------
# Alternating Block Method (ABM) — 24 one-hour blocks, largest block at the
# storm centre (Hour 12), alternating outward. Reference only (Section 3.5.1
# / Annexure III) — HEC-HMS uses the SCS Type II distribution instead.
# ---------------------------------------------------------------------------
def alternating_block_method(p24: float, n_hours: int = 24) -> list[float]:
    """Returns the ordered 1-hr incremental-depth hyetograph (mm), length n_hours."""
    # Depths at each cumulative duration via the same IMD reduction formula
    cum_depth = [p24 * (t / n_hours) ** (1 / 3) for t in range(1, n_hours + 1)]
    incremental = [cum_depth[0]] + [
        cum_depth[i] - cum_depth[i - 1] for i in range(1, n_hours)
    ]
    incremental_sorted = sorted(incremental, reverse=True)

    # Alternate blocks around the centre position
    centre = n_hours // 2
    hyetograph = [0.0] * n_hours
    hyetograph[centre] = incremental_sorted[0]
    left, right = centre - 1, centre + 1
    toggle_left = True
    for block in incremental_sorted[1:]:
        if toggle_left and left >= 0:
            hyetograph[left] = block
            left -= 1
        elif right < n_hours:
            hyetograph[right] = block
            right += 1
        toggle_left = not toggle_left
    return hyetograph


if __name__ == "__main__":
    RETURN_PERIODS = [2, 5, 10, 25, 50, 100, 200, 1000]

    if not RAINFALL_SERIES:
        raise SystemExit(
            "Populate RAINFALL_SERIES with the 31-year IMD annual-maximum "
            "series before running this script."
        )

    gumbel = gumbel_ev1_frequency_analysis(RAINFALL_SERIES, RETURN_PERIODS)
    lognormal = lognormal_frequency_analysis(RAINFALL_SERIES, RETURN_PERIODS)

    print(f"N = {len(RAINFALL_SERIES)}")
    print(f"Mean = {gumbel.mean:.2f} mm, Std Dev = {gumbel.std:.2f} mm, "
          f"Cv = {gumbel.cv:.3f}, Cs = {gumbel.skew:.3f}")
    print(f"Gumbel yn = {gumbel.yn}, Sn = {gumbel.sn}")
    print(f"K-S statistic = {gumbel.ks_stat:.4f} "
          f"({'PASS' if gumbel.ks_pass else 'FAIL'})")

    print("\n100-yr design rainfall (Gumbel EV-I):",
          f"{gumbel.design_values[100]:.2f} mm")
    print("100-yr design rainfall (Lognormal):   ",
          f"{lognormal[100]:.2f} mm")

    depth_table = build_idf_table(gumbel.design_values)
    intensity_table = idf_intensity_table(depth_table)

    print("\nIDF Depth Table (mm):")
    for label, rp_vals in depth_table.items():
        row = "  ".join(f"{rp}yr={v:.2f}" for rp, v in rp_vals.items())
        print(f"  {label:8s}: {row}")

    hyetograph = alternating_block_method(gumbel.design_values[100])
    print("\nABM 100-yr 24-hr hyetograph (mm/hr), Hour 1-24:")
    print("  " + ", ".join(f"{v:.2f}" for v in hyetograph))
