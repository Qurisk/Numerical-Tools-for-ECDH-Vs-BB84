"""Figure 2: effective key-provisioning index vs. the channel error rate.

Compares the BB84 index over several fibre lengths against the ECDH rate for the
NIST prime curves, then solves for the break-even point of a custom operating
point (see the custom-point section of config.py).

Parameters live in config.py, formulas in model.py.
"""

import os

import matplotlib.pyplot as plt
from scipy.optimize import brentq

import config as cfg
import model

eps = cfg.FIG2_EPS
p_bs = model.basis_match(cfg.P_B)

for name in cfg.FIG2_CURVES:
    strength, npk = cfg.CURVES[name]
    plt.plot(eps, model.rate_ecdh(eps, strength, npk),
             label=rf'$\mathcal{{R}}_{{\mathrm{{KP}}}}^{{{name}}}$')

for d_km in cfg.FIG2_DISTANCES_KM:
    eta = model.transmittance(d_km, cfg.ALPHA) * cfg.ETA_DET
    plt.plot(eps, model.rate_bb84(eps, eta, cfg.PD, p_bs),
             label=r'$\mathcal{R}_{\mathrm{KP}}^{BB84}$' + f'({d_km} km)')


# --- custom operating point: break-even between the two rates ----------------

p_bs_custom = model.basis_match(cfg.P_B_CUSTOM)
strength_custom, npk_custom = cfg.CURVES[cfg.SOLVER_CURVE]


def rate_gap(eps_ch, d_km):
    """BB84 rate minus ECDH rate; zero at break-even."""
    eta = cfg.ETA_DET_CUSTOM * model.transmittance(d_km, cfg.ALPHA_CUSTOM)
    return (model.rate_bb84(eps_ch, eta, cfg.PD_CUSTOM, p_bs_custom)
            - model.rate_ecdh(eps_ch, strength_custom, npk_custom))


try:
    d_solution = brentq(lambda d: rate_gap(cfg.ECH_TARGET, d), *cfg.D_BRACKET_KM)
    print("Maximum distance = ", d_solution, "km")
except ValueError:
    print("No intersection found")

try:
    ech_solution = brentq(lambda e: rate_gap(e, cfg.D_TARGET_KM), *cfg.ECH_BRACKET)
    print("Maximum ech = ", ech_solution)
except ValueError:
    print("No intersection found")


plt.xscale('log')
plt.xlabel(cfg.XLABEL)
plt.ylabel(cfg.FIG2_YLABEL)
plt.grid(True, which="both", linestyle="-", alpha=0.5)
plt.legend(loc='upper left', fontsize=8)

os.makedirs(cfg.FIGURE_DIR, exist_ok=True)
plt.savefig(os.path.join(cfg.FIGURE_DIR, "provisioning_rate.pdf"), bbox_inches="tight")
plt.show()
