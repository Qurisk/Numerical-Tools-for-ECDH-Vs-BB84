"""Figure 1: probability of a failed key exchange vs. the channel error rate.

Compares the BB84 abort probability against the probability that an ECDH
public key is corrupted in transit, with and without error-correcting codes.

Parameters live in config.py, formulas in model.py.
"""

import os

import matplotlib.pyplot as plt

import config as cfg
import model

eps = cfg.FIG1_EPS
eta = cfg.FIG1_ETA_CH * cfg.ETA_DET
p_bs = model.basis_match(cfg.P_B)

n_sift = model.n_sifted(cfg.FIG1_N_SIGNAL, eta, cfg.PD, p_bs)
print(f"Expected number of sifted detections = {n_sift}")

if cfg.FIG1_SHOW_QBER:
    plt.plot(eps, model.qber(eps, eta, cfg.PD), label=r'$QBER_{ref}$')

if cfg.FIG1_SHOW_BB84:
    plt.plot(eps, model.p_abort_bb84(eps, n_sift, eta, cfg.PD, cfg.FIG1_QBER_TH),
             label=r'$p_{f,tx}$ (BB84)')

for name in cfg.FIG1_UNCODED:
    _, npk = cfg.CURVES[name]
    p_tx = model.p_fail_uncoded(eps, npk)
    plt.plot(eps, model.p_fail_exchange(p_tx),
             label=rf'$p_{{f,ex}}$ ({name} unc.)')

for name, code in cfg.FIG1_CODED:
    n, _k, t, n_cw = cfg.CODES[(name, code)]
    p_tx = model.p_fail_coded(eps, n, t, n_cw)
    plt.plot(eps, model.p_fail_exchange(p_tx),
             label=rf'$p_{{f,ex}}$({name} unc.+$C_{code[1:]}$)')

plt.xscale('log')
plt.xlabel(cfg.XLABEL)
plt.ylabel(cfg.FIG1_YLABEL)
plt.grid(True, which="both", linestyle="-", alpha=0.5)
plt.legend(loc='upper left', fontsize=8)

os.makedirs(cfg.FIGURE_DIR, exist_ok=True)
plt.savefig(os.path.join(cfg.FIGURE_DIR, "failure_probability.pdf"), bbox_inches="tight")
plt.show()
