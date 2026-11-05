# Yalla Pinterest — Pin Standards

The rulebook for every Pin made for **Yalla | Play & Childhood** (pinterest.com/yallachildcare).
**Read BRAND.md first.** It is the purpose behind these rules and wins any conflict. Every Pin, every run, follows both.

## 1. The goal of every Pin

1. **Be genuinely useful**: answer a real need, question or experience of a parent or early childhood educator, so Yalla becomes a trusted resource for understanding play and creating spaces for children.
2. **Be found and saved on Pinterest.** Pinterest is a visual search engine. A Pin spreads when its image stops the scroll and its words match what people are searching for at that moment.
3. **Let affiliate income grow from that trust.** Product-supported Pins link to a real, tagged Amazon Storefront list or product. No-purchase Pins link to a Yalla resource page when one exists, or have no link.

Honesty note: no copy guarantees virality. We maximise the odds: usefulness, search-matched keywords, strong seasonal timing, beautiful photography, fresh Pin designs.

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

## 3b. How a Pin is built: need → answer → product

Every Pin follows BRAND.md's structure:
1. **Start with a need, question or experience** ("How do I set up a comfortable floor-play space for a baby?", "What can my toddler do with a basket of kitchen things?"). The headline speaks to that moment, not to a product.
2. **Answer it with clear, specific guidance** in the description: what to do, how, and why it helps. Concrete examples ("children might fill, dump, sort and line them up").
3. **Introduce a product only when it meaningfully supports the answer.** Then, in the description, say:
   - **who it's useful for**,
   - **how to use it**,
   - **why we chose it**.
4. **Firsthand experience:** if the product's `firsthand` field in `catalog/products.json` has Ellie's note, use it specifically ("In our infant room, we…"). If it is empty, describe the product from its listing and our reasoning, and never imply Yalla has used it. Never write "we love", "our favorite" or "we use" without a `firsthand` note.

Two kinds of Pin:
- **No-purchase Pins**: room arrangements, invitations with materials families already have, observations about child development, caregiving tips, simpler routines. No affiliate link, no disclosure; destination = a Yalla resource page if one exists (`catalog/destinations.json`), otherwise none. Topics come from `catalog/ideas.json`.
- **Product-supported Pins**: same structure, with the product woven into the answer, linking to the matching list or product, with the disclosure.

Graphics:
- **No product labels or counts** on graphics. The image shows it; the alt text and description name it. Clearly shopping-style Pins (gift guides) may label sparingly, never with counts or sizes.
- Shopping words ("must-have", "essentials", "shop", "buy", "deal") stay out of headlines.
- No pressure to buy, no developmental promises, and never imply families need expensive things.

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
- Photos of children only from Ellie, only those she has permission to publish, and preferably without identifiable faces. Never crop or edit a photo to reveal a face the original avoided.

## 6. Visual system

Brand colors: Yalla Blue `#6065F2`, Ink `#292C45`, Chalk `#F7F5EF`, Paper `#FBFAF6`, Mist `#E7E5F1`, Ink Soft `#5A5D74`, Lilac `#C8B9DC`.
Fonts: **Lora** (headlines; final clause in *italic*), **DM Sans** (eyebrows/small caps).
Brand marks: real wordmark file only (never retyped). **The logo is never central.** No logo bands. On some Pins a tiny wordmark sits quietly in a bottom corner (`"mark": "small"`, ~64px wide, low opacity); on others there is no mark at all (`"mark": "none"`). Vary it across the day's set — roughly half with a small mark, half without. The scallop is used only as a soft edge on photo panels, never as a branded band.

Layouts (render with `scripts/render_pin.py`):
- **float — the primary layout for product Pins.** Product cut-outs are spread seamlessly across the Pin with soft shadows, like an editorial flat-lay, never boxed into tiles, grids or side-by-side frames. Optionally around a lifestyle photo (arch, rounded or full-width), with products overlapping the photo's edges so the photo and products read as one scene. Place each item by hand (`items` with x/y/w): vary sizes by real-world scale, keep generous breathing room, let a few items overlap photo edges, never overlap the headline, keep furniture upright (rotate ≤3°; soft goods like mats or silks up to ~8°), and never put similar colors side by side. Always look at the render and adjust until it feels composed, not stacked.
- The layouts below are secondary; use them sparingly.
- **band-collage** — products floating on Chalk around a full-width scalloped Yalla Blue title band. Big guides (8–14 products).
- **arches** — 2/4/6 products in Mist arches, Lora headline, Blue scallop band with wordmark. Themed sets.
- **hero** — one product large in an arch, headline above. Single-product Pins.
- **story** — a lifestyle photo on top, headline, then a row of 2–4 small arches with the products that make the moment possible ("Tummy time, from the floor up"). Best for theme roundups. Never pair a product cut-out whose color differs from the one in the photo.
- **photo** — a lifestyle or room photo, full-bleed on top (`frame: full`) or inside a tall arch (`frame: arch`), headline below/above. Use these as often as the library allows: real moments sell organically better than cut-outs. Lifestyle photos live in `assets/lifestyle/<product-id>/` and are listed in each product's `lifestyle` field; a photo Pin links to the list containing that product, and its description names the product as part of the moment. Never crop to reveal a face that the original avoided.

