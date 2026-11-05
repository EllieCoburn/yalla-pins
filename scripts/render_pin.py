#!/usr/bin/env python3
"""Render a Yalla Pin (1000x1500 PNG) from a JSON spec.

Usage:  python3 scripts/render_pin.py specs/my-pin.json pins/<folder>/<name>.png

Spec fields
  layout      "arches" | "hero" | "band-collage" | "photo"
  photo       photo layout: repo path of a lifestyle/room photo; photo_position, frame "full"|"arch"
  eyebrow     small caps line, e.g. "Holiday gift guide · 12–24 months"
  headline    plain part of the Lora headline, e.g. "Gifts that get them"
  headline_em italic final clause, e.g. "moving."
  background  "chalk" | "mist" | "blue" | "ink"   (arches/hero; default chalk)
  products    list of product ids from catalog/products.json
              (band-collage: list of {"id","x","y","w","h"} placements instead)
  labels      true/false — product names under arches (default true)
  band_title  band-collage only: {"eyebrow","big","big_em"}
"""
import html, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = dict(blue="#6065F2", ink="#292C45", chalk="#F7F5EF", paper="#FBFAF6", mist="#E7E5F1",
         inksoft="#5A5D74", lilac="#C8B9DC", deep="#4B4FD6")
BG = {"chalk": (C["chalk"], C["ink"], C["blue"], C["mist"], "blue"),
      "mist": (C["mist"], C["ink"], C["blue"], C["paper"], "blue"),
      "blue": (C["blue"], C["chalk"], C["chalk"], "#7479F5", "ink"),
      "ink": (C["ink"], C["chalk"], C["lilac"], "#3A3E5C", "blue")}
# (page bg, text, accent for italic, arch fill, band color)


def a(p):
    return (ROOT / p).as_uri()


def scallop(width, color, flip=False):
    n = width // 40
    d = "M0 24V12" + "a20 12 0 0 1 40 0" * n + f"V24Z"
    t = "transform: scaleY(-1);" if flip else ""
    return (f'<svg width="{width}" height="24" viewBox="0 0 {width} 24" style="display:block;margin-bottom:-2px;{t}">'
            f'<path fill="{color}" d="{d}"/></svg>')


def headline_html(spec, text, accent, size):
    h = html.escape(spec.get("headline", ""))
    em = html.escape(spec.get("headline_em", ""))
    eb = html.escape(spec.get("eyebrow", ""))
    eyebrow = (f'<p style="margin:0;font:500 20px/1.2 \'DM Sans\';letter-spacing:.22em;text-transform:uppercase;'
               f'color:{text};opacity:.8">{eb}</p>') if eb else ""
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;padding:0 70px">{eyebrow}'
            f'<h1 style="margin:0;font:400 {size}px/1.04 Lora;letter-spacing:-.015em;color:{text}">{h} '
            f'<em style="font-style:italic;color:{accent}">{em}</em></h1></div>')


def band(color, word):
    return (f'<div style="margin-top:auto;flex-shrink:0">{scallop(1000, color)}'
            f'<div style="background:{color};height:150px;display:flex;align-items:center;justify-content:center">'
            f'<img src="{a("assets/brand/" + word)}" style="height:58px"></div></div>')


def load_products():
    return {p["id"]: p for p in json.loads((ROOT / "catalog/products.json").read_text())}


def arches(spec, P):
    bg, text, accent, arch, bandc = BG[spec.get("background", "chalk")]
    ids = spec["products"]
    n = len(ids)
    assert n in (2, 3, 4, 6), "arches layout takes 2, 3, 4 or 6 products"
    cols = 2
    rows = 2 if n == 3 else (n + 1) // 2
    labels = spec.get("labels", False)
    radius = 210
    lab_size = 28 if n <= 4 else 26
    cells = []
    for i, pid in enumerate(ids):
        wide = (n == 3 and i == 0)
        p = P[pid]
        lab = (f'<p style="margin:0;font:400 {lab_size}px/1.2 Lora;color:{text};text-align:center">{html.escape(p["name"])}</p>'
               if labels else "")
        rad = "430px 430px 0 0 / 240px 240px 0 0" if wide else f"{radius}px {radius}px 0 0"
        padtop = 70 if wide else (60 if n >= 6 else 80)
        span = "grid-column:span 2;" if wide else ""
        cells.append(f'<div style="{span}display:flex;flex-direction:column;align-items:stretch;gap:10px;min-height:0">'
                     f'<div style="flex:1;min-height:0;border-radius:{rad};background:{arch};'
                     f'display:flex;align-items:flex-end;justify-content:center;box-sizing:border-box;padding:{padtop}px 18px 20px">'
                     f'<img src="{a(p["image"])}" style="max-width:100%;max-height:100%;min-height:0;object-fit:contain"></div>{lab}</div>')
    grid = (f'<div style="flex:1;min-height:0;padding:0 70px;margin:48px 0 44px;display:grid;'
            f'grid-template-columns:repeat({cols},minmax(0,1fr));grid-template-rows:repeat({rows},minmax(0,1fr));'
            f'column-gap:40px;row-gap:{24 if n >= 6 else 30}px">{"".join(cells)}</div>')
    return (f'<div style="width:1000px;height:1500px;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<div style="padding-top:80px">{headline_html(spec, text, accent, spec.get("headline_size", 84))}</div>'
            f'{grid}{band(C[bandc], "wordmark-chalk.png")}</div>')


