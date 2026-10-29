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
- Fonts: Bodoni Moda (headings), DM Sans (body), Yellowtail (neon script), all from Google Fonts under the SIL Open Font License.

## Notes

- This is a design concept, not the restaurant's official site. The booking and group enquiry forms have no backend.
- Menu items and prices come from the PDF menus on prixfixe.net (set menu, à la carte, desserts, wine list). The wine list on the menu page is a selection.
- The current site doesn't list full opening hours, so only set lunch and pre-theatre times are shown.
- Photos and logo belong to Prix Fixe Brasserie (from prixfixe.net). Map © OpenStreetMap contributors.
