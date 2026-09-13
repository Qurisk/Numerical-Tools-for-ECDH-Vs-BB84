"""User-editable parameters for the numerical tools.

Everything a reader may want to change lives here; model.py holds the formulas,
and the numerical scripts assemble, solve, and plot. Edit this file, not those.
"""

import numpy as np

# =============================================================================
# Physical parameters
#
# These values generated the published figures. Changing them changes the
# figures; the paper quotes them as they stand.
# =============================================================================

ETA_DET = 0.75              # detector efficiency               [0;1]
PD      = 1e-7              # dark-count probability            [0;1]
P_B     = 0.5               # probability of selecting one basis
ALPHA   = 0.2               # fibre loss                        [dB/km]

# =============================================================================
# Elliptic curves and error-correcting codes
# =============================================================================

# curve : (security strength St [bit], uncompressed public key npk [bit])
CURVES = {
    "P-256": (128, 520),
    "P-384": (192, 776),
    "P-521": (256, 1064),
}

# (curve, code) : (n, k, t, number of codewords per public key)
CODES = {
    ("P-256", "C1"): (650, 520, 13, 1),     # rate R = 0.8
    ("P-384", "C1"): (971, 776, 20, 1),
    ("P-521", "C1"): (662, 532, 13, 2),
    ("P-256", "C2"): (865, 520, 37, 1),     # rate R = 0.6
    ("P-384", "C2"): (643, 388, 26, 2),
    ("P-521", "C2"): (887, 532, 38, 2),
}

# =============================================================================
# Figure 1 -- failure probability vs. channel error rate
# =============================================================================

FIG1_EPS = np.logspace(-6, 0, 500)      # channel error rate sweep

FIG1_ETA_CH   = 1e-3                    # fixed channel transmittance   [0;1]
FIG1_N_SIGNAL = 10 ** 6                 # number of emitted signals
FIG1_QBER_TH  = 0.11                    # BB84 abort threshold

# Curves drawn. Comment out an entry to drop it from the figure.
FIG1_SHOW_QBER    = False                            # QBER reference curve
FIG1_SHOW_BB84    = True                            # BB84 abort probability
FIG1_UNCODED      = ["P-256", "P-384", "P-521"]     # ECDH without coding
FIG1_CODED        = [                               # ECDH with coding
    ("P-256", "C1"),
    ("P-256", "C2"),
]

# =============================================================================
# Figure 2 -- key-provisioning index vs. channel error rate
# =============================================================================

FIG2_EPS = np.logspace(-5, np.log10(0.5), 500)

FIG2_CURVES      = ["P-256"]                # ECDH curves drawn
FIG2_DISTANCES_KM = [15, 20, 25, 30]        # BB84 links drawn

# =============================================================================
# Solver operating point
#
# Used by solver.py. It is independent of Figure 2 and tracks the
# physical parameters above except where a CUSTOM value deliberately overrides one.
# =============================================================================

ETA_DET_CUSTOM = 0.70       # deliberately more conservative than ETA_DET
PD_CUSTOM      = PD
P_B_CUSTOM     = P_B
ALPHA_CUSTOM   = ALPHA

SOLVER_CURVE = "P-256"      # curve whose St and npk the solver compares against

# Solved for distance at this channel error rate:
ECH_TARGET   = 5e-2
D_BRACKET_KM = (0, 500)     # search bracket for brentq

# Solved for channel error rate at this distance:
D_TARGET_KM  = 18
ECH_BRACKET  = (1e-6, 1e-1) # search bracket for brentq
SOLVER_PLOT_POINTS = 500

# =============================================================================
# Output
# =============================================================================

FIGURE_DIR = "figures"

# =============================================================================
# Axis labels
#
# Both figures sweep the same unified channel-error parameter, so they share an
# x label.
# =============================================================================

XLABEL          = r"Unified channel-error parameter $\varepsilon_{ch}$"
FIG1_YLABEL     = r"Protocol-level failure probability"
FIG2_YLABEL     = r"Key-provisioning index $\mathcal{R}_{\mathrm{KP}}$"
DISTANCE_XLABEL = r"Fibre distance $d$ [km]"