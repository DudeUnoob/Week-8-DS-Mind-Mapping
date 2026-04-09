"""
SDG Mind Map: "SDG Progress 2030"
A detailed, visually rich mind map based on the 2025 SDG Report.

Central node  : SDG Progress 2030
Primary nodes : 5 (one per key SDG cluster)
Secondary nodes: 3 per primary = 15 total

All statistics sourced from:
  The Sustainable Development Goals Report 2025, United Nations
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import math

# ─── Color palette ────────────────────────────────────────────────────────────
BG         = "#0D1B2A"   # deep navy
GOLD       = "#F5C518"   # SDG gold
CTR_TEXT   = "#0D1B2A"

# Five branch colours (SDG-inspired)
COLORS = {
    "poverty":  "#E63946",  # red
    "health":   "#2A9D8F",  # teal
    "climate":  "#457B9D",  # steel blue
    "energy":   "#F4A261",  # amber
    "gender":   "#A8DADC",  # pale cyan
}

# Labels used in the icon for each branch (simple unicode symbols)
ICONS = {
    "poverty": "\u25C6",   # ◆  diamond
    "health":  "\u2665",   # ♥  heart
    "climate": "\u2299",   # ⊙  earth-like
    "energy":  "\u26A1",   # ⚡ bolt
    "gender":  "\u2640",   # ♀  female
}

# ─── Node data (literature-backed, 2025 report) ───────────────────────────────
PRIMARY_NODES = [
    # ── 1: No Poverty & Hunger ─────────────────────────────────────────────────
    {
        "key":   "poverty",
        "label": "No Poverty\n& Hunger",
        "stat":  "808 M in extreme poverty\n28% food insecure globally",
        "secondary": [
            {
                "label":  "Poverty Line\nRaised to $3/day",
                "detail": "1.5 B escaped poverty\n1990–2022 (World Bank)\nGoal 1 still severely off track",
                "symbol": "\u25AA",
            },
            {
                "label":  "2.3 Billion\nFood Insecure",
                "detail": "8.2% undernourished in 2024\n\u2191 from 7.8% in 2015\n(Goal 2 stagnating)",
                "symbol": "\u25AA",
            },
            {
                "label":  "Social Protection\n52.4% Covered",
                "detail": "3.8 B still unprotected\nLow-income: only 9.7%\n$1.4 T/yr gap to fill",
                "symbol": "\u25AA",
            },
        ],
    },
    # ── 2: Health & Education ──────────────────────────────────────────────────
    {
        "key":   "health",
        "label": "Health\n& Education",
        "stat":  "COVID reversed 1.8 yrs\nof life expectancy gains",
        "secondary": [
            {
                "label":  "HIV/AIDS\n40% Fewer Infections",
                "detail": "630 K AIDS deaths 2024\n\u2193 from 1.4 M in 2010\n1.3 M still infected in 2024",
                "symbol": "\u25AA",
            },
            {
                "label":  "272 Million\nOut of School",
                "detail": "Only 60% upper-sec.\ncompletion globally\n754 M adults illiterate",
                "symbol": "\u25AA",
            },
            {
                "label":  "14.7 M Health\nWorker Shortage",
                "detail": "1 worker per 621 people\nin low-income countries\nvs. 1 per 64 in high-income",
                "symbol": "\u25AA",
            },
        ],
    },
    # ── 3: Climate & Biodiversity ──────────────────────────────────────────────
    {
        "key":   "climate",
        "label": "Climate &\nBiodiversity",
        "stat":  "2024: Hottest year on record\n1.5\u00b0C threshold surpassed",
        "secondary": [
            {
                "label":  "CO\u2082 at\n2-Million-Yr High",
                "detail": "18% of SDG targets\nhave regressed since 2015\nClimate action off track",
                "symbol": "\u25AA",
            },
            {
                "label":  "120 M People\nDisplaced",
                "detail": "2\u00d7 more than in 2015\nConflict + climate shocks\nGoal 16 deteriorating",
                "symbol": "\u25AA",
            },
            {
                "label":  "Biodiversity\nPartial Progress",
                "detail": "Key ecosystem protection\ndoubled since 2015\nbut pace still insufficient",
                "symbol": "\u25AA",
            },
        ],
    },
    # ── 4: Energy & Digital ────────────────────────────────────────────────────
    {
        "key":   "energy",
        "label": "Energy\n& Digital",
        "stat":  "92% electricity access\nby 2023 globally",
        "secondary": [
            {
                "label":  "Renewables\nExpanding",
                "detail": "Goal 7 best SDG data\ncoverage (>80%)\nClean cooking still lagging",
                "symbol": "\u25AA",
            },
            {
                "label":  "Internet at 68%\nin 2024",
                "detail": "\u2191 from 40% in 2015\n70% connectivity growth\nGoal 9 moderate progress",
                "symbol": "\u25AA",
            },
            {
                "label":  "Digital Divide\nPersists",
                "detail": "AI & tech access unequal\n$4 T annual financing gap\nLDCs lack digital tools",
                "symbol": "\u25AA",
            },
        ],
    },
    # ── 5: Gender & Equity ─────────────────────────────────────────────────────
    {
        "key":   "gender",
        "label": "Gender\n& Equity",
        "stat":  "Women hold 27.2%\nof parliament seats",
        "secondary": [
            {
                "label":  "99 Legal Reforms\n2019–2024",
                "detail": "No country scores perfect\nacross all gender areas\n51% of nations have gaps",
                "symbol": "\u25AA",
            },
            {
                "label":  "1 in 5 Girls\nChild Marriage",
                "detail": "31% in Sub-Saharan Africa\n230 M affected by FGM\n4 M new cases annually",
                "symbol": "\u25AA",
            },
            {
                "label":  "Unpaid Care\nWork Disparity",
                "detail": "Women do 2.5\u00d7 more\nunpaid work than men\nLimits education & careers",
                "symbol": "\u25AA",
            },
        ],
    },
]

# Angles for the 5 primary nodes (degrees), top-first, clockwise
PRIMARY_ANGLES_DEG = [90, 18, -54, -126, -198]
PRIMARY_R   = 4.2
SECONDARY_R = 8.2

# Per-primary, spread of secondary angles (relative offsets in degrees)
SEC_OFFSETS = [28, 0, -28]


# ─── Drawing helpers ──────────────────────────────────────────────────────────

def fancy_box(ax, cx, cy, w, h, fc, ec="#FFFFFF", lw=1.2,
              alpha=1.0, zorder=5, radius=0.3):
    """Draw a rounded rectangle centred at (cx, cy)."""
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad={radius}",
        facecolor=fc, edgecolor=ec,
        linewidth=lw, alpha=alpha, zorder=zorder
    )
    ax.add_patch(box)


def text(ax, x, y, s, fs, color, bold=False, italic=False,
         ha="center", va="center", zorder=6, ls=1.35):
    weight = "bold" if bold else "normal"
    style  = "italic" if italic else "normal"
    ax.text(x, y, s, fontsize=fs, color=color,
            fontweight=weight, fontstyle=style,
            ha=ha, va=va, zorder=zorder,
            linespacing=ls, fontfamily="DejaVu Sans")


def branch(ax, x0, y0, x1, y1, color, lw=2.5, rad=0.12, zorder=2):
    ax.annotate(
        "",
        xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(
            arrowstyle="-",
            color=color, lw=lw,
            connectionstyle=f"arc3,rad={rad}",
        ),
        zorder=zorder,
    )


def dot(ax, x, y, color, r=0.14, zorder=7):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=zorder))


def glow(ax, x, y, r, color, alpha):
    ax.add_patch(plt.Circle((x, y), r, color=color, alpha=alpha, zorder=1))


# ─── Figure setup ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(26, 26))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-11.5, 11.5)
ax.set_ylim(-11.5, 11.5)
ax.set_aspect("equal")
ax.axis("off")

# Decorative concentric glows
for r_, a_ in [(10.8, 0.03), (8.5, 0.05), (6.0, 0.07), (3.5, 0.10)]:
    glow(ax, 0, 0, r_, "#1E4A7F", a_)

# ─── Header ───────────────────────────────────────────────────────────────────
text(ax, 0, 11.0,
     "SDG PROGRESS 2030  \u2014  Mind Map",
     fs=22, color=GOLD, bold=True, zorder=10)
text(ax, 0, 10.42,
     "Source: The Sustainable Development Goals Report 2025, United Nations",
     fs=10.5, color="#999999", italic=True, zorder=10)

# Horizontal divider line
ax.plot([-10.5, 10.5], [10.1, 10.1], color=GOLD, lw=0.8, alpha=0.5, zorder=10)

# ─── Central node ─────────────────────────────────────────────────────────────
# Pulsing rings
for r_, a_ in [(2.4, 0.12), (2.0, 0.22), (1.65, 0.35)]:
    glow(ax, 0, 0, r_, GOLD, a_)

fancy_box(ax, 0, 0, 3.0, 1.8, GOLD, ec="#FFE066", lw=2.5, zorder=5)
text(ax, 0,  0.25, "SDG Progress 2030",  fs=19, color=CTR_TEXT, bold=True, zorder=6)
text(ax, 0, -0.38,
     "35% on track  |  18% regressed\n48% insufficient progress\n(UN SDG Report, 2025)",
     fs=9.5, color="#222222", italic=True, zorder=6)

# 17 SDG colour dots as a wheel around centre
SDG_RING_COLS = [
    "#E5243B","#DDA63A","#4C9F38","#C5192D","#FF3A21",
    "#26BDE2","#FCC30B","#A21942","#FD6925","#DD1367",
    "#FD9D24","#BF8B2E","#3F7E44","#0A97D9","#56C02B",
    "#00689D","#19486A",
]
for idx, sc in enumerate(SDG_RING_COLS):
    a_ = math.radians(idx * 360 / 17 - 90)
    wx = 2.75 * math.cos(a_)
    wy = 2.75 * math.sin(a_)
    dot(ax, wx, wy, sc, r=0.16, zorder=7)

# Small centre star
text(ax, 0, 0.85, "\u2605", fs=11, color=CTR_TEXT, bold=True, zorder=7)

# ─── Primary & Secondary nodes ────────────────────────────────────────────────
for pnode, pa_deg in zip(PRIMARY_NODES, PRIMARY_ANGLES_DEG):
    key   = pnode["key"]
    col   = COLORS[key]
    icon  = ICONS[key]
    pa    = math.radians(pa_deg)

    px = PRIMARY_R * math.cos(pa)
    py = PRIMARY_R * math.sin(pa)

    # Glow behind primary
    glow(ax, px, py, 1.6, col, 0.15)

    # Branch centre → primary
    branch(ax, 0, 0, px, py, col, lw=3.2, rad=0.10)
    dot(ax, px, py, col, r=0.22, zorder=7)

    # Primary node box
    fancy_box(ax, px, py, 2.75, 1.7, col, ec="#FFFFFF", lw=1.5, zorder=5)
    # Icon symbol (top centre of box)
    text(ax, px, py + 0.50, icon, fs=15, color="#FFFFFF", bold=True, zorder=6)
    # Node label
    text(ax, px, py + 0.05, pnode["label"], fs=12.5, color="#FFFFFF", bold=True,
         zorder=6, ls=1.2)
    # Stat line
    text(ax, px, py - 0.60, pnode["stat"], fs=8.5, color="#FFFFCC",
         italic=True, zorder=6, ls=1.2)

    # ── Secondary nodes ────────────────────────────────────────────────────────
    for j, (snode, off_deg) in enumerate(zip(pnode["secondary"], SEC_OFFSETS)):
        sa  = math.radians(pa_deg + off_deg)
        sx  = SECONDARY_R * math.cos(sa)
        sy  = SECONDARY_R * math.sin(sa)

        # Branch primary → secondary
        branch(ax, px, py, sx, sy, col, lw=1.8, rad=0.15)
        dot(ax, sx, sy, col, r=0.11, zorder=7)

        # Secondary box
        fancy_box(ax, sx, sy, 2.7, 1.55, "#112233", ec=col, lw=1.4,
                  alpha=0.95, zorder=5, radius=0.25)
        # Title
        text(ax, sx, sy + 0.32, snode["label"],
             fs=9.5, color=col, bold=True, zorder=6, ls=1.2)
        # Detail
        text(ax, sx, sy - 0.40, snode["detail"],
             fs=7.8, color="#CCCCCC", italic=True, zorder=6, ls=1.3)

# ─── Six SDG Transitions strip (bottom area) ──────────────────────────────────
transitions = [
    ("Food\nSystems",    "#E63946"),
    ("Clean\nEnergy",    "#F4A261"),
    ("Digital\nConnect", "#2A9D8F"),
    ("Education",        "#457B9D"),
    ("Jobs & Social\nProtection", "#A8DADC"),
    ("Climate &\nBiodiversity",  "#56C02B"),
]

ax.plot([-10.5, 10.5], [-8.85, -8.85], color="#444455", lw=0.8, alpha=0.7, zorder=10)
text(ax, -6.2, -9.15,
     "6 Critical SDG Transitions called by UN Secretary-General Guterres, 2025:",
     fs=9, color="#AAAAAA", italic=True, ha="left", zorder=10)

for k, (tr_label, tr_col) in enumerate(transitions):
    tx = -10.0 + k * 3.38
    ty = -10.1
    fancy_box(ax, tx, ty, 3.0, 1.2, tr_col, ec="#FFFFFF", lw=0.9, alpha=0.88, zorder=8)
    text(ax, tx, ty, tr_label, fs=9, color="#FFFFFF", bold=True, zorder=9, ls=1.3)

# ─── Progress colour legend (top-left) ────────────────────────────────────────
legend_data = [
    ("#2ECC71", "On Track / Moderate Progress  (35%)"),
    ("#F39C12", "Marginal or Stagnated  (48%)"),
    ("#E74C3C", "Regressed below 2015 baseline  (18%)"),
]
lx, ly0 = -11.0, 9.3
text(ax, lx, ly0 + 0.55, "Global SDG Progress Status:", fs=9, color="#AAAAAA",
     ha="left", zorder=10)
for li, (lc, lt) in enumerate(legend_data):
    ly = ly0 - li * 0.60
    dot(ax, lx + 0.25, ly, lc, r=0.20, zorder=10)
    text(ax, lx + 0.65, ly, lt, fs=9, color="#CCCCCC", ha="left", zorder=10)

# ─── Key stat callouts (scattered small badges) ───────────────────────────────
callouts = [
    (-9.5, 2.5, "#E63946", "800 M+\nExtreme Poor"),
    (9.2,  2.5, "#2A9D8F", "40% \u2193 HIV\nsince 2010"),
    (-9.5, -2.5, "#457B9D", "120 M\nDisplaced"),
    (9.2, -2.5,  "#F4A261", "68% Internet\nAccess 2024"),
]
for bx, by, bc, bl in callouts:
    fancy_box(ax, bx, by, 2.3, 1.1, bc, ec="#FFFFFF", lw=0.9, alpha=0.75,
              zorder=4, radius=0.2)
    text(ax, bx, by, bl, fs=9, color="#FFFFFF", bold=True, zorder=5, ls=1.3)

# ─── Footer ───────────────────────────────────────────────────────────────────
ax.plot([-10.5, 10.5], [-11.1, -11.1], color=GOLD, lw=0.5, alpha=0.4, zorder=10)
text(ax, 0, -11.3,
     "\u2605  Only 5 years remain to achieve the 2030 Agenda.  "
     "\"We face a global development emergency.\"  \u2014 UN SG António Guterres, 2025  \u2605",
     fs=9.5, color=GOLD, italic=True, zorder=10)

# ─── Save ─────────────────────────────────────────────────────────────────────
OUT = "/workspace/SDG_MindMap_2030.pdf"
fig.savefig(OUT, format="pdf", bbox_inches="tight", dpi=200, facecolor=BG)
print(f"Saved: {OUT}")
plt.close(fig)
