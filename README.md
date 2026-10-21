# Jennifer Malecki Psychologist — WordPress build

Site: https://jennifermalecki.wsdfy.com (Atarim workspace: VentraIP)

## Stack

- Theme: Hello Elementor, with the child theme in `theme/hello-elementor-child`
  - `functions.php` loads every file in `assets/css` and `assets/js`, and lets admins upload SVG icons
  - `assets/css/jm-site.css` is the design layer Elementor controls can't express (animated waves, chips, hover motion, scroll reveal, breathing exercise)
  - `assets/js/jm-site.js` runs the breathing toggle and the footprint walk, and keeps the hero video playing
- Elementor 4.3 (free): containers plus core widgets, so every section is editable in the Elementor editor
- Ultimate Addons for Elementor (UAE): Site Header (post 33) and Site Footer (post 34), shown site-wide
- Home page: post 14, set as the static front page
- Inner pages: About (50), Services (51), Fees & Rebates (52), For Referrers (53), Gallery (54)
- Headers: Home uses post 33 (front page only); inner pages use post 55 (crisis bar, cream bar, full-screen menu)

## Source

- `design/home/` holds the design reference (`Main.dc.html`). Every value in the build comes from it.
- `assets/` holds the images, video and line icons uploaded to the media library.
- `design/pages/` holds the inner-page design exports (About, Services, Fees & Rebates, For Referrers, Gallery).
- `elementor/build.py` generates the Elementor data into `elementor/dist/`:
  - `home.json`, `header.json`, `footer.json`
  - `kit.json`: Site Settings (colours, Cormorant Garamond and Figtree fonts, container defaults)
- `elementor/build_css.py` generates `theme/hello-elementor-child/assets/css/jm-site.css`, inlining the decorative SVGs from `elementor/svg.py`.

- `elementor/build_pages.py` generates the inner pages and their header: `about.json`, `services.json`, `fees.json`, `referrers.json`, `gallery.json`, `header-inner.json`.

```sh
python3 elementor/build.py && python3 elementor/build_pages.py && python3 elementor/build_css.py
```

## Deploying

Push, then load `elementor/dist/*.json` into each post's `_elementor_data` meta. On this site that happens through the Atarim connector, with your approval. Afterwards, clear Elementor's CSS cache (Elementor → Tools → Regenerate CSS & Data).

Once the content team starts editing in Elementor, the editor is the source of truth. Re-running the build overwrites edits made there.

## Responsive behaviour

- Font sizes follow the design: fixed px values, or `clamp()` where the design uses it, entered as Elementor custom units.
- Two-column sections use flex-wrap with the design's flex-basis and grow values, so they stack where the design stacks.
- Card grids use `repeat(auto-fit, minmax(...))` as a custom grid-columns value.
- Header: the teal crisis bar sits at the top; below it there is no bar, just a round menu button floating over the hero video on every screen size (jm-site.js opens the UAE menu on desktop). The white logo sits in the hero above the title.
