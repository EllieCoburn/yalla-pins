# Yalla Pinterest — Pin Standards

The rulebook for every Pin made for **Yalla | Play & Childhood** (pinterest.com/yallachildcare).
Every Pin, every run, follows this document. When in doubt, follow this file over habit.

## 1. The goal of every Pin

1. **Be found and saved on Pinterest.** Pinterest is a visual search engine. A Pin spreads when its image stops the scroll and its words match what people are searching for at that moment.
2. **Drive clicks to Ellie's Amazon affiliate lists and products.** Every Pin links to a real, tagged Amazon Storefront list or product.

Honesty note: no copy guarantees virality. We maximise the odds: search-matched keywords, strong seasonal timing, scroll-stopping images, fresh Pin designs.

## 2. Workflow (non-negotiable)

- Claude builds Pins and saves them to **Buffer as drafts only**. Never `shareNow`, never queue, never schedule.
- Ellie reviews, tweaks and approves each draft in Buffer.
- Every Pin made is logged in `log/pins.jsonl`.

## 3. Brand voice (all public text)

Yalla's voice: **warm, unhurried, specific, inclusive, honest.** Written by early childhood educators who are also moms, for parents, caregivers, grandparents and educators.

Intentional language — use these, avoid the classic terms:

| Use | Avoid |
| --- | --- |
| child, little ones, toddlers | student |
| child-led play / exploration | free play |
| invitation, provocation, experience | activity, lesson |
| open-ended | "educational toy" hype |
| learning environment, play space | classroom (except as a search keyword in descriptions for educators) |
| grown-ups, caregivers, families | assuming one family shape |

Rules:
- Explain why an item is useful, from its documented features. Never invent personal experience, testimonials, results, safety certifications or developmental promises ("boosts IQ", "prevents delays" — never).
- Use "chosen by / selected by Yalla's early childhood educators" — never "tested by" unless Ellie confirms.
- No guilt, no pressure, no "must-have" shaming. Warm confidence instead.
- No emoji. No ALL CAPS shouting.
- Program names from the brand guide are not used on Pinterest Pins unless Ellie asks.

## 4. Keywords & metadata (maximise discovery)

For every Pin, before writing, identify:
- **Who is searching** (gift-giving grandparent, first-time parent, Montessori-curious mom, toddler teacher, family childcare provider).
- **What they type** (e.g. "gifts for 1 year old", "toddler christmas gifts", "first birthday gift ideas", "montessori toys for toddlers", "gross motor toys for toddlers", "non-plastic toddler gifts", "stocking stuffers for toddlers").
- **The season or moment** (holiday gifting Oct–Dec; first birthdays year-round; new year playroom reset in January; spring outdoor play; back-to-school for educators).

Then:
- **Title (≤100 chars):** lead with the exact high-intent search phrase, then Yalla's angle. Example: `Gift Ideas for 1 Year Olds: Open-Ended Toddler Gifts They'll Grow Into (12–24 Months)`.
- **Description (≤500 chars, aim 400–480):** first sentence restates the main keyword naturally. Name the actual products (brand names are searched: Nugget, Stapelstein, Pikler, Cozy Coupe, bilibo). Weave in 3–5 related search phrases as natural sentences, never a keyword dump. End with the disclosure.
- **Alt text:** describe the image accurately and name every product shown. Keyword-rich but true.
- **Board:** the most specific matching board (see §8). Board names are keywords.
- **Hashtags:** none. They no longer help on Pinterest and Buffer has no Pinterest tag field.
- **Seasonal lead time:** publish seasonal Pins 30–60 days before the moment.

## 5. Affiliate & compliance

- Destination URLs must be exact links from `catalog/lists.json` / `catalog/products.json`, which carry Ellie's tags (`nataliemart0f-20` or `onamznat09b6b-20`). Never invent, alter or strip tags.
- Every affiliate Pin description ends with: `As an Amazon Associate, Yalla earns from qualifying purchases.`
- Never show prices or "deals" on Pins or in copy (Amazon policy).
- Never use Amazon-hosted product photos. Only product images Ellie supplied (in `assets/products/`).
- Age labels must match the product listing. If a product's listing age doesn't fit the Pin's age range, leave it out of that Pin (note in log).
- Never photos of children unless Ellie supplies them and confirms permission; never commit children's photos to this public repo.

## 6. Visual system

Brand colors: Yalla Blue `#6065F2`, Ink `#292C45`, Chalk `#F7F5EF`, Paper `#FBFAF6`, Mist `#E7E5F1`, Ink Soft `#5A5D74`, Lilac `#C8B9DC`.
Fonts: **Lora** (headlines; final clause in *italic*), **DM Sans** (eyebrows/small caps).
Brand marks: real wordmark file only (never retyped), dotted sun as a general mark. Scalloped edges top Blue/Ink bands.

Layouts (render with `scripts/render_pin.py`):
- **band-collage** — products floating on Chalk around a full-width scalloped Yalla Blue title band. Big guides (8–14 products).
- **arches** — 2/4/6 products in Mist arches, Lora headline, Blue scallop band with wordmark. Themed sets.
- **hero** — one product large in an arch, headline above. Single-product Pins.

Rules Ellie set:
- **Image-centric.** Products are the hero; text is a short title only.
- **No small notes** on graphics (no tips, no "affiliate links" tags, no captions beyond product names in arches).
- **Don't place similar-colored products side by side** (e.g. red/yellow dump truck next to the red/yellow Cozy Coupe).
- 1000 × 1500 px, 2:3.
- Every new Pin must be a **fresh design** — vary layout, product subset, headline and background (Chalk / Mist / Blue / Ink) so Pinterest treats it as new content.
- Always look at the rendered PNG before uploading: no overlaps, no clipping, nothing touching the band or wordmark.

## 7. Cadence

- Target: **7 Pins per day**, every day.
- Mix: aim for no more than 3 Pins to the same destination URL per day; rotate boards; mix layouts. While the catalog has only one or two lists, more Pins may share a URL, but each must be a clearly different design, product subset and search angle (never near-duplicates).
- Products with `"hold": true` in `catalog/products.json` are not used in new Pins until Ellie confirms the image matches the listing.
- Products whose `listing_age` falls outside a Pin's stated age range are left out of that Pin.
- Order of priority while holiday searches peak (Nov–mid Dec): holiday gift guides by age, themed gift sets (movement, sensory, wooden, "gifts that aren't plastic", stocking stuffers), then single-product heroes.

## 8. Board map

| Pin topic | Board |
| --- | --- |
| Any gift guide / gift set | Gift Guides for Intentional Play |
| Movement / gross motor product Pins (non-gift framing) | Types of Play |
| Infant materials | Infant Provocations |
| 1–2 year materials | 1-2 Year Old Provocations |
| Toddler materials | Toddler Provocations |
| Open-ended materials / loose parts | Materials |
| Learning environments / furniture | Reggio Classroom Design |

Create no new boards without Ellie's approval.
