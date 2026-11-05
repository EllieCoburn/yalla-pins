# yalla-pins

Pinterest Pin pipeline for **Yalla | Play & Childhood** (pinterest.com/yallachildcare).
Public on purpose: Buffer downloads Pin images from `raw.githubusercontent.com`. Never commit photos of children or anything private.

Read **STANDARDS.md** before making any Pin.

## Layout

| Path | What it is |
| --- | --- |
| `STANDARDS.md` | Brand voice, keyword strategy, visual rules, compliance, board map, cadence |
| `catalog/lists.json` | Amazon Storefront lists with exact tagged URLs |
| `catalog/products.json` | Products with supplied cut-out images, listing ages, colors, themes |
| `assets/products/` | Product cut-outs (supplied by Ellie only, never Amazon photos) |
| `assets/originals/<product-id>.png` | Product images exactly as Ellie supplied them |
| `assets/lifestyle/<product-id>/` | Lifestyle photos of each product in use, listed in that product's `lifestyle` field. No identifiable children unless Ellie confirms permission |
| `assets/rooms/` | Room and environment photos not tied to one product (e.g. a whole infant room) |
| `assets/brand/`, `assets/fonts/` | Yalla wordmark, sun mark, Lora + DM Sans (SIL OFL) |
| `scripts/render_pin.py` | Renders a Pin spec (JSON) to a 1000×1500 PNG |
| `specs/` | Every Pin's spec, named `YYYY-MM-DD-<slug>.json` |
| `pins/` | Rendered Pin images (public URLs for Buffer) |
| `log/pins.jsonl` | One line per Pin: date, slug, layout, products, list, title, board, Buffer draft id |

## Making a Pin

```bash
python3 scripts/render_pin.py specs/2026-11-06-movement-gifts.json pins/2026-11/2026-11-06-movement-gifts.png
```

Layouts: `arches` (2, 3, 4 or 6 products), `hero` (1 product), `band-collage` (hand-placed products around a blue title band).
Backgrounds for arches/hero: `chalk`, `mist`, `blue`, `ink`.

Image URL for Buffer after pushing:
`https://raw.githubusercontent.com/EllieCoburn/yalla-pins/main/<path to png>`

## Buffer

- Organization `6aecd856030645f4bf9f3947`, Pinterest channel `6aecd9dfe29c69a17174b1df` (yallachildcare).
- Always `saveToDraft: true`. Ellie approves every Pin.
- Board `serviceId`s come from Buffer `get_channel` → `metadata.boards`. Gift Guides for Intentional Play = `914160493052943248`.
