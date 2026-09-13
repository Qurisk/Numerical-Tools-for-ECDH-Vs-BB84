"""Render the repository architecture diagram used in README.md.

Run from the repository root:  python docs/make_architecture.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

EDGE, FILL, ACCENT = "#3c4550", "#eef1f5", "#dbe4f0"
MONO = {"family": "monospace", "fontsize": 10.0, "color": "#1b1f24"}
SUB = {"fontsize": 8.4, "color": "#48515c"}


def box(ax, x, y, w, h, title, subtitle, fill=FILL):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                linewidth=1.1, edgecolor=EDGE, facecolor=fill))
    ax.text(x, y + 0.14, title, ha="center", va="center", **MONO)
    ax.text(x, y - 0.19, subtitle, ha="center", va="center", **SUB)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, linewidth=1.1,
                                shrinkA=0, shrinkB=0))


fig, ax = plt.subplots(figsize=(13.5, 5.2))
ax.set_xlim(0, 13.5)
ax.set_ylim(0.55, 5.55)
ax.axis("off")

CONFIG_X = 3.4
MODEL_X = 10.1
BUS = 4.0

SCRIPT_X = (2.2, 6.75, 11.3)

box(
    ax,
    CONFIG_X,
    4.9,
    5.1,
    0.95,
    "config.py",
    "user-editable parameters  (start here)",
    ACCENT
)

box(
    ax,
    MODEL_X,
    4.9,
    5.1,
    0.95,
    "model.py",
    "closed-form analytical model"
)

# Shared bus: all numerical scripts use config.py and model.py.
for x in (CONFIG_X, MODEL_X):
    ax.plot(
        [x, x],
        [4.425, BUS],
        color=EDGE,
        linewidth=1.1
    )

ax.plot(
    [SCRIPT_X[0], SCRIPT_X[-1]],
    [BUS, BUS],
    color=EDGE,
    linewidth=1.1
)

for x in SCRIPT_X:
    ax.plot(
        [x],
        [BUS],
        marker="o",
        markersize=4.5,
        color=EDGE
    )

    arrow(
        ax,
        x,
        BUS,
        x,
        3.33
    )

box(
    ax,
    SCRIPT_X[0],
    2.82,
    4.1,
    0.95,
    "ECDHvsQKD_perf_chan.py",
    "Figure 1 of Section 5"
)

box(
    ax,
    SCRIPT_X[1],
    2.82,
    4.4,
    0.95,
    "effective_key_material_provisioning_rate.py",
    "Figure 2 of Section 5"
)

box(
    ax,
    SCRIPT_X[2],
    2.82,
    3.3,
    0.95,
    "solver.py",
    "R_KP break-even solvers"
)

for x in SCRIPT_X:
    arrow(
        ax,
        x,
        2.345,
        x,
        1.70
    )

box(
    ax,
    SCRIPT_X[0],
    1.18,
    4.1,
    0.95,
    "figures/failure_probability.pdf",
    "protocol-level failure figure"
)

box(
    ax,
    SCRIPT_X[1],
    1.18,
    4.4,
    0.95,
    "figures/provisioning_rate.pdf",
    "key-provisioning figure"
)

box(
    ax,
    SCRIPT_X[2],
    1.18,
    3.6,
    0.95,
    "figures/break_even_*.pdf",
    "plots intersections; prints d* and eps_ch*"
)

fig.tight_layout(pad=0.3)

fig.savefig(
    "docs/architecture.png",
    dpi=200,
    facecolor="white"
)

fig.savefig(
    "docs/architecture.pdf",
    facecolor="white"
)

print(
    "wrote docs/architecture.png and docs/architecture.pdf"
)
