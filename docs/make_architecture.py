"""Render the repository architecture diagram used in README.md.

Run from the repository root:  python docs/make_architecture.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

EDGE, FILL, ACCENT = "#3c4550", "#eef1f5", "#dbe4f0"
MONO = {"family": "monospace", "fontsize": 10.5, "color": "#1b1f24"}
SUB = {"fontsize": 8.8, "color": "#48515c"}


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


fig, ax = plt.subplots(figsize=(10.5, 5.0))
ax.set_xlim(0, 10.5); ax.set_ylim(0.6, 5.45); ax.axis("off")

LEFT, RIGHT, BUS = 2.75, 7.75, 3.95

box(ax, LEFT, 4.85, 4.3, 0.95, "config.py", "configuration file for users  (start here)", ACCENT)
box(ax, RIGHT, 4.85, 4.3, 0.95, "model.py", "provides functions for formulae")

# shared bus: both scripts import both modules
for x in (LEFT, RIGHT):
    ax.plot([x, x], [4.375, BUS], color=EDGE, linewidth=1.1)
ax.plot([LEFT, RIGHT], [BUS, BUS], color=EDGE, linewidth=1.1)
for x in (LEFT, RIGHT):
    ax.plot([x], [BUS], marker="o", markersize=4.5, color=EDGE)  # junction: both scripts use both modules
    arrow(ax, x, BUS, x, 3.28)

box(ax, LEFT, 2.8, 4.6, 0.95, "ECDHvsQKD_perf_chan.py", "Figure 1 of Section 5")
box(ax, RIGHT, 2.8, 4.9, 0.95, "effective_key_material_provisioning_rate.py", "Figure 2 of Section 5")

for x in (LEFT, RIGHT):
    arrow(ax, x, 2.325, x, 1.68)

box(ax, LEFT, 1.2, 4.6, 0.95, "figures/failure_probability.pdf", "expected sifted detections")
box(ax, RIGHT, 1.2, 4.9, 0.95, "figures/provisioning_rate.pdf",
    "break-even distance and error rate")

fig.tight_layout(pad=0.3)
fig.savefig("docs/architecture.png", dpi=200, facecolor="white")
fig.savefig("docs/architecture.pdf", facecolor="white")
print("wrote docs/architecture.png and docs/architecture.pdf")