Rules Ellie set:
- **Photography first.** Warm, natural light, rich but believable color, inviting spaces, materials shown in context. Use lifestyle and room photos whenever the library has them; product cut-outs support photos, not replace them.
- **Image-centric.** Text on the graphic is a short headline only; the guidance lives in the description.
- **No small notes** on graphics (no tips, no "affiliate links" tags, no captions beyond product names in arches).
- **Don't place similar-colored products side by side** (e.g. red/yellow dump truck next to the red/yellow Cozy Coupe).
- 1000 × 1500 px, 2:3.
- Headlines: the plain clause on one line, the italic clause on the next.
- Every new Pin must be a **fresh design** — vary layout, product subset, headline and background (Chalk / Mist / Blue / Ink) so Pinterest treats it as new content.
- Always look at the rendered PNG before uploading: no overlaps, no clipping, nothing touching the band or wordmark.

## 7. Cadence

- Target: **7 Pins per day**, every day.
- **Daily mix: about 3 no-purchase Pins and 4 product-supported Pins.** The product-supported Pins are spread across Ellie's niche lists (§9). While holiday searches peak, at most 2 of the 4 are gift guides. If the photo library can't support 3 beautiful no-purchase Pins, make as many as it can and tell Ellie which photos would unlock more; never fill the gap with weak images.
- Mix: aim for no more than 3 Pins to the same destination URL per day; rotate boards; mix layouts. While the catalog has only one or two lists, more Pins may share a URL, but each must be a clearly different design, product subset and search angle (never near-duplicates).
- Products with `"hold": true` in `catalog/products.json` are not used in new Pins until Ellie confirms the image matches the listing.
- Products whose `listing_age` falls outside a Pin's stated age range are left out of that Pin.
- Seasonal timing: in Nov–mid Dec, gift guides by age and themed gift ideas are timely for the gift-guide slots; framing stays need-first ("what will they actually play with?").

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
| Infant room setup, layout, essentials | Reggio Classroom Design or Classroom Ideas |
| Infant materials (mirrors, baskets, mats) | Infant Provocations or Materials |

Create no new boards without Ellie's approval.

## 9. Lists, niches & the daily mix

Each Amazon list is a niche with its own audience. `catalog/lists.json` holds, per list: `niche` (who it serves), `search_angles` (gaps in Pinterest search to fill), `boards`, `daily_target` (Pins per day) and optional `active_until`.

Daily mix:
- Split the 7 daily Pins across active lists by `daily_target` (a list past `active_until` is inactive).
- A list can only get Pins for products that have an image and no `hold`. If a list can't support its target with genuinely fresh designs, give its slots to other lists and tell Ellie what's needed.
- Every Pin targets one `search_angle` (or a closely related phrase) as its main keyword. Over days, cover all angles of each list before repeating one, so Yalla fills many gaps in search rather than competing with itself.
- Write for that list's audience. Gift Pins speak to parents and gift-givers; infant classroom Pins speak to infant room teachers, center directors and home daycare providers.

### Infant classroom list — specifics
- Audience: infant teachers, educarers, directors, family/home daycare providers, people opening a program.
- Search terms people actually use ("infant classroom", "daycare infant room", "infant room setup") belong in titles, descriptions and alt text even though Yalla's own word is "learning environment"; graphic headlines can use Yalla's language.
- Angles: natural / neutral infant room; Reggio Emilia-inspired infant room; Montessori-style infant room; movement & tummy time area (mats, mirror with bar, mirror cubbies); diapering station (changing table, wall organizer); rest area (daycare cribs); feeding (low chairs); low open shelves and natural-material baskets; home daycare infant setup; setting up a new infant room checklist.
- Never claim a product meets licensing or safety regulations. Licensing rules vary by state: when relevant, say "check your state's licensing requirements". Describe crib/changing-table features only as the listing states them.
- Real photos of a calm, natural infant room (no children, or only with permission and never in this public repo) outperform product collages for "infant classroom setup" searches — ask Ellie for them.
