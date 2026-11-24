from pathlib import Path

from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"

FRAMES = [
    ("grafico1_pib_nominal_e_real.png",
     "Gráfico 1 – PIB da China em dólares correntes e em termos reais e crescimento real anual, 2000–2025",
     "Fonte: Elaborado pela autora com base em IMF (2026)."),
    ("grafico2_quatro_medidas.png",
     "Gráfico 2 – PIB total e PIB per capita da China em relação aos Estados Unidos, em dólares correntes e em PPC, 1990–2025",
     "Fonte: Elaborado pela autora com base em IMF (2026)."),
    ("grafico3_vizinhos_asiaticos.png",
     "Gráfico 3 – PIB per capita em PPC de China, Japão, Coreia do Sul e Taiwan em relação aos Estados Unidos, "
     "a partir do ano em que cada país atingiu 20% da renda per capita norte-americana",
     "Fonte: Elaborado pela autora com base em Bolt e van Zanden (2024)."),
    ("grafico4_parceiros_comerciais.png",
     "Gráfico 4 – Número de economias que comerciam mais com a China do que com os Estados Unidos, 2001–2023",
     "Fonte: Elaborado pela autora com base em Lowy Institute (2025), a partir de dados do FMI."),
]

W, PAD, IMG_W = 1000, 28, 944
SECONDS = 4.5
BG, INK, MUTED, DOT = (255, 255, 255), (28, 28, 30), (110, 110, 115), (205, 205, 210)


def font(size, weight):
    path = fm.findfont(fm.FontProperties(family="Inter", weight=weight))
    return ImageFont.truetype(path, size)


def wrap(text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if f.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def main():
    f_t, f_s = font(19, 600), font(15, 400)
    imgs = []
    for name, *_ in FRAMES:
        im = Image.open(FIG / name).convert("RGB")
        imgs.append(im.resize((IMG_W, round(im.height * IMG_W / im.width)), Image.LANCZOS))

    lead_t, lead_s = 27, 21
    n_t = max(len(wrap(t, f_t, W - 2 * PAD)) for _, t, _ in FRAMES)
    n_s = max(len(wrap(s, f_s, W - 2 * PAD)) for _, _, s in FRAMES)
    title_h, src_h, dots_h = n_t * lead_t, n_s * lead_s, 34
    img_h = max(i.height for i in imgs)
    H = PAD + title_h + 14 + img_h + 12 + src_h + dots_h + 10

    out = []
    for k, ((_, title, source), im) in enumerate(zip(FRAMES, imgs)):
        c = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(c)
        y = PAD
        for ln in wrap(title, f_t, W - 2 * PAD):
            d.text((PAD, y), ln, font=f_t, fill=INK)
            y += lead_t
        y = PAD + title_h + 14
        c.paste(im, ((W - IMG_W) // 2, y + (img_h - im.height) // 2))
        y += img_h + 12
        for ln in wrap(source, f_s, W - 2 * PAD):
            d.text((PAD, y), ln, font=f_s, fill=MUTED)
            y += lead_s
        cx, cy = W // 2 - 3 * 10, H - 22
        for j in range(len(FRAMES)):
            r = 5 if j == k else 3
            d.ellipse((cx + j * 20 - r, cy - r, cx + j * 20 + r, cy + r), fill=INK if j == k else DOT)
        out.append(c.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))

    out[0].save(FIG / "carrossel.gif", save_all=True, append_images=out[1:],
                duration=int(SECONDS * 1000), loop=0, optimize=True, disposal=1)
    print(f"figures/carrossel.gif  {W}x{H}  {(FIG / 'carrossel.gif').stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
