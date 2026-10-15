#!/usr/bin/env python3
"""EXP-001: generate the KDP coloring-book deliverables (interior.pdf, cover.pdf).

Everything is vector line art drawn from equations — deterministic (seeded), no
image models, no network. KDP specs this targets:

- Interior: 8.5x11 in, no bleed, all ink >= 0.5 in from every edge (KDP needs
  0.25 outside / 0.375 gutter at this page count). Designs sit on right-hand
  pages with blank backs so markers cannot bleed through onto the next design.
  Page count must stay in 24..110 so the print cost stays $2.84 (large trim,
  black ink).
- Cover: one full spread (back + spine + front) with 0.125 in bleed. Spine
  width for black-ink/white-paper is pages * 0.002252 in. The bottom-right
  2.0x1.2 in of the back cover is left white for Amazon's barcode.

Run:  .venv/bin/python experiments/kdp-coloring-book/generate.py
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Arc, Circle, Polygon, Rectangle

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 8.5, 11.0
MARGIN = 0.6            # inches of white around all ink (> the 0.375 gutter rule)
ART = 7.0               # the art box is ART x ART inches, centered, above the caption
INK = "#111111"

TITLE = "MATHEMATICAL PATTERNS"
SUBTITLE = "A Coloring Book of 50 Geometric Designs"
TAGLINE = "fractals · spirals · tilings · mandalas"
AUTHOR = "Junyi Zhou"
YEAR = "2026"


# ---------------------------------------------------------------- page helpers
def blank_fig():
    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.patch.set_facecolor("white")
    return fig


def design_page(pdf, title, note, draw):
    """One design: square art box centered, caption at the bottom."""
    fig = blank_fig()
    side = ART / PAGE_W, ART / PAGE_H
    ax = fig.add_axes([(1 - side[0]) / 2, 0.16, side[0], side[1]])
    ax.set_aspect("equal")
    ax.axis("off")
    draw(ax)
    fig.text(0.5, 0.105, title, ha="center", va="center", fontsize=13, weight="bold", color=INK)
    fig.text(0.5, 0.082, note, ha="center", va="center", fontsize=8.5, color="#444444", style="italic")
    fig.text(0.5, MARGIN / PAGE_H * 0.8, "", ha="center")  # keep layout stable
    pdf.savefig(fig)
    plt.close(fig)


def blank_page(pdf):
    fig = blank_fig()
    pdf.savefig(fig)
    plt.close(fig)


def plot(ax, x, y, lw=1.4):
    ax.plot(x, y, color=INK, lw=lw, solid_capstyle="round", solid_joinstyle="round")


# ------------------------------------------------------------------ the designs
def d_rose(k, turns=2):
    def draw(ax):
        t = np.linspace(0, turns * 2 * math.pi, 4000)
        r = np.cos(k * t)
        plot(ax, r * np.cos(t), r * np.sin(t), lw=1.6)
        ax.add_patch(Circle((0, 0), 1.02, fill=False, ec=INK, lw=1.2))
    return draw


def d_lissajous(a, b, delta):
    def draw(ax):
        t = np.linspace(0, 2 * math.pi, 5000)
        plot(ax, np.sin(a * t + delta), np.sin(b * t), lw=1.6)
    return draw


def d_spiro(R, r, d, epi=False):
    def draw(ax):
        g = math.gcd(R, r)
        turns = r // g
        t = np.linspace(0, turns * 2 * math.pi, 9000)
        if epi:
            x = (R + r) * np.cos(t) - d * np.cos((R + r) / r * t)
            y = (R + r) * np.sin(t) - d * np.sin((R + r) / r * t)
        else:
            x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
            y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)
        plot(ax, x, y, lw=1.1)
    return draw


def d_mandala(seed):
    def draw(ax):
        rng = random.Random(seed)
        n = rng.choice([8, 10, 12, 16])
        ax.add_patch(Circle((0, 0), 0.08, fill=False, ec=INK, lw=1.4))
        r0 = 0.12
        while r0 < 0.95:
            kind = rng.choice(["petal", "arc", "dots", "zig", "ring"])
            band = rng.uniform(0.10, 0.22)
            r1 = min(r0 + band, 0.98)
            w = r1 - r0  # effective width: band may have been clamped at the rim
            if kind == "ring":
                ax.add_patch(Circle((0, 0), r1, fill=False, ec=INK, lw=1.3))
            else:
                for i in range(n):
                    th = 2 * math.pi * i / n
                    if kind == "petal":
                        t = np.linspace(0, 1, 60)
                        w = 0.9 * math.pi / n
                        rr = r0 + (r1 - r0) * np.sin(math.pi * t)
                        aa = th + w * (2 * t - 1) * np.sin(math.pi * t)
                        plot(ax, rr * np.cos(aa), rr * np.sin(aa), lw=1.3)
                    elif kind == "arc":
                        a0 = math.degrees(th) - 160 / n
                        ax.add_patch(Arc((0, 0), 2 * (r0 + w / 2), 2 * (r0 + w / 2),
                                         theta1=a0, theta2=a0 + 320 / n, ec=INK, lw=1.3))
                    elif kind == "dots":
                        rr = r0 + w / 2
                        ax.add_patch(Circle((rr * math.cos(th), rr * math.sin(th)),
                                            w / 3.2, fill=False, ec=INK, lw=1.2))
                    elif kind == "zig":
                        th2 = 2 * math.pi * (i + 0.5) / n
                        plot(ax, [r0 * math.cos(th), r1 * math.cos(th2)],
                             [r0 * math.sin(th), r1 * math.sin(th2)], lw=1.2)
                        plot(ax, [r1 * math.cos(th2), r0 * math.cos(2 * math.pi * (i + 1) / n)],
                             [r1 * math.sin(th2), r0 * math.sin(2 * math.pi * (i + 1) / n)], lw=1.2)
            r0 = r1
        ax.add_patch(Circle((0, 0), 1.0, fill=False, ec=INK, lw=1.6))
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05)
    return draw


def d_phyllotaxis(n, grow):
    def draw(ax):
        golden = math.pi * (3 - math.sqrt(5))
        for i in range(1, n):
            r = math.sqrt(i / n)
            th = i * golden
            size = (0.012 + 0.030 * r) if grow else 0.020
            ax.add_patch(Circle((r * math.cos(th), r * math.sin(th)), size,
                                fill=False, ec=INK, lw=0.9))
        ax.add_patch(Circle((0, 0), 1.03, fill=False, ec=INK, lw=1.4))
        ax.set_xlim(-1.08, 1.08); ax.set_ylim(-1.08, 1.08)
    return draw


def d_koch(inward):
    def draw(ax):
        # L-system turtle: axiom F--F--F, rule F -> F+F--F+F, 60-degree turns.
        seq = "F--F--F"
        for _ in range(4):
            seq = seq.replace("F", "F+F--F+F")
        sign = -1.0 if inward else 1.0
        ang = 0.0
        x = y = 0.0
        xs, ys = [x], [y]
        for ch in seq:
            if ch == "F":
                x += math.cos(ang); y += math.sin(ang)
                xs.append(x); ys.append(y)
            elif ch == "+":
                ang += sign * math.pi / 3
            elif ch == "-":
                ang -= sign * math.pi / 3
        xs = np.array(xs); ys = np.array(ys)
        cx, cy = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
        s = 2.0 / max(xs.max() - xs.min(), ys.max() - ys.min())
        plot(ax, (xs - cx) * s, (ys - cy) * s, lw=1.1)
        ax.add_patch(Circle((0, 0), 0.22, fill=False, ec=INK, lw=1.2))
    return draw


def d_sierpinski():
    def draw(ax):
        def rec(p, size, depth):
            if depth == 0:
                tri = [(p[0], p[1]), (p[0] + size, p[1]), (p[0] + size / 2, p[1] + size * math.sqrt(3) / 2)]
                ax.add_patch(Polygon(tri, closed=True, fill=False, ec=INK, lw=1.0))
                return
            h = size / 2
            rec(p, h, depth - 1)
            rec((p[0] + h, p[1]), h, depth - 1)
            rec((p[0] + h / 2, p[1] + h * math.sqrt(3) / 2), h, depth - 1)
        rec((-1, -0.85), 2, 5)
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-0.95, 1.0)
    return draw


def d_hilbert(order=5):
    def draw(ax):
        # Hilbert curve by coordinate transform of the index.
        n = 2 ** order
        def d2xy(d):
            x = y = 0
            s = 1
            while s < n:
                rx = 1 & (d // 2)
                ry = 1 & (d ^ rx)
                if ry == 0:
                    if rx == 1:
                        x, y = s - 1 - x, s - 1 - y
                    x, y = y, x
                x += s * rx
                y += s * ry
                d //= 4
                s *= 2
            return x, y
        pts = [d2xy(i) for i in range(n * n)]
        xs = [2 * p[0] / (n - 1) - 1 for p in pts]
        ys = [2 * p[1] / (n - 1) - 1 for p in pts]
        plot(ax, xs, ys, lw=1.0)
    return draw


def d_dragon(order=12):
    def draw(ax):
        turns = [1]
        for _ in range(order - 1):
            turns = turns + [1] + [-t for t in reversed(turns)]
        x, y, dx, dy = 0.0, 0.0, 1.0, 0.0
        xs, ys = [x], [y]
        for t in [0] + turns:
            if t == 1:
                dx, dy = -dy, dx
            elif t == -1:
                dx, dy = dy, -dx
            x += dx; y += dy
            xs.append(x); ys.append(y)
        xs = np.array(xs); ys = np.array(ys)
        cx, cy = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
        s = 2.0 / max(xs.max() - xs.min(), ys.max() - ys.min())
        plot(ax, (xs - cx) * s, (ys - cy) * s, lw=0.9)
    return draw


def d_tree(spread, ratio):
    def draw(ax):
        def rec(x, y, ang, length, depth):
            if depth == 0:
                return
            x2 = x + length * math.cos(ang)
            y2 = y + length * math.sin(ang)
            plot(ax, [x, x2], [y, y2], lw=0.8 + 0.22 * depth)
            rec(x2, y2, ang + spread, length * ratio, depth - 1)
            rec(x2, y2, ang - spread, length * ratio, depth - 1)
        rec(0, -1.0, math.pi / 2, 0.55, 9)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.05, 1.15)
    return draw


def d_truchet(seed, nx=11, ny=11):
    def draw(ax):
        rng = random.Random(seed)
        s = 2.0 / nx
        for i in range(nx):
            for j in range(ny):
                x0, y0 = -1 + i * s, -1 + j * s
                if rng.random() < 0.5:
                    ax.add_patch(Arc((x0, y0), s, s, theta1=0, theta2=90, ec=INK, lw=1.3))
                    ax.add_patch(Arc((x0 + s, y0 + s), s, s, theta1=180, theta2=270, ec=INK, lw=1.3))
                else:
                    ax.add_patch(Arc((x0 + s, y0), s, s, theta1=90, theta2=180, ec=INK, lw=1.3))
                    ax.add_patch(Arc((x0, y0 + s), s, s, theta1=270, theta2=360, ec=INK, lw=1.3))
        ax.add_patch(Rectangle((-1, -1), 2, 2 * ny / nx, fill=False, ec=INK, lw=1.4))
        ax.set_xlim(-1.03, 1.03); ax.set_ylim(-1.03, -1 + 2 * ny / nx + 0.03)
    return draw


def _star(ax, cx, cy, r, n, k, lw=1.2, rot=0.0):
    pts = [(cx + r * math.cos(rot + 2 * math.pi * (i * k % n) / n),
            cy + r * math.sin(rot + 2 * math.pi * (i * k % n) / n)) for i in range(n)]
    pts.append(pts[0])
    plot(ax, [p[0] for p in pts], [p[1] for p in pts], lw=lw)


def d_star_grid(n, k):
    def draw(ax):
        step = 0.5
        for i in range(-2, 3):
            for j in range(-2, 3):
                cx, cy = i * step * 2, j * step * 2
                if abs(cx) <= 1.01 and abs(cy) <= 1.01:
                    _star(ax, cx, cy, step * 0.95, n, k, rot=math.pi / n)
                    ax.add_patch(Circle((cx, cy), step * 0.32, fill=False, ec=INK, lw=1.0))
        ax.add_patch(Rectangle((-1.5, -1.5), 3, 3, fill=False, ec=INK, lw=1.4))
        ax.set_xlim(-1.53, 1.53); ax.set_ylim(-1.53, 1.53)
    return draw


def d_star_nest(n, k):
    def draw(ax):
        for s in (1.0, 0.78, 0.56, 0.34):
            _star(ax, 0, 0, s, n, k, lw=1.4, rot=math.pi / 2)
        ax.add_patch(Circle((0, 0), 1.04, fill=False, ec=INK, lw=1.4))
        ax.set_xlim(-1.08, 1.08); ax.set_ylim(-1.08, 1.08)
    return draw


def d_rhombille():
    def draw(ax):
        s = 0.24
        for q in range(-5, 6):
            for r in range(-5, 6):
                cx = s * 1.5 * q
                cy = s * math.sqrt(3) * (r + q / 2)
                if abs(cx) > 1.0 or abs(cy) > 1.0:
                    continue
                hexpts = [(cx + s * math.cos(a), cy + s * math.sin(a))
                          for a in [math.pi / 3 * i for i in range(6)]]
                ax.add_patch(Polygon(hexpts, closed=True, fill=False, ec=INK, lw=1.1))
                for i in (0, 2, 4):
                    plot(ax, [cx, hexpts[i][0]], [cy, hexpts[i][1]], lw=1.1)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1)
    return draw


def d_circlepack(seed):
    def draw(ax):
        rng = random.Random(seed)
        placed = []
        tries = 0
        while len(placed) < 110 and tries < 30000:
            tries += 1
            x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
            lim = 1.0 - math.hypot(x, y)
            if lim <= 0.03:
                continue
            r = min(lim, min((math.hypot(x - a, y - b) - c for a, b, c in placed), default=lim))
            if r < 0.035:
                continue
            r = min(r, rng.uniform(0.05, 0.28))
            if r < 0.035:
                continue
            placed.append((x, y, r))
        for x, y, r in placed:
            ax.add_patch(Circle((x, y), r, fill=False, ec=INK, lw=1.2))
        ax.add_patch(Circle((0, 0), 1.0, fill=False, ec=INK, lw=1.5))
        ax.set_xlim(-1.04, 1.04); ax.set_ylim(-1.04, 1.04)
    return draw


def d_apollonian():
    def draw(ax):
        # Descartes circle theorem, three equal starter circles in a unit circle.
        def complex_c(c):
            return complex(c[0], c[1])
        r = 2 * math.sqrt(3) - 3
        start = []
        for i in range(3):
            a = math.pi / 2 + 2 * math.pi * i / 3
            start.append(((1 - r) * math.cos(a), (1 - r) * math.sin(a), r))
        outer = (0.0, 0.0, 1.0)
        circles = [outer] + start

        def curv(c, outer_c=False):
            return (-1 if outer_c else 1) / c[2]

        def fits(c4, existing):
            # inside the unit circle, and tangent-or-apart from every other circle
            # (no overlap and no containment — tangency, d == r + r4, passes)
            if math.hypot(c4[0], c4[1]) + c4[2] > 1.001:
                return False
            for a, b, r in existing[1:]:
                d = math.hypot(c4[0] - a, c4[1] - b)
                if d < r + c4[2] - 1e-3:
                    return False
            return True

        def next_circle(c1, k1, c2, k2, c3, k3, existing):
            k4 = k1 + k2 + k3 + 2 * math.sqrt(max(k1 * k2 + k2 * k3 + k3 * k1, 0))
            if k4 <= 0:
                return None
            z1, z2, z3 = complex_c(c1), complex_c(c2), complex_c(c3)
            root = 2 * (k1 * k2 * z1 * z2 + k2 * k3 * z2 * z3 + k3 * k1 * z3 * z1) ** 0.5
            num = z1 * k1 + z2 * k2 + z3 * k3
            for z4 in ((num + root) / k4, (num - root) / k4):
                c4 = (z4.real, z4.imag, 1 / k4)
                if fits(c4, existing):
                    return c4
            return None

        triples = [(outer, curv(outer, True), start[0], curv(start[0]), start[1], curv(start[1])),
                   (outer, curv(outer, True), start[1], curv(start[1]), start[2], curv(start[2])),
                   (outer, curv(outer, True), start[2], curv(start[2]), start[0], curv(start[0])),
                   (start[0], curv(start[0]), start[1], curv(start[1]), start[2], curv(start[2]))]
        for depth in range(4):
            new_triples = []
            for c1, k1, c2, k2, c3, k3 in triples:
                c4 = next_circle(c1, k1, c2, k2, c3, k3, circles)
                if not c4 or c4[2] < 0.015:
                    continue
                circles.append(c4)
                k4 = 1 / c4[2]
                new_triples += [(c1, k1, c2, k2, c4, k4), (c2, k2, c3, k3, c4, k4), (c1, k1, c3, k3, c4, k4)]
            triples = new_triples
        for x, y, r0 in circles:
            ax.add_patch(Circle((x, y), r0, fill=False, ec=INK, lw=1.1))
        ax.set_xlim(-1.04, 1.04); ax.set_ylim(-1.04, 1.04)
    return draw


def d_torus_knot(p, q):
    def draw(ax):
        t = np.linspace(0, 2 * math.pi, 5000)
        r = 0.62 + 0.38 * np.cos(q * t)
        x = r * np.cos(p * t)
        y = r * np.sin(p * t)
        plot(ax, x, y, lw=1.5)
        ax.add_patch(Circle((0, 0), 1.03, fill=False, ec=INK, lw=1.2))
    return draw


def d_golden():
    def draw(ax):
        # squares laid out by successive subdivision of a 21x13 Fibonacci rectangle
        sq = []
        gx, gy, gw, gh = 0.0, 0.0, 21.0, 13.0
        order = ["L", "B", "R", "T", "L", "B", "R"]
        sizes = [13, 8, 5, 3, 2, 1, 1]
        for side, s in zip(order, sizes):
            if side == "L":
                sq.append((gx, gy, s)); gx += s; gw -= s
            elif side == "B":
                sq.append((gx, gy, s)); gy += s; gh -= s
            elif side == "R":
                sq.append((gx + gw - s, gy, s)); gw -= s
            elif side == "T":
                sq.append((gx, gy + gh - s, s)); gh -= s
        scale = 2.0 / 21.0
        for (sx, sy, s) in sq:
            ax.add_patch(Rectangle((sx * scale - 1, sy * scale - 13 / 21), s * scale, s * scale,
                                   fill=False, ec=INK, lw=1.2))
        arcs = [((13, 13), 13, 180, 270), ((13, 8), 8, 270, 360), ((16, 8), 5, 0, 90),
                ((16, 10), 3, 90, 180), ((15, 10), 2, 180, 270), ((15, 9), 1, 270, 360), ((15, 9), 1, 0, 90)]
        for (cx0, cy0), rr, a0, a1 in arcs:
            ax.add_patch(Arc((cx0 * scale - 1, cy0 * scale - 13 / 21), 2 * rr * scale, 2 * rr * scale,
                             theta1=a0, theta2=a1, ec=INK, lw=1.6))
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-0.72, 0.62)
    return draw


def d_moire(radial):
    def draw(ax):
        if radial:
            for r in np.arange(0.08, 1.4, 0.08):
                ax.add_patch(Circle((-0.3, 0), r, fill=False, ec=INK, lw=1.0))
                ax.add_patch(Circle((0.3, 0), r, fill=False, ec=INK, lw=1.0))
            ax.add_patch(Rectangle((-1, -1), 2, 2, fill=False, ec="white", lw=0))
            ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
            clip = Rectangle((-1, -1), 2, 2, fill=False, ec=INK, lw=1.5)
            ax.add_patch(clip)
            for p in ax.patches:
                p.set_clip_path(clip)
        else:
            for r in np.arange(0.07, 1.0, 0.065):
                ax.add_patch(Circle((0, 0), r, fill=False, ec=INK, lw=1.0))
            for i in range(36):
                a = 2 * math.pi * i / 36
                plot(ax, [0.07 * math.cos(a), math.cos(a)], [0.07 * math.sin(a), math.sin(a)], lw=1.0)
            ax.add_patch(Circle((0, 0), 1.0, fill=False, ec=INK, lw=1.5))
            ax.set_xlim(-1.03, 1.03); ax.set_ylim(-1.03, 1.03)
    return draw


def d_superellipse():
    def draw(ax):
        t = np.linspace(0, 2 * math.pi, 2000)
        for n, s in [(0.6, 1.0), (1.0, 0.85), (1.6, 0.7), (2.5, 0.55), (4.0, 0.4), (8.0, 0.25)]:
            x = s * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** (2 / n)
            y = s * np.sign(np.sin(t)) * np.abs(np.sin(t)) ** (2 / n)
            plot(ax, x, y, lw=1.4)
    return draw


def d_harmonograph(seed):
    def draw(ax):
        rng = random.Random(seed)
        f1, f2 = rng.choice([(3.001, 2.0), (2.01, 3.0), (5.002, 4.0)])
        p1, p2 = rng.uniform(0, math.pi), rng.uniform(0, math.pi)
        d1, d2 = 0.004, 0.0065
        t = np.linspace(0, 60, 20000)
        x = np.sin(f1 * t + p1) * np.exp(-d1 * t) + 0.3 * np.sin(f2 * t) * np.exp(-d2 * t)
        y = np.sin(f2 * t + p2) * np.exp(-d1 * t) + 0.3 * np.sin(f1 * t) * np.exp(-d2 * t)
        m = max(np.abs(x).max(), np.abs(y).max())
        plot(ax, x / m, y / m, lw=0.75)
    return draw


def d_chladni(n, m):
    def draw(ax):
        g = np.linspace(-1, 1, 500)
        X, Y = np.meshgrid(g, g)
        Z = np.cos(n * math.pi * X) * np.cos(m * math.pi * Y) - np.cos(m * math.pi * X) * np.cos(n * math.pi * Y)
        ax.contour(X, Y, Z, levels=[-0.9, -0.45, 0, 0.45, 0.9], colors=INK, linewidths=1.1,
                   linestyles="solid")
        ax.add_patch(Rectangle((-1, -1), 2, 2, fill=False, ec=INK, lw=1.5))
        ax.set_xlim(-1.03, 1.03); ax.set_ylim(-1.03, 1.03)
    return draw


def d_sine_weave():
    def draw(ax):
        x = np.linspace(-1, 1, 1200)
        for i in range(14):
            y0 = -1 + 2 * i / 13
            plot(ax, x, y0 + 0.10 * np.sin(6 * math.pi * x + i * math.pi / 2), lw=1.3)
        ax.add_patch(Rectangle((-1.02, -1.16), 2.04, 2.32, fill=False, ec=INK, lw=1.4))
        ax.set_xlim(-1.06, 1.06); ax.set_ylim(-1.2, 1.2)
    return draw


def d_whirl(n_sides, steps=28, twist=0.09):
    def draw(ax):
        pts = np.array([[math.cos(2 * math.pi * i / n_sides + math.pi / 2),
                         math.sin(2 * math.pi * i / n_sides + math.pi / 2)] for i in range(n_sides)])
        for _ in range(steps):
            closed = np.vstack([pts, pts[:1]])
            plot(ax, closed[:, 0], closed[:, 1], lw=1.1)
            pts = pts + twist * (np.roll(pts, -1, axis=0) - pts)
    return draw


def d_hexweb():
    def draw(ax):
        for ring in range(1, 7):
            s = ring / 6
            hexpts = [(s * math.cos(a + math.pi / 6), s * math.sin(a + math.pi / 6))
                      for a in [math.pi / 3 * i for i in range(6)]]
            ax.add_patch(Polygon(hexpts, closed=True, fill=False, ec=INK, lw=1.3))
        for a in [math.pi / 3 * i + math.pi / 6 for i in range(6)]:
            plot(ax, [0, math.cos(a)], [0, math.sin(a)], lw=1.2)
    return draw


def build_designs():
    designs = [
        ("Rose Curve, 8 Petals", "r = cos(4θ) — an even k doubles the petal count.", d_rose(4, 1)),
        ("Rose Curve, 5 Petals", "r = cos(5θ) — an odd k keeps exactly k petals.", d_rose(5, 1)),
        ("Rose Curve, 7 Petals", "r = cos(7θ) — polar graphs turn equations into flowers.", d_rose(7, 1)),
        ("Overlapping Rose", "r = cos(5θ/2) — a fractional k needs two turns to close.", d_rose(2.5, 2)),
        ("Lissajous 3:4", "x = sin 3t, y = sin 4t — two perpendicular vibrations.", d_lissajous(3, 4, math.pi / 2)),
        ("Lissajous 5:6", "Neighboring frequencies weave a tight braid.", d_lissajous(5, 6, math.pi / 2)),
        ("Lissajous 7:9", "The pattern closes because 7 and 9 share no factor.", d_lissajous(7, 9, math.pi / 2)),
        ("Spirograph 5:3", "A circle rolling inside a circle traces a hypotrochoid.", d_spiro(5, 3, 5)),
        ("Spirograph 7:4", "Change one gear tooth and the whole flower changes.", d_spiro(7, 4, 6)),
        ("Spirograph 11:7", "Coprime gears visit every position before closing.", d_spiro(11, 7, 9)),
        ("Epitrochoid 4:1", "Here the small circle rolls outside the big one.", d_spiro(4, 1, 2, epi=True)),
        ("Epitrochoid 6:1", "Six lobes: the ratio of the radii decides the count.", d_spiro(6, 1, 3, epi=True)),
        ("Phyllotaxis", "Sunflower seeds: each turns 137.5° — the golden angle.", d_phyllotaxis(500, True)),
        ("Phyllotaxis, Even Seeds", "The same spiral with equal seeds shows the lattice.", d_phyllotaxis(650, False)),
        ("Koch Snowflake", "Every edge sprouts a smaller copy of itself, forever.", d_koch(False)),
        ("Koch Anti-Snowflake", "The same rule bent inward eats the triangle instead.", d_koch(True)),
        ("Sierpinski Triangle", "Remove the middle triangle; repeat in each corner.", d_sierpinski()),
        ("Hilbert Curve", "One line that visits every cell of the square.", d_hilbert(5)),
        ("Dragon Curve", "Fold a paper strip 12 times — this is its crease pattern.", d_dragon(12)),
        ("Fractal Tree", "Each branch splits into two at the same angle.", d_tree(math.radians(24), 0.72)),
        ("Windswept Tree", "Unequal angles make the same rule grow sideways.", d_tree(math.radians(38), 0.68)),
        ("Truchet Tiles I", "One square tile, two orientations, endless corridors.", d_truchet(7)),
        ("Truchet Tiles II", "A different coin-flip sequence, a different maze.", d_truchet(23)),
        ("Eight-Point Star Grid", "The {8/3} star of Islamic geometric art, repeated.", d_star_grid(8, 3)),
        ("Twelve-Point Star Grid", "The {12/5} star — drawn with one unbroken line.", d_star_grid(12, 5)),
        ("Nested Heptagram", "{7/3}: connect every third corner of a heptagon.", d_star_nest(7, 3)),
        ("Nested Nonagram", "{9/4}: nine points, skip four, never lift the pen.", d_star_nest(9, 4)),
        ("Rhombille Tiling", "Three diamonds per hexagon — the tumbling-cubes illusion.", d_rhombille()),
        ("Circle Packing I", "Circles grown until they touch — nature's packing.", d_circlepack(11)),
        ("Circle Packing II", "A new random seed, a new arrangement of tangencies.", d_circlepack(42)),
        ("Apollonian Gasket", "Every gap between three circles holds another circle.", d_apollonian()),
        ("Torus Knot (2,3)", "The trefoil: the simplest knot that cannot be undone.", d_torus_knot(2, 3)),
        ("Torus Knot (3,5)", "Wind 3 times one way, 5 the other, around a donut.", d_torus_knot(3, 5)),
        ("Golden Spiral", "Fibonacci squares 1,1,2,3,5,8,13 — the spiral lives in their corners.", d_golden()),
        ("Moiré Circles", "Two identical ripple patterns, slightly offset, interfere.", d_moire(True)),
        ("Polar Grid", "Circles times rays: the graph paper of polar coordinates.", d_moire(False)),
        ("Superellipses", "|x|ⁿ + |y|ⁿ = 1 morphs a diamond into a square.", d_superellipse()),
        ("Harmonograph I", "A pendulum with a pen: damped sine waves in two axes.", d_harmonograph(3)),
        ("Harmonograph II", "Tiny detuning (3.001 vs 2) makes the orbit precess.", d_harmonograph(9)),
        ("Chladni Figure 3:5", "Where a vibrating plate stands still, sand gathers.", d_chladni(3, 5)),
        ("Chladni Figure 4:7", "Higher frequencies carve finer standing-wave cells.", d_chladni(4, 7)),
        ("Sine Weave", "Fourteen phase-shifted sine waves braid a fabric.", d_sine_weave()),
        ("Whirling Triangles", "Chase the next corner by 9% each step and spiral in.", d_whirl(3)),
        ("Whirling Squares", "The pursuit curve: four mice each chasing the next.", d_whirl(4)),
        ("Whirling Hexagons", "Six chasers trace a logarithmic spiral nest.", d_whirl(6)),
        ("Honeycomb Web", "Nested hexagons with spokes — bees build with least wax.", d_hexweb()),
    ]
    seed = 100
    while len(designs) < 50:
        idx = len(designs) - 45
        designs.append((f"Mandala No. {idx}",
                        "Rotational symmetry: one motif, repeated n times around.", d_mandala(seed)))
        seed += 7
    assert len(designs) == 50
    return designs


# ----------------------------------------------------------------- front matter
def text_page(pdf, lines):
    """lines: (y, text, size, weight, color) tuples in figure coords."""
    fig = blank_fig()
    for y, text, size, weight, color in lines:
        fig.text(0.5, y, text, ha="center", va="center", fontsize=size,
                 weight=weight, color=color, wrap=True)
    pdf.savefig(fig)
    plt.close(fig)


def title_page(pdf):
    fig = blank_fig()
    fig.text(0.5, 0.68, TITLE, ha="center", fontsize=30, weight="bold", color=INK)
    fig.text(0.5, 0.615, SUBTITLE, ha="center", fontsize=15, color=INK)
    fig.text(0.5, 0.565, TAGLINE, ha="center", fontsize=11, color="#666666")
    ax = fig.add_axes([0.3, 0.2, 0.4, 0.31])
    ax.set_aspect("equal"); ax.axis("off")
    d_spiro(7, 4, 6)(ax)
    fig.text(0.5, 0.12, AUTHOR, ha="center", fontsize=13, color=INK)
    pdf.savefig(fig); plt.close(fig)


def copyright_page(pdf):
    text_page(pdf, [
        (0.5, f"{TITLE} — {SUBTITLE}", 10, "bold", INK),
        (0.46, f"Copyright © {YEAR} {AUTHOR}. All rights reserved.", 9, "normal", "#444444"),
        (0.42, "No part of this book may be reproduced without permission,", 9, "normal", "#444444"),
        (0.395, "except for personal, non-commercial coloring enjoyment.", 9, "normal", "#444444"),
        (0.34, "Every pattern in this book is generated from the mathematical", 9, "normal", "#444444"),
        (0.315, "equations named on its page.", 9, "normal", "#444444"),
    ])


def howto_page(pdf):
    text_page(pdf, [
        (0.78, "How to Use This Book", 18, "bold", INK),
        (0.68, "Each design sits on a right-hand page with a blank back,", 11, "normal", INK),
        (0.655, "so markers will not bleed through onto the next pattern.", 11, "normal", INK),
        (0.60, "Below every design is the mathematical idea that drew it —", 11, "normal", INK),
        (0.575, "a one-line answer to “what am I coloring?”", 11, "normal", INK),
        (0.52, "Try the color-test page opposite before using new pens.", 11, "normal", INK),
        (0.44, "There is no wrong way to color mathematics.", 11, "normal", "#666666"),
    ])


def colortest_page(pdf):
    fig = blank_fig()
    fig.text(0.5, 0.88, "Color Test Page", ha="center", fontsize=16, weight="bold", color=INK)
    fig.text(0.5, 0.85, "Try your pens and markers here first.", ha="center", fontsize=10, color="#666666")
    ax = fig.add_axes([0.15, 0.15, 0.7, 0.62])
    ax.set_aspect("equal"); ax.axis("off")
    for i in range(5):
        for j in range(7):
            ax.add_patch(Rectangle((i * 1.1, j * 1.1), 1, 1, fill=False, ec=INK, lw=1.2))
    ax.set_xlim(-0.2, 5.7); ax.set_ylim(-0.2, 7.9)
    pdf.savefig(fig); plt.close(fig)


# ----------------------------------------------------------------------- cover
def make_cover(page_count):
    bleed = 0.125
    spine = page_count * 0.002252
    w = 2 * bleed + 2 * PAGE_W + spine
    h = 2 * bleed + PAGE_H
    fig = plt.figure(figsize=(w, h))
    fig.patch.set_facecolor("#f3f0e7")  # swiss paper

    def fx(x):  # inches -> figure fraction
        return x / w

    def fy(y):
        return y / h

    front_cx = fx(bleed + PAGE_W + spine + PAGE_W / 2)
    back_cx = fx(bleed + PAGE_W / 2)

    # front: red bar, title, pattern
    bar = Rectangle((fx(bleed + PAGE_W + spine + 0.75), fy(bleed + 9.55)),
                    fx(PAGE_W - 1.5), fy(0.07), transform=fig.transFigure,
                    facecolor="#d92b2b", edgecolor="none")
    fig.patches.append(bar)
    fig.text(front_cx, fy(bleed + 9.0), TITLE, ha="center", fontsize=34, weight="bold", color=INK)
    fig.text(front_cx, fy(bleed + 8.45), SUBTITLE, ha="center", fontsize=16, color=INK)
    fig.text(front_cx, fy(bleed + 8.0), TAGLINE, ha="center", fontsize=12, color="#6f6b61")
    ax = fig.add_axes([fx(bleed + PAGE_W + spine + 1.9), fy(bleed + 1.9), fx(PAGE_W - 3.8), fy(5.4)])
    ax.set_aspect("equal"); ax.axis("off")
    d_torus_knot(3, 5)(ax)
    fig.text(front_cx, fy(bleed + 1.1), AUTHOR, ha="center", fontsize=15, color=INK)

    # back: blurb high up, barcode corner left empty
    blurb = [
        "Fifty patterns, zero randomness about what they mean:",
        "every page is drawn from a real mathematical object —",
        "fractals, spirographs, standing waves, tilings, knots —",
        "and names its equation in one line.",
        "",
        "Bold lines, single-sided pages, a color-test page,",
        "and the quiet satisfaction of coloring",
        "something that is true.",
    ]
    for i, line in enumerate(blurb):
        fig.text(back_cx, fy(bleed + 9.4 - i * 0.34), line, ha="center", fontsize=11.5, color=INK)
    axb = fig.add_axes([fx(bleed + 2.45), fy(bleed + 2.6), fx(3.6), fy(3.6)])
    axb.set_aspect("equal"); axb.axis("off")
    d_rose(5, 1)(axb)
    # barcode keep-out: bottom-right 2x1.2 in of the back trim area, white
    kb = Rectangle((fx(bleed + PAGE_W - 2.25), fy(bleed + 0.25)), fx(2.0), fy(1.2),
                   transform=fig.transFigure, facecolor="white", edgecolor="none")
    fig.patches.append(kb)

    out = HERE / "cover.pdf"
    fig.savefig(out, format="pdf", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out, w, h, spine


def main():
    designs = build_designs()
    interior = HERE / "interior.pdf"
    with PdfPages(interior) as pdf:
        title_page(pdf)
        copyright_page(pdf)
        howto_page(pdf)
        colortest_page(pdf)
        for title, note, draw in designs:
            design_page(pdf, title, note, draw)
            blank_page(pdf)
    page_count = 4 + 2 * len(designs)
    assert 24 <= page_count <= 110, page_count
    cover, w, h, spine = make_cover(page_count)
    print(f"interior: {interior.name}, {page_count} pages, {PAGE_W}x{PAGE_H} in")
    print(f"cover:    {cover.name}, {w:.4f}x{h:.4f} in (spine {spine:.4f} in, bleed 0.125 in)")


if __name__ == "__main__":
    main()
