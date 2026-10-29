# Prix Fixe Brasserie: website redesign

A redesign concept for [Prix Fixe Brasserie](https://www.prixfixe.net/), a French brasserie at 39 Dean Street, Soho, London. Built as plain HTML, CSS and JavaScript.

**Pages:** Home · Menus (set, à la carte, desserts, wine) · The Brasserie (story, groups, photos) · Find us (map + group enquiry) · Book a table

## Run locally

```bash
python3 -m http.server 5180
```

Then open http://localhost:5180. Any static file server works.

## Structure

```
index.html, menu.html, about.html, contact.html, reservation.html
assets/css/style.css   all styles
assets/js/main.js      mobile nav, scroll reveal, menu tab highlighting, booking form
assets/img/            photos and logo
```

## Design

- Direction: a Soho brasserie at night. Oxblood and cream, with the red neon of the shop sign as the accent colour.
- Logo: vector trace of the original lettering (from the menu PDF artwork). Horizontal and stacked versions, red (light backgrounds) and neon (dark backgrounds), as SVG and PNG in `assets/logo/`. The stacked layout is aligned to the original stacked neon logo.
- Fonts: Bodoni Moda (headings), DM Sans (body), Yellowtail (neon script), all from Google Fonts under the SIL Open Font License.

## Notes

- This is a design concept, not the restaurant's official site. The booking and group enquiry forms have no backend.
- Menu items and prices come from the PDF menus on prixfixe.net (set menu, à la carte, desserts, wine list). The wine list on the menu page is a selection.
- Tripadvisor reviews and the Travellers' Choice 2026 award are from Tripadvisor screenshots supplied by the client. Ratings (OpenTable 4.8, Tripadvisor 4.4), opening hours and review quotes were collected in October 2026 from search listings, [Harden's](https://www.hardens.com/az/restaurants/london/w1/prix-fixe.htm) and [Yelp](https://www.yelp.co.uk/biz/prix-fixe-london-2). Tripadvisor and OpenTable block automated reading, so their figures come from search results. Check them before going live.
- Photos and logo belong to Prix Fixe Brasserie (from prixfixe.net). Map © OpenStreetMap contributors.

## Languages

English pages in the root are the source. French (`fr/`) and Traditional Chinese (`zh/`) pages are generated from them:

```bash
python3 i18n/build.py
```

Run it after any change to an English page. Translations live in `i18n/translations.py`, keyed by the English text; the script lists any text it left untranslated (wine names, places and brands are kept on purpose). Don't edit `fr/` or `zh/` by hand. The script also adds the EN / FR / 中文 switcher and hreflang links to every page.

## Pitch

`pitch/` holds before/after comparisons of prixfixe.net (as it rendered on 29 October 2026) and the redesign, desktop and phone.

When you change `style.css` or `main.js`, bump the `?v=` number on their links in every page, so browsers and GitHub Pages fetch the new file instead of a cached one.
