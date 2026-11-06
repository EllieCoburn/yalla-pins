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
            f'<em style="display:block;font-style:italic;color:{accent}">{em}</em></h1></div>')


def foot(h=72):
    return f'<div style="height:{h}px;flex-shrink:0"></div>'


def mark(spec, dark):
    """Tiny, quiet brand mark in a corner. spec["mark"]: "small" (default) | "none"; spec["mark_corner"]: "br" | "bl"."""
    if spec.get("mark", "small") == "none":
        return ""
    word = "wordmark-chalk.png" if dark else "wordmark-blue.png"
    side = "left" if spec.get("mark_corner", "br") == "bl" else "right"
    return (f'<img src="{a("assets/brand/" + word)}" style="position:absolute;{side}:44px;bottom:36px;width:64px;'
            f'opacity:{0.7 if dark else 0.55}">')


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
    grid = (f'<div style="flex:1;min-height:0;padding:0 70px;margin:56px 0 44px;display:grid;'
            f'grid-template-columns:repeat({cols},minmax(0,1fr));grid-template-rows:repeat({rows},minmax(0,1fr));'
            f'column-gap:40px;row-gap:{24 if n >= 6 else 30}px">{"".join(cells)}</div>')
    return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<div style="padding-top:90px">{headline_html(spec, text, accent, spec.get("headline_size", 84))}</div>'
            f'{grid}{foot(40)}{mark(spec, text == C["chalk"])}</div>')


def hero(spec, P):
    bg, text, accent, arch, bandc = BG[spec.get("background", "chalk")]
    p = P[spec["products"][0]]
    lab = (f'<p style="margin:16px 0 0;font:400 34px/1.2 Lora;color:{text};text-align:center">{html.escape(p["name"])}</p>'
           if spec.get("labels", False) else "")
    return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<div style="padding-top:96px">{headline_html(spec, text, accent, spec.get("headline_size", 92))}</div>'
            f'<div style="flex:1;min-height:0;display:flex;flex-direction:column;padding:0 110px;margin:64px 0 110px">'
            f'<div style="flex:1;min-height:0;border-radius:400px 400px 0 0;background:{arch};'
            f'display:flex;align-items:flex-end;justify-content:center;box-sizing:border-box;padding:160px 60px 70px">'
            f'<img src="{a(p["image"])}" style="max-width:100%;max-height:100%;object-fit:contain"></div>{lab}</div>'
            f'{mark(spec, text == C["chalk"])}</div>')


def photo(spec, P):
    """Lifestyle/room photo. spec: photo (repo path), photo_position (CSS object-position),
    frame: "full" (photo on top, headline below) | "arch" (headline above, photo in a tall arch) |
           "bleed" (photo fills the Pin, headline on a scalloped Chalk panel at the bottom)."""
    bg, text, accent, arch, _ = BG[spec.get("background", "chalk")]
    src = a(spec["photo"])
    pos = spec.get("photo_position", "50% 50%")
    frame = spec.get("frame", "full")
    dark = text == C["chalk"]
    if frame == "arch":
        return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
                f'<div style="padding-top:90px">{headline_html(spec, text, accent, spec.get("headline_size", 84))}</div>'
                f'<div style="flex:1;min-height:0;padding:0 90px;margin:60px 0 110px;display:flex">'
                f'<img src="{src}" style="flex:1;min-width:0;width:100%;height:100%;object-fit:cover;object-position:{pos};'
                f'border-radius:410px 410px 0 0"></div>{mark(spec, dark)}</div>')
    if frame == "bleed":
        ph = spec.get("panel_height", 360)
        n = 25
        d = "M0 12" + "a20 12 0 0 1 40 0" * n + f"V{ph + 12}H0Z"
        return (f'<div style="width:1000px;height:1500px;position:relative;overflow:hidden;background:{bg}">'
                f'<img src="{src}" style="position:absolute;inset:0;width:1000px;height:1500px;object-fit:cover;object-position:{pos}">'
                f'<svg width="1000" height="{ph + 12}" viewBox="0 0 1000 {ph + 12}" style="position:absolute;left:0;bottom:0">'
                f'<path fill="{bg}" d="{d}"/></svg>'
                f'<div style="position:absolute;left:0;right:0;bottom:0;height:{ph}px;display:flex;align-items:center;justify-content:center;padding-bottom:20px;box-sizing:border-box">'
                f'{headline_html(spec, text, accent, spec.get("headline_size", 76))}</div>{mark(spec, dark)}</div>')
    return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<img src="{src}" style="width:1000px;height:{spec.get("photo_height", 1020)}px;object-fit:cover;object-position:{pos};flex-shrink:0">'
            f'<div style="flex:1;display:flex;align-items:center;justify-content:center;padding-bottom:30px">'
            f'{headline_html(spec, text, accent, spec.get("headline_size", 80))}</div>{mark(spec, dark)}</div>')


