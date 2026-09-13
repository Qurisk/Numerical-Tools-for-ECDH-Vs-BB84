"""Closed-form models for the ECDH vs. BB84 key-provisioning comparison.

Pure functions only: no module-level state, no configuration, no plotting.
Every formula used by the figure scripts appears here exactly once.

Symbols follow the paper:
    eps_ch  channel error rate                     [0;1]
    eta     overall transmittance (channel x detector)
    pd      dark-count probability                 [0;1]
    p_bs    probability of a matching basis choice
    npk     public-key length                      [bit]
    St      security strength                      [bit]
"""

import numpy as np
from scipy.stats import binom


# --- channel and detection ---------------------------------------------------

def transmittance(d_km, alpha_db_km):
    """Fibre transmittance over d_km at a loss of alpha_db_km."""
    return 10 ** (-(alpha_db_km * d_km) / 10)


def basis_match(p_b):
    """Probability that Alice and Bob select the same basis."""
    return p_b ** 2 + (1 - p_b) ** 2


def sifted_yield(eta, pd, p_bs):
    """Probability that an emitted signal produces a sifted detection."""
    return p_bs * (eta + (1 - eta) * pd)


def qber(eps_ch, eta, pd):
    """Quantum bit error rate, dark counts contributing at one half."""
    return (eta * eps_ch + 0.5 * (1 - eta) * pd) / (eta + (1 - eta) * pd)


# --- key-provisioning index ----------------------------------------

def binary_entropy(x):
    """Binary Shannon entropy H2(x), in bits, with H2(0)=H2(1)=0."""
    x = np.asarray(x, dtype=float)

    with np.errstate(divide="ignore", invalid="ignore"):
        h = -x * np.log2(x) - (1 - x) * np.log2(1 - x)

    return np.where((x == 0) | (x == 1), 0.0, h)


def secret_fraction(q):
    """Asymptotic BB84 secret-key fraction r_inf, clipped at zero."""
    return np.maximum(0, 1 - 2 * binary_entropy(q))


def rate_bb84(eps_ch, eta, pd, p_bs):
    """BB84 key-provisioning index R_KP, per emitted signal."""
    return secret_fraction(qber(eps_ch, eta, pd)) * sifted_yield(eta, pd, p_bs)


def rate_ecdh(eps_ch, strength_bits, npk_bits):
    """ECDH key-provisioning index R_KP, per channel use."""
    return (strength_bits / (2 * npk_bits)) * (1 - binary_entropy(eps_ch))


# --- failure probabilities ---------------------------------------------------

def n_sifted(n_signals, eta, pd, p_bs):
    """Expected number of sifted detections out of n_signals emitted."""
    return int(round(n_signals * sifted_yield(eta, pd, p_bs)))


def p_abort_bb84(eps_ch, n_sift, eta, pd, qber_threshold):
    """Probability that the observed QBER exceeds the abort threshold."""
    threshold = int(np.floor(n_sift * qber_threshold))
    return binom.sf(threshold, n_sift, qber(eps_ch, eta, pd))


def p_fail_uncoded(eps_ch, npk_bits):
    """Probability that an uncoded npk-bit public key is corrupted."""
    return 1 - (1 - eps_ch) ** npk_bits


def p_fail_coded(eps_ch, n, t, n_codewords):
    """Probability that a public key carried by n_codewords (n,k,t) words fails."""
    return 1 - (1 - binom.sf(t, n, eps_ch)) ** n_codewords


def p_fail_exchange(p_fail_tx):
    """A full exchange needs both public keys to arrive intact."""
    return 1 - (1 - p_fail_tx) ** 2