def hero(spec, P):
    bg, text, accent, arch, bandc = BG[spec.get("background", "chalk")]
    p = P[spec["products"][0]]
    lab = (f'<p style="margin:16px 0 0;font:400 34px/1.2 Lora;color:{text};text-align:center">{html.escape(p["name"])}</p>'
           if spec.get("labels", False) else "")
    return (f'<div style="width:1000px;height:1500px;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<div style="padding-top:84px">{headline_html(spec, text, accent, spec.get("headline_size", 92))}</div>'
            f'<div style="padding:0 120px;margin-top:56px"><div style="height:820px;border-radius:380px 380px 0 0;background:{arch};'
            f'display:flex;align-items:flex-end;justify-content:center;box-sizing:border-box;padding:0 60px 60px">'
            f'<img src="{a(p["image"])}" style="max-width:100%;max-height:640px;object-fit:contain"></div>{lab}</div>'
            f'{band(C[bandc], "wordmark-chalk.png")}</div>')


def photo(spec, P):
    """Lifestyle photo layout. spec: photo (repo path), photo_position (CSS object-position), background, frame ("full"|"arch")."""
    bg, text, accent, arch, bandc = BG[spec.get("background", "chalk")]
    src = a(spec["photo"])
    pos = spec.get("photo_position", "50% 50%")
    if spec.get("frame", "full") == "arch":
        img = (f'<div style="flex:1;min-height:0;padding:0 100px;margin:52px 0 48px;display:flex">'
               f'<img src="{src}" style="flex:1;min-width:0;width:100%;height:100%;object-fit:cover;object-position:{pos};'
               f'border-radius:400px 400px 0 0"></div>')
        return (f'<div style="width:1000px;height:1500px;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
                f'<div style="padding-top:80px">{headline_html(spec, text, accent, spec.get("headline_size", 84))}</div>'
                f'{img}{band(C[bandc], "wordmark-chalk.png")}</div>')
    return (f'<div style="width:1000px;height:1500px;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<img src="{src}" style="width:1000px;height:{spec.get("photo_height", 930)}px;object-fit:cover;object-position:{pos};flex-shrink:0">'
            f'<div style="padding-top:56px">{headline_html(spec, text, accent, spec.get("headline_size", 80))}</div>'
            f'{band(C[bandc], "wordmark-chalk.png")}</div>')


def band_collage(spec, P):
    bt = spec["band_title"]
    top = spec.get("band_top", 612)
    n = 25
    d = ("M0 12" + "a20 12 0 0 1 40 0" * n + "V306" + "a20 12 0 0 1 -40 0" * n + "Z")
    imgs = "".join(
        f'<img src="{a(P[x["id"]]["image"])}" style="position:absolute;left:{x["x"]}px;top:{x["y"]}px;width:{x["w"]}px;'
        f'height:{x["h"]}px;object-fit:contain">' for x in spec["products"])
    return (f'<div style="width:1000px;height:1500px;position:relative;overflow:hidden;background:{C["chalk"]}">'
            f'<svg width="1000" height="318" viewBox="0 0 1000 318" style="position:absolute;left:0;top:{top}px">'
            f'<path fill="{C["blue"]}" d="{d}"/></svg>'
            f'<div style="position:absolute;left:0;top:{top + 24}px;width:1000px;height:270px;display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;gap:10px;text-align:center;color:{C["chalk"]}">'
            f'<img src="{a("assets/brand/sun-chalk.png")}" style="width:52px;height:52px">'
            f'<p style="margin:0;font:600 20px \'DM Sans\';letter-spacing:.22em;text-transform:uppercase">{html.escape(bt.get("eyebrow", ""))}</p>'
            f'<h1 style="margin:0;font:400 {bt.get("size", 112)}px/1 Lora;letter-spacing:-.015em">{html.escape(bt.get("big", ""))} '
            f'<em>{html.escape(bt.get("big_em", ""))}</em></h1></div>{imgs}'
            f'<img src="{a("assets/brand/wordmark-blue.png")}" style="position:absolute;left:430px;top:1380px;width:140px"></div>')


def render(spec_path, out_path):
    spec = json.loads(Path(spec_path).read_text())
    P = load_products()
    body = {"arches": arches, "hero": hero, "band-collage": band_collage, "photo": photo}[spec["layout"]](spec, P)
    fonts = (f"@font-face{{font-family:Lora;src:url({a('assets/fonts/Lora.ttf')});font-style:normal;font-weight:400 700}}"
             f"@font-face{{font-family:Lora;src:url({a('assets/fonts/Lora-Italic.ttf')});font-style:italic;font-weight:400 700}}"
             f"@font-face{{font-family:'DM Sans';src:url({a('assets/fonts/DMSans.ttf')});font-weight:100 1000}}")
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{fonts}body{{margin:0}}</style></head><body>{body}</body></html>'
    tmp = Path(out_path).with_suffix(".html")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(page)
    from playwright.sync_api import sync_playwright
    chrome = os.environ.get("CHROME", "/usr/bin/google-chrome")
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome if Path(chrome).exists() else None)
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        pg.goto(tmp.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(out_path))
        b.close()
    tmp.unlink()
    print(out_path)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