def story(spec, P):
    """Lifestyle photo on top, headline, then a row of small arches with the products that make it possible.
    spec: photo, photo_position, photo_height, products (2-4), background."""
    bg, text, accent, arch, _ = BG[spec.get("background", "chalk")]
    ids = spec["products"]
    n = len(ids)
    cells = "".join(
        f'<div style="flex:1;min-width:0;height:100%;border-radius:200px 200px 0 0;background:{arch};display:flex;align-items:flex-end;'
        f'justify-content:center;box-sizing:border-box;padding:{80 if n <= 3 else 64}px 14px 16px">'
        f'<img src="{a(P[i]["image"])}" style="max-width:100%;max-height:100%;object-fit:contain"></div>' for i in ids)
    return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'<img src="{a(spec["photo"])}" style="width:1000px;height:{spec.get("photo_height", 720)}px;object-fit:cover;'
            f'object-position:{spec.get("photo_position", "50% 50%")};flex-shrink:0">'
            f'<div style="padding-top:52px">{headline_html(spec, text, accent, spec.get("headline_size", 76))}</div>'
            f'<div style="flex:1;min-height:0;display:flex;gap:{28 if n <= 3 else 22}px;padding:0 60px;margin:44px 0 96px">{cells}</div>'
            f'{mark(spec, text == C["chalk"])}</div>')


def float_layout(spec, P):
    """Free composition: products float on the page with soft shadows, optionally around a lifestyle photo.
    spec:
      background  chalk | mist | blue | ink
      head        {"x","y","w","align": "left"|"center", "size"}  headline block position (uses eyebrow/headline/headline_em)
      photo       optional {"src","x","y","w","h","radius" (CSS border-radius), "position"}
      items       [{"id","x","y","w","z"(optional),"rot"(optional deg)}]  height follows the cut-out's proportions
      shadow      true (default) — soft grounded drop shadow under each product
    """
    bg, text, accent, _, _ = BG[spec.get("background", "chalk")]
    hd = spec.get("head", {"x": 70, "y": 90, "w": 860, "align": "center"})
    align = hd.get("align", "center")
    eb = html.escape(spec.get("eyebrow", ""))
    h = html.escape(spec.get("headline", ""))
    em = html.escape(spec.get("headline_em", ""))
    head = (f'<div style="position:absolute;left:{hd["x"]}px;top:{hd["y"]}px;width:{hd["w"]}px;text-align:{align};z-index:20">'
            + (f'<p style="margin:0 0 14px;font:500 20px/1.2 \'DM Sans\';letter-spacing:.22em;text-transform:uppercase;color:{text};opacity:.8">{eb}</p>' if eb else "")
            + f'<h1 style="margin:0;font:400 {hd.get("size", 84)}px/1.04 Lora;letter-spacing:-.015em;color:{text}">{h} '
              f'<em style="display:block;font-style:italic;color:{accent}">{em}</em></h1></div>')
    ph = ""
    if spec.get("photo"):
        q = spec["photo"]
        ph = (f'<img src="{a(q["src"])}" style="position:absolute;left:{q["x"]}px;top:{q["y"]}px;width:{q["w"]}px;height:{q["h"]}px;'
              f'object-fit:cover;object-position:{q.get("position", "50% 50%")};border-radius:{q.get("radius", "0")};z-index:1">')
    sh = "filter:drop-shadow(0 22px 26px rgba(41,44,69,.16)) drop-shadow(0 4px 6px rgba(41,44,69,.10));" if spec.get("shadow", True) else ""
    items = "".join(
        f'<img src="{a(P[it["id"]]["image"])}" style="position:absolute;left:{it["x"]}px;top:{it["y"]}px;width:{it["w"]}px;height:auto;'
        f'z-index:{it.get("z", 10)};transform:rotate({it.get("rot", 0)}deg);{sh}">' for it in spec["items"])
    return (f'<div style="width:1000px;height:1500px;position:relative;overflow:hidden;background:{bg}">'
            f'{ph}{head}{items}{mark(spec, text == C["chalk"])}</div>')


