
"""Solvers for the ECDH vs. BB84 key-provisioning index.

Scenario 1: fix eps_ch and solve the BB84/ECDH break-even fibre distance.
Scenario 2: fix the BB84 fibre distance and solve the break-even eps_ch.

Parameters live in config.py; provisioning formulas live in model.py.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
import config as cfg
import model


# --- solver operating point ---------------------------------------------------

p_bs_custom = model.basis_match(cfg.P_B_CUSTOM)
strength_custom, npk_custom = cfg.CURVES[cfg.SOLVER_CURVE]


def rate_gap(eps_ch, d_km):
    """BB84 R_KP minus ECDH R_KP; zero is the break-even condition."""

    eta = cfg.ETA_DET_CUSTOM * model.transmittance(d_km, cfg.ALPHA_CUSTOM)

    return (model.rate_bb84(eps_ch, eta, cfg.PD_CUSTOM, p_bs_custom) - model.rate_ecdh(eps_ch, strength_custom, npk_custom))


def solve_distance():
    """Solve R_KP^BB84 = R_KP^ECDH for d at fixed ECH_TARGET."""

    d_min, d_max = cfg.D_BRACKET_KM

    gap_min = rate_gap(cfg.ECH_TARGET, d_min)
    gap_max = rate_gap(cfg.ECH_TARGET, d_max)

    if gap_min * gap_max > 0:

        if gap_min < 0:
            print("Distance solver: BB84 is below ECDH at both ends of D_BRACKET_KM, so no sign change is bracketed. Inspect or adjust the bracket.")

        else:
            print("Distance solver: BB84 is above ECDH at both ends of D_BRACKET_KM, so no sign change is bracketed. Inspect or adjust the bracket.")

        return None

    d_solution = brentq(
        lambda d: rate_gap(cfg.ECH_TARGET, d),
        d_min,
        d_max
    )

    print(
        f"Break-even distance = {d_solution:.6f} km"
    )

    if gap_min > 0:
        print(
            "At the lower end of D_BRACKET_KM, BB84 has the larger R_KP. "
            f"The break-even point is d = {d_solution:.6f} km."
        )

    else:
        print(
            "At the lower end of D_BRACKET_KM, ECDH has the larger R_KP. "
            f"The break-even point is d = {d_solution:.6f} km."
        )

    return d_solution


def solve_error_rate():
    """Solve R_KP^BB84 = R_KP^ECDH for eps_ch at fixed D_TARGET_KM."""

    e_min, e_max = cfg.ECH_BRACKET

    gap_min = rate_gap(e_min, cfg.D_TARGET_KM)
    gap_max = rate_gap(e_max, cfg.D_TARGET_KM)

    if gap_min * gap_max > 0:

        if gap_min < 0:
            print(
                "Error-rate solver: BB84 is below ECDH at both ends of "
                "ECH_BRACKET, so no sign change is bracketed. "
                "Inspect or adjust the bracket."
            )

        else:
            print(
                "Error-rate solver: BB84 is above ECDH at both ends of "
                "ECH_BRACKET, so no sign change is bracketed. "
                "Inspect or adjust the bracket."
            )

        return None

    ech_solution = brentq(
        lambda e: rate_gap(e, cfg.D_TARGET_KM),
        e_min,
        e_max
    )

    print(
        f"Break-even eps_ch = {ech_solution:.8f}"
    )

    if gap_min > 0:
        print(
            "At the lower end of ECH_BRACKET, BB84 has the larger R_KP. "
            f"The break-even point is eps_ch = {ech_solution:.8f}."
        )

    else:
        print(
            "At the lower end of ECH_BRACKET, ECDH has the larger R_KP. "
            f"The break-even point is eps_ch = {ech_solution:.8f}."
        )

    return ech_solution


def plot_distance_break_even(d_solution):
    """Plot R_KP versus distance for the fixed-ECH_TARGET solver."""

    d_min, d_max = cfg.D_BRACKET_KM

    # This only changes the visible range of the graph.
    # It does NOT change the bracket used by Brent.
    if d_solution is not None:
        d_max_plot = min(
            d_max,
            max(2 * d_solution, d_solution + 1)
        )
    else:
        d_max_plot = d_max

    distances = np.linspace(
        d_min,
        d_max_plot,
        cfg.SOLVER_PLOT_POINTS
    )

    eta_values = (
        cfg.ETA_DET_CUSTOM
        * model.transmittance(
            distances,
            cfg.ALPHA_CUSTOM
        )
    )

    bb84_values = model.rate_bb84(
        cfg.ECH_TARGET,
        eta_values,
        cfg.PD_CUSTOM,
        p_bs_custom
    )

    ecdh_value = model.rate_ecdh(
        cfg.ECH_TARGET,
        strength_custom,
        npk_custom
    )

    ecdh_values = np.full_like(
        distances,
        ecdh_value,
        dtype=float
    )

    plt.figure()

    plt.plot(
        distances,
        bb84_values,
        label=(
            rf'$\mathcal{{R}}_{{\mathrm{{KP}}}}^{{BB84}}$ '
            rf'($\varepsilon_{{ch}}={cfg.ECH_TARGET:g}$)'
        )
    )

    plt.plot(
        distances,
        ecdh_values,
        label=(
            rf'$\mathcal{{R}}_{{\mathrm{{KP}}}}^{{{cfg.SOLVER_CURVE}}}$ '
            rf'($\varepsilon_{{ch}}={cfg.ECH_TARGET:g}$)'
        )
    )

    if d_solution is not None:

        plt.scatter(
            [d_solution],
            [ecdh_value],
            zorder=3
        )

        plt.axvline(
            d_solution,
            linestyle='-',
            alpha=0.7,
            label=(
                rf'$d^\star={d_solution:.2f}\,\mathrm{{km}}$'
            )
        )

    plt.xlabel(cfg.DISTANCE_XLABEL)
    plt.ylabel(cfg.FIG2_YLABEL)
    plt.grid(True, linestyle='-', alpha=0.5)
    plt.legend(fontsize=8)

    plt.savefig(
        os.path.join(
            cfg.FIGURE_DIR,
            "break_even_distance.pdf"
        ),
        bbox_inches="tight"
    )


def plot_error_break_even(ech_solution):
    """Plot R_KP versus eps_ch for the fixed-D_TARGET_KM solver."""

    e_min, e_max = cfg.ECH_BRACKET

    eps_values = np.logspace(
        np.log10(e_min),
        np.log10(e_max),
        cfg.SOLVER_PLOT_POINTS
    )

    eta_target = (
        cfg.ETA_DET_CUSTOM
        * model.transmittance(
            cfg.D_TARGET_KM,
            cfg.ALPHA_CUSTOM
        )
    )

    bb84_values = model.rate_bb84(
        eps_values,
        eta_target,
        cfg.PD_CUSTOM,
        p_bs_custom
    )

    ecdh_values = model.rate_ecdh(
        eps_values,
        strength_custom,
        npk_custom
    )

    plt.figure()

    plt.plot(
        eps_values,
        bb84_values,
        label=(
            rf'$\mathcal{{R}}_{{\mathrm{{KP}}}}^{{BB84}}$ '
            rf'($d={cfg.D_TARGET_KM:g}\,\mathrm{{km}}$)'
        )
    )

    plt.plot(
        eps_values,
        ecdh_values,
        label=(
            rf'$\mathcal{{R}}_{{\mathrm{{KP}}}}^'
            rf'{{{cfg.SOLVER_CURVE}}}$'
        )
    )

    if ech_solution is not None:

        rkp_solution = model.rate_ecdh(
            ech_solution,
            strength_custom,
            npk_custom
        )

        plt.scatter(
            [ech_solution],
            [rkp_solution],
            zorder=3
        )

        plt.axvline(
            ech_solution,
            linestyle='-',
            alpha=0.7,
            label=(
                rf'$\varepsilon_{{ch}}^\star='
                rf'{ech_solution:.4f}$'
            )
        )

    plt.xscale('log')

    plt.xlabel(cfg.XLABEL)
    plt.ylabel(cfg.FIG2_YLABEL)

    plt.grid(
        True,
        which='both',
        linestyle='-',
        alpha=0.5
    )

    plt.legend(fontsize=8)

    plt.savefig(
        os.path.join(
            cfg.FIGURE_DIR,
            "break_even_channel_error.pdf"
        ),
        bbox_inches="tight"
    )


os.makedirs(
    cfg.FIGURE_DIR,
    exist_ok=True
)

d_solution = solve_distance()
ech_solution = solve_error_rate()

plot_distance_break_even(d_solution)
plot_error_break_even(ech_solution)

plt.show()
