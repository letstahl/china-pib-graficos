"""Gera os quatro gráficos a partir de data/raw e grava as séries derivadas em data/processed.

Uso: python src/make_figures.py
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC, FIG = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "figures"
PROC.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

INK, INK2, GRID = "#222222", "#6B6B6B", "#D6D6D6"
JADE, RED, GOLD, BLUE = "#2B8A68", "#E8938B", "#C9A03F", "#2F84B8"
JADE_T, RED_T, GOLD_T, BLUE_T = "#1F6B50", "#B65F57", "#8A6A18", "#1F5F88"
SANS = ["Inter", "DejaVu Sans"]

plt.rcParams.update({
    "font.family": SANS, "font.size": 8, "text.color": INK, "axes.edgecolor": GRID,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.major.size": 0, "ytick.major.size": 0,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.axisbelow": True, "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID,
    "grid.linewidth": 0.9, "grid.linestyle": (0, (1, 2.6)),
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "savefig.dpi": 300,
})
W = 6.3
DASH = (0, (4, 2.2))


def load_imf():
    out = {}
    with open(RAW / "imf_weo_2026oct.csv", newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault((r["indicator"], r["country"]), {})[int(r["year"])] = float(r["value"])
    return out


def load_maddison():
    out = {}
    with open(RAW / "maddison_gdppc.csv", newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["country"], {})[int(r["year"])] = float(r["gdppc_2011_intl_usd"])
    return out


def load_lowy():
    with open(RAW / "lowy_trade.csv", newline="") as f:
        rows = [(int(r["year"]), int(r["economies_trading_more_with_china"]),
                 int(r["economies_trading_twice_or_more_with_china"])) for r in csv.DictReader(f)]
    return rows


def write_csv(name, header, rows):
    with open(PROC / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def br(v, n=1):
    return f"{v:.{n}f}".replace(".", ",")


def frame(plot_h):
    top = 0.15
    H = top + plot_h + 0.38
    return plt.figure(figsize=(W, H)), H, top


def ax_in(fig, H, x0, y_top, w, h):
    return fig.add_axes([x0 / W, 1 - (y_top + h) / H, w / W, h / H])


def style_ticks(ax):
    ax.tick_params(axis="y", pad=2, labelsize=8)
    ax.tick_params(axis="x", pad=4, labelsize=8)


def save(fig, name):
    fig.savefig(FIG / f"{name}.png")
    plt.close(fig)


def fig1(imf):
    ys = list(range(2000, 2026))
    nom0 = imf[("NGDPD", "CHN")][2000]
    nom = [100 * imf[("NGDPD", "CHN")][y] / nom0 for y in ys]
    g = {y: imf[("NGDP_RPCH", "CHN")][y] for y in ys}
    real = [100.0]
    for y in ys[1:]:
        real.append(real[-1] * (1 + g[y] / 100))
    write_csv("fig1_china_gdp_index.csv",
              ["year", "nominal_usd_bn", "nominal_index_2000_100", "real_growth_pct", "real_index_2000_100"],
              [(y, imf[("NGDPD", "CHN")][y], round(n, 2), g[y], round(r, 2)) for y, n, r in zip(ys, nom, real)])

    top_h, gap, bot_h = 2.0, 0.32, 1.3
    fig, H, top = frame(top_h + gap + bot_h)
    L_, PW = 0.45, 4.35
    a1 = ax_in(fig, H, L_, top, PW, top_h)
    a2 = ax_in(fig, H, L_, top + top_h + gap, PW, bot_h)
    a1.fill_between(ys, real, nom, color=GOLD, alpha=0.22, lw=0)
    a1.plot(ys, nom, color=RED, lw=2.2, solid_capstyle="round")
    a1.plot(ys, real, color=JADE, lw=2.2, solid_capstyle="round")
    a1.plot([2025], [nom[-1]], "o", ms=4.5, color=RED)
    a1.plot([2025], [real[-1]], "o", ms=4.5, color=JADE)
    a1.set_xlim(1999.7, 2025.4)
    a1.set_ylim(0, 1750)
    a1.set_yticks([0, 500, 1000, 1500])
    a1.set_xticks([])
    style_ticks(a1)
    a1.text(2026, nom[-1], f"PIB nominal\n×{br(nom[-1] / 100)}", color=RED_T, va="center",
            fontsize=8.2, fontweight="semibold", linespacing=1.25)
    a1.text(2026, real[-1], f"PIB real\n×{br(real[-1] / 100)}", color=JADE_T, va="center",
            fontsize=8.2, fontweight="semibold", linespacing=1.25)
    a1.annotate("inflação + variação\ncambial do yuan", xy=(2014.8, 675), xytext=(2007.5, 1060),
                ha="center", va="center", fontsize=7.8, color=GOLD_T, style="italic", linespacing=1.25,
                arrowprops=dict(arrowstyle="-|>", color=GOLD_T, lw=0.9, shrinkA=14, shrinkB=0, mutation_scale=8))
    a2.bar(ys, [g[y] for y in ys], color=JADE, width=0.7, alpha=0.7, lw=0)
    a2.set_xlim(1999.7, 2025.4)
    a2.set_ylim(0, 20)
    a2.set_yticks([0, 5, 10, 15])
    a2.set_yticklabels([f"{t}%" for t in (0, 5, 10, 15)])
    a2.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
    style_ticks(a2)
    means = []
    for x0, x1 in ((2001, 2010), (2011, 2019), (2020, 2025)):
        seg = [g[y] for y in range(x0, x1 + 1)]
        m = sum(seg) / len(seg)
        means.append((x0, x1, m))
        a2.plot([x0 - 0.4, x1 + 0.4], [m, m], color=INK, lw=1.2)
        a2.text((x0 + x1) / 2, 17.6, f"média {br(m)}% a.a.", ha="center", va="center",
                fontsize=8, fontweight="semibold", color=INK)
    a2.text(2026, 8, "crescimento\nreal anual", fontsize=7.8, color=INK2, va="center", linespacing=1.25)
    save(fig, "grafico1_pib_nominal_e_real")
    return {"nominal_x": nom[-1] / 100, "real_x": real[-1] / 100, "means": means}


def fig2(imf):
    ys = list(range(1990, 2026))

    def ratio(ind, num="CHN", den="USA"):
        return [100 * imf[(ind, num)][y] / imf[(ind, den)][y] for y in ys]

    ser = {"tot_ppc": ratio("PPPSH"), "tot_usd": ratio("NGDPD"), "pc_ppc": ratio("PPPPC"), "pc_usd": ratio("NGDPDPC")}
    write_csv("fig2_china_vs_usa.csv", ["year", *[f"{k}_pct_of_usa" for k in ser]],
              [(y, *[round(ser[k][i], 2) for k in ser]) for i, y in enumerate(ys)])
    sty = {"tot_ppc": (JADE, "-", JADE_T, "PIB total\nem PPC"), "tot_usd": (JADE, DASH, JADE_T, "PIB total\nem US$"),
           "pc_ppc": (RED, "-", RED_T, "per capita\nem PPC"), "pc_usd": (RED, DASH, RED_T, "per capita\nem US$")}
    ph = 3.1
    fig, H, top = frame(ph)
    ax = ax_in(fig, H, 0.45, top, 4.35, ph)
    ax.axhline(100, color=INK, lw=0.9, zorder=1)
    ax.text(1990.2, 103, "EUA = 100%", fontsize=7.6, color=INK2, va="bottom")
    for k, v in ser.items():
        c, ls, ct, lab = sty[k]
        ax.plot(ys, v, color=c, lw=2.2, ls=ls, solid_capstyle="round", dash_capstyle="round", zorder=3)
        ax.plot([2025], [v[-1]], "o", ms=4.5, color=c, zorder=4)
        ax.text(2026, v[-1], f"{lab}  {br(v[-1], 0)}%", color=ct, fontsize=8.2, fontweight="semibold",
                va="center", linespacing=1.15)
    ax.set_xlim(1990, 2025.4)
    ax.set_ylim(0, 150)
    ticks = [0, 25, 50, 75, 100, 125, 150]
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{t}%" for t in ticks])
    ax.set_xticks([1990, 2000, 2010, 2020, 2025])
    style_ticks(ax)
    i16, i21 = ys.index(2016), ys.index(2021)
    ap = dict(arrowstyle="-", color=INK2, lw=0.7)
    ax.annotate("2016: a China passa\nos EUA em PPC", (2016, ser["tot_ppc"][i16]), xytext=(2003.5, 124),
                fontsize=7.8, color=INK, va="center", arrowprops=ap)
    ax.annotate(f"2021: pico em US$\n({br(ser['tot_usd'][i21], 0)}% dos EUA)", (2021, ser["tot_usd"][i21]),
                xytext=(2013.2, 43), fontsize=7.8, color=INK, va="center", arrowprops=ap)
    save(fig, "grafico2_quatro_medidas")
    return {k: v[-1] for k, v in ser.items()}


def fig3(mad):
    cfg = [("JPN", "Japão", GOLD, GOLD_T, 1.8), ("KOR", "Coreia do Sul", RED, RED_T, 1.8),
           ("TWN", "Taiwan", BLUE, BLUE_T, 1.8), ("CHN", "China", JADE, JADE_T, 2.8)]
    ph = 3.0
    fig, H, top = frame(ph)
    ax = ax_in(fig, H, 0.45, top, 4.25, ph)
    rows, start = [], {}
    for k, lab, c, ct, lw in cfg:
        d = mad[k]
        r = {y: d[y] / mad["USA"][y] * 100 for y in d if y in mad["USA"]}
        y0 = min(y for y in sorted(r) if r[y] >= 20)
        start[k] = y0
        xs = [y - y0 for y in sorted(r) if y0 <= y <= y0 + 30]
        vs = [r[y0 + x] for x in xs]
        rows += [(k, y0 + x, x, round(v, 2)) for x, v in zip(xs, vs)]
        ax.plot(xs, vs, color=c, lw=lw, solid_capstyle="round", zorder=4 if k == "CHN" else 3)
        ax.plot([xs[-1]], [vs[-1]], "o", ms=4.5, color=c, zorder=5)
        yl = {"KOR": vs[-1] + 2.5, "CHN": vs[-1] - 5.5, "TWN": vs[-1] - 2.5}.get(k, vs[-1])
        ax.text(xs[-1] + 0.6, yl, f"{lab}  {br(vs[-1], 0)}%", color=ct, fontsize=8.2, fontweight="semibold", va="center")
    write_csv("fig3_catchup_from_20pct.csv", ["country", "year", "years_since_20pct", "pct_of_usa_gdppc"], rows)
    ax.axhline(20, color=INK2, lw=0.7, ls=(0, (1, 2)), zorder=1)
    ax.set_xlim(0, 30.4)
    ax.set_ylim(10, 80)
    ax.set_yticks([20, 40, 60, 80])
    ax.set_yticklabels([f"{t}%" for t in (20, 40, 60, 80)])
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    style_ticks(ax)
    ax.set_xlabel("anos desde que atingiu 20% da renda per capita dos EUA", fontsize=8, color=INK2, labelpad=4)
    save(fig, "grafico3_vizinhos_asiaticos")
    return start


def fig4(lowy):
    ph = 2.9
    fig, H, top = frame(ph)
    ax = ax_in(fig, H, 0.45, top, 4.1, ph)
    rows = [r for r in lowy if r[0] >= 2001]
    yrs, m, t2 = [r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]
    ax.plot(yrs, m, color=JADE, lw=2.4, solid_capstyle="round", zorder=3)
    ax.plot(yrs, t2, color=JADE, lw=2.4, ls=DASH, solid_capstyle="round", zorder=3)
    for v in (m, t2):
        ax.plot([2023], [v[-1]], "o", ms=4.5, color=JADE, zorder=4)
    ax.text(2023.5, m[-1] + 4, f"mais com a China\n{m[-1]} economias", color=JADE_T, fontsize=8.2,
            fontweight="semibold", va="center", linespacing=1.15)
    ax.text(2023.5, t2[-1] - 8, f"o dobro ou mais\n{t2[-1]} economias", color=JADE_T, fontsize=8.2,
            fontweight="semibold", va="center", linespacing=1.15)
    ax.annotate("2001: a China entra\nna OMC", (2001, m[0]), xytext=(2003.2, 112), fontsize=7.8, color=INK,
                va="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
    ax.set_xlim(2001, 2023.4)
    ax.set_ylim(0, 170)
    ax.set_yticks([0, 50, 100, 150])
    ax.set_xticks([2001, 2005, 2010, 2015, 2020, 2023])
    style_ticks(ax)
    save(fig, "grafico4_parceiros_comerciais")
    return m[-1], t2[-1]


def main():
    imf, mad, lowy = load_imf(), load_maddison(), load_lowy()
    r1, r2, r3, r4 = fig1(imf), fig2(imf), fig3(mad), fig4(lowy)
    print(f"G1  PIB nominal x{r1['nominal_x']:.1f} | PIB real x{r1['real_x']:.1f} | "
          + " | ".join(f"{a}-{b}: {m:.1f}%" for a, b, m in r1["means"]))
    print("G2  2025, % dos EUA: " + " | ".join(f"{k} {v:.1f}" for k, v in r2.items()))
    print("G3  ano em que cada país atinge 20%: " + " | ".join(f"{k} {v}" for k, v in r3.items()))
    print(f"G4  2023: {r4[0]} economias comerciam mais com a China; {r4[1]} com o dobro ou mais")


if __name__ == "__main__":
    main()