def checklist(spec, P):
    """Image on top (photo or floating cut-outs), headline, then a short list of what the space needs.
    spec: background; top_height (default 640);
      photo {"src","position","frame": "full"|"arch"} OR items [{"id","x","y","w","rot"}] placed inside the top area;
      list ["...", ...]  (simple list)  OR  sections [{"name": "...", "items": "comma line"}] (overview)."""
    bg, text, accent, arch, _ = BG[spec.get("background", "chalk")]
    th = spec.get("top_height", 640)
    top = ""
    if spec.get("photo"):
        q = spec["photo"]
        if q.get("frame", "full") == "arch":
            top = (f'<div style="height:{th}px;flex-shrink:0;padding:70px 150px 0;box-sizing:border-box;display:flex">'
                   f'<img src="{a(q["src"])}" style="flex:1;min-width:0;height:100%;object-fit:cover;object-position:{q.get("position","50% 50%")};'
                   f'border-radius:350px 350px 0 0"></div>')
        else:
            top = (f'<img src="{a(q["src"])}" style="width:1000px;height:{th}px;object-fit:cover;object-position:{q.get("position","50% 50%")};flex-shrink:0">')
    elif spec.get("items"):
        sh = "filter:drop-shadow(0 22px 26px rgba(41,44,69,.16)) drop-shadow(0 4px 6px rgba(41,44,69,.10));"
        imgs = "".join(f'<img src="{a(P[i["id"]]["image"])}" style="position:absolute;left:{i["x"]}px;top:{i["y"]}px;width:{i["w"]}px;'
                       f'transform:rotate({i.get("rot",0)}deg);{sh}">' for i in spec["items"])
        top = f'<div style="position:relative;height:{th}px;flex-shrink:0">{imgs}</div>'
    rule = "rgba(247,245,239,.35)" if text == C["chalk"] else "#D6CFC3"
    if spec.get("sections"):
        rows = "".join(
            f'<div style="display:grid;grid-template-columns:210px minmax(0,1fr);column-gap:24px;padding:21px 0;border-top:1px solid {rule}">'
            f'<p style="margin:0;font:400 italic 32px/1.2 Lora;color:{accent}">{html.escape(sec["name"])}</p>'
            f'<p style="margin:0;font:400 26px/1.4 \'DM Sans\';color:{text}">{html.escape(sec["items"])}</p></div>' for sec in spec["sections"])
    else:
        rows = "".join(
            f'<div style="display:flex;gap:18px;align-items:baseline;padding:20px 0;border-top:1px solid {rule}">'
            f'<span style="flex-shrink:0;width:10px;height:10px;border-radius:50%;background:{accent};transform:translateY(-4px)"></span>'
            f'<p style="margin:0;font:400 31px/1.35 \'DM Sans\';color:{text}">{html.escape(t)}</p></div>' for t in spec["list"])
    return (f'<div style="width:1000px;height:1500px;position:relative;background:{bg};display:flex;flex-direction:column;overflow:hidden">'
            f'{top}<div style="padding-top:{spec.get("head_pad", 50)}px">{headline_html(spec, text, accent, spec.get("headline_size", 72))}</div>'
            f'<div style="padding:0 84px;margin-top:40px;display:flex;flex-direction:column"><div style="border-bottom:1px solid {rule}">{rows}</div></div>'
            f'{mark(spec, text == C["chalk"])}</div>')


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
            f'<em>{html.escape(bt.get("big_em", ""))}</em></h1></div>{imgs}{mark(spec, False)}</div>')


def render(spec_path, out_path):
    spec = json.loads(Path(spec_path).read_text())
    P = load_products()
    body = {"arches": arches, "hero": hero, "band-collage": band_collage, "photo": photo, "story": story, "float": float_layout, "checklist": checklist}[spec["layout"]](spec, P)
    fonts = (f"@font-face{{font-family:Lora;src:url({a('assets/fonts/Lora.ttf')});font-style:normal;font-weight:400 700}}"
             f"@font-face{{font-family:Lora;src:url({a('assets/fonts/Lora-Italic.ttf')});font-style:italic;font-weight:400 700}}"
             f"@font-face{{font-family:'DM Sans';src:url({a('assets/fonts/DMSans.ttf')});font-weight:100 1000}}")
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{fonts}body{{margin:0}}</style></head><body>{body}</body></html>'
    out_path = Path(out_path).resolve()
    tmp = out_path.with_suffix(".html")
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
