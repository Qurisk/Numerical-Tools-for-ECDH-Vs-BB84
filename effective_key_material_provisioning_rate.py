"""Figure 2: effective key-provisioning index vs. the channel error rate.

Compares the BB84 index over several fibre lengths against the ECDH rate for the
selected NIST prime curves.

Parameters live in config.py, formulas in model.py.
"""

import os
import matplotlib.pyplot as plt
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


plt.xscale('log')
plt.xlabel(cfg.XLABEL)
plt.ylabel(cfg.FIG2_YLABEL)
plt.grid(True, which="both", linestyle="-", alpha=0.5)
plt.legend(loc='upper left', fontsize=8)

os.makedirs(cfg.FIGURE_DIR, exist_ok=True)
plt.savefig(os.path.join(cfg.FIGURE_DIR, "provisioning_rate.pdf"), bbox_inches="tight")
plt.show()