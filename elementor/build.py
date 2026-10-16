"""Generates Elementor data (containers + core/UAE widgets) for the Home page,
the UAE header and footer, and the Elementor kit, from the 01 · Home design.

Every section is built from editable Elementor elements; values (font sizes,
spacing, colours, radii) are taken straight from design/home/Main.dc.html.

    python3 elementor/build.py   ->  elementor/dist/*.json
"""
import hashlib
import json
from pathlib import Path

DIST = Path(__file__).resolve().parent / "dist"

UPLOADS = "https://jennifermalecki.wsdfy.com/wp-content/uploads/2026/10/"
MEDIA = {
    "logo_dark": (7, "jm-logo-dark.png"),
    "logo_light": (8, "jm-logo-light.png"),
    "hero_poster": (9, "jm-hero-poster.jpg"),
    "sand": (11, "jm-sand-texture.jpg"),
    "art_ocean": (12, "jm-artwork-ocean.jpg"),
    "art_wave": (13, "jm-artwork-wave.jpg"),
    "i_clock": (23, "jm-icon-clock.svg"),
    "i_heart": (24, "jm-icon-heart.svg"),
    "i_palette": (25, "jm-icon-palette.svg"),
    "i_waves": (26, "jm-icon-waves.svg"),
    "i_smile": (27, "jm-icon-smile.svg"),
    "i_search": (28, "jm-icon-search-time.svg"),
    "i_phone": (29, "jm-icon-phone.svg"),
    "i_mail": (30, "jm-icon-mail.svg"),
    "i_arrow": (31, "jm-icon-arrow-right.svg"),
    "i_wave_line": (32, "jm-icon-wave-line.svg"),
    "i_menu": (36, "jm-icon-menu.svg"),
    "i_close": (37, "jm-icon-close.svg"),
}
HERO_VIDEO = UPLOADS + "jm-hero-ocean.mp4"

# Palette
INK, TEAL, TEAL_DK, SAND, STONE, OCHRE = "#12323F", "#1D5067", "#0d4c5c", "#F7F5EF", "#EBE7DB", "#DDAA33"
BODY, BODY_DK, MUTED, MIST, MIST_LT = "#3E5A66", "#22414D", "#C9D6DC", "#A2C3D3", "#DCE8EE"
SERIF, SANS, SCRIPT = "Cormorant Garamond", "Figtree", "Great Vibes"

PHONE, PHONE_URL = "0404 174 184", "tel:0404174184"
EMAIL = "psych@jennifermalecki.com.au"
# Inner pages aren't built yet, so their links are "#" placeholders for now. Swap in the real
# paths (/about/, /services/, /fees-rebates/, /for-referrers/, /gallery/, /resources/,
# /contact/) as each page goes live.
URL = {
    "home": "/", "about": "#", "services": "#", "fees": "#",
    "referrers": "#", "gallery": "#", "resources": "#", "contact": "#",
}

_ids: set = set()


def uid(seed: str) -> str:
    """Stable 7-char element id, so re-running the build keeps ids unchanged."""
    n = 0
    while True:
        h = hashlib.md5(f"{seed}|{n}".encode()).hexdigest()[:7]
        if h not in _ids:
            _ids.add(h)
            return h
        n += 1


# ---------------------------------------------------------------- value helpers

def px(v, unit="px"):
    if isinstance(v, str):
        return {"unit": "custom", "size": v}
    return {"unit": unit, "size": v}


def dims(t, r=None, b=None, l=None, unit="px"):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    vals = [t, r, b, l]
    if any(isinstance(v, str) and not v.lstrip("-").isdigit() for v in vals):
        unit = "custom"
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l),
            "isLinked": len(set(map(str, vals))) == 1}


def gap(row, col=None):
    col = row if col is None else col
    return {"row": str(row), "column": str(col), "isLinked": row == col, "unit": "px", "size": col}


def media(key):
    mid, name = MEDIA[key]
    return {"url": UPLOADS + name, "id": mid}


def svg_icon(key):
    mid, name = MEDIA[key]
    return {"value": {"url": UPLOADS + name, "id": mid}, "library": "svg"}


def link(url, external=False):
    return {"url": url, "is_external": "on" if external else ""}


def typo(prefix, family, size, weight=None, lh=None, ls=None, transform=None, style=None):
    s = {f"{prefix}_typography": "custom", f"{prefix}_font_family": family, f"{prefix}_font_size": px(size)}
    if weight:
        s[f"{prefix}_font_weight"] = str(weight)
    if lh is not None:
        s[f"{prefix}_line_height"] = px(lh, "em")
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = px(ls, "em")
    if transform:
        s[f"{prefix}_text_transform"] = transform
    if style:
        s[f"{prefix}_font_style"] = style
    return s


def border(width, color, radius=None):
    s = {"border_border": "solid", "border_width": dims(width), "border_color": color}
    if radius is not None:
        s["border_radius"] = radius if isinstance(radius, dict) else dims(radius)
    return s


def gradient(a, b, angle=180):
    return {"background_background": "gradient", "background_color": a, "background_color_stop": px(0, "%"),
            "background_color_b": b, "background_color_b_stop": px(100, "%"),
            "background_gradient_type": "linear", "background_gradient_angle": px(angle, "deg")}


def sand_bg(color="#E4D4B2"):
    return {"background_background": "classic", "background_color": color, "background_image": media("sand"),
            "background_repeat": "repeat", "background_size": "initial", "background_bg_width": px(800),
            "background_position": "top left"}


# ---------------------------------------------------------------- element helpers

def container(name, children, *, boxed=False, row=False, wrap=False, gap_=0, pad=0, cls="", tag=None,
              justify=None, align=None, width=None, grow=None, shrink=1, mobile_width=True, **extra):
    s = {
        "content_width": "boxed" if boxed else "full",
        "flex_direction": "row" if row else "column",
        "flex_gap": gap_ if isinstance(gap_, dict) else gap(gap_),
        "padding": pad if isinstance(pad, dict) else dims(pad),
    }
    if boxed:
        s["boxed_width"] = px(1240)
    if wrap:
        s["flex_wrap"] = "wrap"
    if justify:
        s["flex_justify_content"] = justify
    if align:
        s["flex_align_items"] = align
    if width is not None:
        s["width"] = px(width) if not isinstance(width, dict) else width
        if mobile_width and isinstance(width, (int, float)) and width > 0:
            s["width_mobile"] = px(100, "%")
    if grow is not None:
        s["_flex_size"] = "custom"
        s["_flex_grow"] = grow
        s["_flex_shrink"] = shrink
    if cls:
        s["css_classes"] = cls
    if tag:
        s["html_tag"] = tag
    s.update(extra)
    return {"id": uid(name), "elType": "container", "isInner": False, "settings": s, "elements": children}


def grid(name, children, min_col, gap_, cols_mobile=None, **extra):
    s = {
        "container_type": "grid", "content_width": "full",
        "grid_columns_grid": px(f"repeat(auto-fit, minmax(min({min_col}px, 100%), 1fr))"),
        "grid_rows_grid": px("auto"),
        "grid_gaps": gap(gap_), "grid_outline": "", "padding": dims(0),
    }
    if cols_mobile:
        s["grid_columns_grid_mobile"] = {"unit": "fr", "size": cols_mobile, "sizes": []}
    s.update(extra)
    return {"id": uid(name), "elType": "container", "isInner": False, "settings": s, "elements": children}


def widget(name, wtype, settings):
    return {"id": uid(name), "elType": "widget", "widgetType": wtype, "settings": settings, "elements": []}


def heading(name, text, tag, family, size, color, *, weight=None, lh=None, ls=None, transform=None,
            style=None, align=None, cls="", shadow=None, maxw=None, **extra):
    s = {"title": text, "header_size": tag, "title_color": color}
    s.update(typo("typography", family, size, weight, lh, ls, transform, style))
    if align:
        s["align"] = align
    if cls:
        s["_css_classes"] = cls
    if shadow:
        h, v, blur, c = shadow
        s["text_shadow_text_shadow_type"] = "yes"
        s["text_shadow_text_shadow"] = {"horizontal": h, "vertical": v, "blur": blur, "color": c}
    if maxw:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = px(maxw)
    s.update(extra)
    return widget(name, "heading", s)


def text(name, html, size, color, *, lh=None, family=SANS, weight=None, cls="", maxw=None, align=None, **extra):
    s = {"editor": html, "text_color": color}
    s.update(typo("typography", family, size, weight, lh))
    if cls:
        s["_css_classes"] = cls
    if maxw:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = px(maxw)
    if align:
        s["align"] = align
    s.update(extra)
    return widget(name, "text-editor", s)


def eyebrow(name, label, color=TEAL, ls=0.16, **extra):
    return heading(name, label, "p", SANS, 13, color, weight=600, lh=1.2, ls=ls, transform="uppercase", **extra)


def h2(name, label, size="clamp(36px, 4vw, 54px)", lh=1.08, color=INK, tag="h2", **extra):
    return heading(name, label, tag, SERIF, size, color, weight=600, lh=lh, ls=-0.01, **extra)


BTN_STYLES = {
    #            text   bg      border   hover-text hover-bg  hover-border
    "primary": ("#ffffff", TEAL, None, "#ffffff", TEAL_DK, None),
    "ghost": (TEAL, "", TEAL, "#ffffff", TEAL, TEAL),
    "ochre": (INK, OCHRE, None, INK, "#E8BE57", None),
    "light": (SAND, "", STONE, INK, STONE, STONE),
}


def button(name, label, url, style="primary", *, full=False, cls="", grow_none=True, **extra):
    fg, bg, bd, hfg, hbg, hbd = BTN_STYLES[style]
    s = {
        "text": label, "link": link(url) if url else {"url": ""},
        "button_text_color": fg, "hover_color": hfg,
        "background_background": "classic", "background_color": bg or "transparent",
        "button_background_hover_background": "classic", "button_background_hover_color": hbg,
        "border_border": "solid", "border_width": dims(2), "border_color": bd or "transparent",
        "button_hover_border_color": hbd or "transparent",
        "border_radius": dims(999), "text_padding": dims(15, 26),
        "button_hover_transition_duration": px(0.2, "s"),
    }
    s.update(typo("typography", SANS, 16, 600, 1))
    if full:
        s["align"] = "justify"
        s["content_align"] = "center"
    if cls:
        s["_css_classes"] = cls
    if grow_none and not full:
        s["_flex_size"] = "none"
    s.update(extra)
    return widget(name, "button", s)


def textlink(name, label, url, *, arrow=False, full=False, **extra):
    s = {
        "text": label, "link": link(url),
        "button_text_color": TEAL, "hover_color": TEAL_DK,
        "background_background": "classic", "background_color": "transparent",
        "button_background_hover_background": "classic", "button_background_hover_color": "transparent",
        "border_radius": dims(0), "text_padding": dims(14, 0),
        "_css_classes": "jm-textlink",
    }
    s.update(typo("typography", SANS, 16, 600, 1))
    if arrow:
        s["selected_icon"] = svg_icon("i_arrow")
        s["icon_align"] = "row-reverse"
        s["icon_indent"] = px(8)
    if full:
        s["align"] = "justify"
        s["content_align"] = "center"
    else:
        s["_flex_size"] = "none"
        s["_flex_align_self"] = "flex-start"
    s.update(extra)
    return widget(name, "button", s)


def icon(name, key, size, color=TEAL, cls="", **extra):
    s = {"selected_icon": svg_icon(key), "view": "default", "align": "start", "primary_color": color, "size": px(size)}
    if cls:
        s["_css_classes"] = cls
    s.update(extra)
    return widget(name, "icon", s)


def icon_list(name, items, *, inline=False, size=15, color=INK, hover=None, family=SANS, weight=None, lh=None,
              space=None, icon_size=None, icon_color=None, cls="", align=None, **extra):
    rows = []
    for i, item in enumerate(items):
        label, url, ico = (item + (None, None))[:3] if isinstance(item, tuple) else (item, None, None)
        row = {"text": label, "_id": uid(f"{name}-item-{i}"),
               "selected_icon": svg_icon(ico) if ico else {"value": "", "library": ""}}
        if url:
            row["link"] = link(url)
        rows.append(row)
    s = {"view": "inline" if inline else "traditional", "icon_list": rows, "text_color": color}
    s.update(typo("icon_typography", family, size, weight, lh))
    if hover:
        s["text_color_hover"] = hover
    if space is not None:
        s["space_between"] = px(space)
    if icon_size:
        s["icon_size"] = px(icon_size)
        s["text_indent"] = px(8)
    if icon_color:
        s["icon_color"] = icon_color
        if hover:
            s["icon_color_hover"] = hover
    if align:
        s["icon_align"] = align
    if cls:
        s["_css_classes"] = cls
    s.update(extra)
    return widget(name, "icon-list", s)


def image(name, key, *, width=None, height=None, url=None, cls="", fit=None, **extra):
    s = {"image": media(key), "image_size": "full", "align": "start"}
    if width:
        s["width"] = px(width)
    if height:
        s["height"] = px(height)
    if fit:
        s["object-fit"] = fit
    if url:
        s["link_to"] = "custom"
        s["link"] = link(url)
    if cls:
        s["_css_classes"] = cls
    s.update(extra)
    return widget(name, "image", s)


def html(name, code, cls=""):
    s = {"html": code}
    if cls:
        s["_css_classes"] = cls
    return widget(name, "html", s)


def section(name, children, *, pad, bg=None, cls="", boxed_width=1240, **kw):
    extra = {"html_tag": "section"}
    if bg:
        extra.update({"background_background": "classic", "background_color": bg})
    c = container(name, children, boxed=True, pad=pad, cls=cls, **extra, **kw)
    c["settings"]["boxed_width"] = px(boxed_width)
    return c


# ---------------------------------------------------------------- shared pieces

def wave_card(name, children, *, radius, pad, gap_, size="", hover=True):
    cls = "jm-wave-card" + (f" jm-wave-{size}" if size else "") + (" jm-card" if hover else "")
    return container(name, children, gap_=gap_, pad=pad, cls=cls,
                     **gradient("#FBFAF6", "#EEF4F6"), **border(1, "#D5E2E8", radius))


def section_head(name, kids, maxw, gap_=16):
    return container(name, kids, gap_=gap_, width=maxw, grow=0, shrink=1)


FOOTPRINT = ('<svg viewBox="0 0 22 34" aria-hidden="true" style="animation-delay:{d:.2f}s">'
             '<path d="M11 33c-4 0-6-3-6-8 0-6 1-10 3-13 2-2 6-2 7 1 2 4 2 9 1 13-1 4-2 7-5 7z"/>'
             '<circle cx="6" cy="6.5" r="2.2"/><circle cx="10" cy="3.6" r="2"/>'
             '<circle cx="14" cy="4.2" r="1.8"/><circle cx="17.2" cy="6.8" r="1.5"/></svg>')


def footprints(start):
    return ('<div class="jm-prints" aria-hidden="true">'
            + "".join(f"<span>{FOOTPRINT.format(d=start + i * 0.45)}</span>" for i in range(4)) + "</div>")


BREATH_HTML = (
    '<div class="jm-breath is-running" aria-hidden="true">'
    '<div class="jm-breath-words">'
    '<span class="jm-b-in">Breathe in…</span>'
    '<span class="jm-b-out">and out…</span>'
    '<span class="jm-b-idle">Press start when you are ready</span>'
    '</div>'
    '<div class="jm-breath-sea"><div class="jm-breath-rise">'
    '<div class="jm-breath-waves"></div><div class="jm-breath-body"></div>'
    '</div></div></div>'
)


# ---------------------------------------------------------------- header

def build_header():
    topbar = container("hdr-topbar", [
        text("hdr-crisis",
             f'<p>In an emergency call&nbsp;<a href="tel:000"><strong>000</strong></a> · 24/7 crisis support: '
             f'Lifeline&nbsp;<a href="tel:131114"><strong>13&nbsp;11&nbsp;14</strong></a></p>',
             14, STONE, lh=1.4, _flex_size="shrink",
             # Tablet/mobile: when the bar wraps, centre each line; on phones the crisis line takes
             # its own (two-line) row and the phone and email share one row underneath.
             align_tablet="center", typography_font_size_mobile=px(13), _element_width_mobile="inherit"),
        icon_list("hdr-contact", [(PHONE, PHONE_URL, "i_phone"), (EMAIL, f"mailto:{EMAIL}", "i_mail")],
                  inline=True, size=14, color=STONE, hover=OCHRE, lh=1.4, space=22, icon_size=16,
                  icon_color=STONE, _flex_size="shrink",
                  icon_align_tablet="center", icon_typography_font_size_mobile=px(13),
                  space_between_mobile=px(16), _element_width_mobile="inherit"),
    ], boxed=True, row=True, wrap=True, justify="space-between", align="center", gap_=gap(6, 24),
        pad=dims(10, 24), cls="jm-topbar", background_background="classic", background_color=INK,
        flex_justify_content_tablet="center", flex_gap_mobile=gap(6, 24))

    nav = widget("hdr-nav", "navigation-menu", {
        "menu": "main-menu", "layout": "horizontal", "dropdown": "none", "navmenu_align": "left",
        "padding_horizontal_menu_item": px(13), "padding_vertical_menu_item": px(0),
        "menu_space_between": px(0), "menu_row_space": px(0),
        **typo("menu_typography", SANS, 15, 500, 1),
        "color_menu_item": SAND, "bg_color_menu_item": "",
        "color_menu_item_hover": "#ffffff", "bg_color_menu_item_hover": "rgba(255,255,255,0.12)",
        "color_menu_item_active": "#ffffff", "bg_color_menu_item_active": "rgba(255,255,255,0.18)",
        # Tablet and mobile (1024px and below): hamburger toggle; the menu opens as a panel under the pill.
        "dropdown": "tablet", "resp_align": "right", "full_width_dropdown": "yes",
        "dropdown_icon": svg_icon("i_menu"), "dropdown_close_icon": svg_icon("i_close"),
        "toggle_color": SAND, "toggle_hover_color": OCHRE, "toggle_size": px(28),
        "color_dropdown_item": SAND, "background_color_dropdown_item": INK,
        "color_dropdown_item_hover": "#ffffff", "background_color_dropdown_item_hover": TEAL,
        "color_dropdown_item_active": OCHRE, "background_color_dropdown_item_active": INK,
        **typo("dropdown_typography", SANS, 17, 500, 1.2),
        "padding_horizontal_dropdown_item": px(24), "padding_vertical_dropdown_item": px(16),
        "distance_from_menu": px(0),
        "dropdown_divider_border": "solid", "divider_border_color": "rgba(255,255,255,0.1)",
        "dropdown_divider_width": px(1),
        "_css_classes": "jm-nav",
        "_flex_size": "none",
    })

    # Floating header: a rounded glass pill over the hero (position and blur are in jm-site.css).
    main = container("hdr-main", [
        image("hdr-logo", "logo_light", width=92, height=60, fit="contain", url=URL["home"],
              _flex_size="none", width_mobile=px(76), height_mobile=px(50)),
        nav,
        button("hdr-cta", "Request a chat", URL["contact"], "ochre",
               hide_tablet="hidden-tablet", hide_mobile="hidden-mobile"),
    ], row=True, justify="space-between", align="center", gap_=gap(12, 20),
        pad=dims(10, 10, 10, 28), padding_mobile=dims(8, 8, 8, 18), cls="jm-header-main",
        flex_wrap="nowrap", flex_wrap_mobile="nowrap",
        background_background="classic", background_color="rgba(18,50,63,0.72)",
        border_border="solid", border_width=dims(1), border_color="rgba(255,255,255,0.14)",
        border_radius=dims(999))

    return [topbar, main]


# ---------------------------------------------------------------- footer

def build_footer():
    h = lambda n, t: heading(n, t, "h2", SERIF, 24, "#ffffff", weight=600, lh=1.2, ls=-0.01)
    cols = grid("ftr-grid", [
        container("ftr-col-brand", [
            image("ftr-logo", "logo_light", width=170),
            text("ftr-entity", "<p>Jennifer Malecki – Psychologist<br>"
                               "Jennifer Malecki &amp; Associates Pty Ltd</p>", 14, MUTED, lh=1.6),
        ], gap_=16),
        container("ftr-col-visit", [
            h("ftr-visit-h", "Visit"),
            text("ftr-address", "<p>Unit 1 / 38 Burnett Street<br>Mooloolaba QLD 4557</p>", 15, MUTED, lh=1.7),
            text("ftr-mode", "<p>In person in Mooloolaba and secure telehealth</p>", 15, MUTED, lh=1.7),
        ], gap_=12),
        container("ftr-col-contact", [
            h("ftr-contact-h", "Contact"),
            icon_list("ftr-contact-links", [(PHONE, PHONE_URL), (EMAIL, f"mailto:{EMAIL}")],
                      size=15, color=STONE, hover=OCHRE, lh=1.2, space=12),
            text("ftr-reg", "<p>Provider No. 1894363H<br>AHPRA Reg. [PSY0000000000]</p>", 14, MUTED, lh=1.6),
        ], gap_=12),
        container("ftr-col-explore", [
            h("ftr-explore-h", "Explore"),
            icon_list("ftr-explore-links", [
                ("About Jennifer", URL["about"]), ("Services &amp; approach", URL["services"]),
                ("Fees &amp; rebates", URL["fees"]), ("For GPs &amp; referrers", URL["referrers"]),
                ("Gallery", URL["gallery"]), ("Resources &amp; support", URL["resources"]),
                ("Contact", URL["contact"]),
            ], size=15, color=STONE, hover=OCHRE, lh=1.2, space=10),
        ], gap_=10, tag="nav"),
    ], 220, 40)

    main = container("ftr-main", [cols], boxed=True, pad=dims(72, 24, 36, 24),
                     background_background="classic", background_color=INK)

    bottom = container("ftr-bottom", [
        container("ftr-bottom-inner", [
            text("ftr-crisis", "<p>This website is not a crisis service. If you are in immediate danger call 000, "
                               "or Lifeline on 13 11 14.</p>", 13, MUTED, lh=1.6),
            text("ftr-ack", "<p>[Acknowledgement of Country — wording to be confirmed by Jennifer]</p>", 13, MUTED, lh=1.6),
            container("ftr-legal", [
                text("ftr-copy", "<p>© 2026 Jennifer Malecki &amp; Associates Pty Ltd · ABN [00 000 000 000] · Artwork and "
                                 "images © Jennifer Malecki, not for reproduction</p>", 13, MUTED, lh=1.6,
                     _flex_size="shrink"),
                icon_list("ftr-policies", [("Privacy policy", "#"), ("Website disclaimer", "#")], inline=True,
                          size=13, color=STONE, hover=OCHRE, lh=1.6, space=20, _flex_size="none"),
            ], row=True, wrap=True, justify="space-between", gap_=gap(8, 24)),
        ], gap_=14, pad=dims(24, 0, 36, 0),
            border_border="solid", border_width=dims(1, 0, 0, 0), border_color="rgba(235,231,219,0.2)"),
    ], boxed=True, pad=dims(0, 24), background_background="classic", background_color=INK)

    for c in (main, bottom):
        c["settings"]["css_classes"] = "jm-footer"
        c["settings"]["html_tag"] = "div"
    return [main, bottom]


# ---------------------------------------------------------------- home page

def hero():
    lined = dict(family=SERIF, size="clamp(20px, 2vw, 28px)", color="#ffffff", weight=600, lh=1.2, ls=0.02,
                 align="center", cls="jm-lined", shadow=(0, 1, 12, "rgba(0,0,0,0.5)"))
    msg = container("hero-msg", [
        heading("hero-place", "Mooloolaba · Sunshine Coast", "p", lined.pop("family"), lined.pop("size"),
                lined.pop("color"), _margin=dims(0, 0, 4, 0), **lined),
        heading("hero-script", "You do not have to carry it alone", "p", SCRIPT, "clamp(46px, 6.2vw, 92px)",
                "#ffffff", weight=400, lh=1.1, align="center", maxw=1000, shadow=(0, 2, 20, "rgba(0,0,0,0.5)")),
        heading("hero-name", "Dr Jennifer Malecki, PhD · Psychologist", "p", SERIF, "clamp(20px, 2vw, 28px)",
                "#ffffff", weight=600, lh=1.2, ls=0.02, align="center", cls="jm-lined",
                shadow=(0, 1, 12, "rgba(0,0,0,0.5)"), _margin=dims(4, 0, 0, 0)),
    ], gap_=12, pad=dims(24, 24, 64, 24), justify="center", align="center", cls="jm-hero-msg",
        grow=1, background_background="classic", background_color="rgba(18,50,63,0.32)")
    return container("hero", [msg], tag="section", cls="jm-hero", align="stretch",
                     min_height=px("clamp(300px, 34vw, 500px)"),
                     background_background="video", background_video_link=HERO_VIDEO,
                     background_video_fallback=media("hero_poster"), background_play_on_mobile="yes",
                     background_color=TEAL, overflow="hidden")


def intro_band():
    left = container("intro-left", [
        heading("intro-pill", "Now accepting new clients &amp; referrals — no wait time", "p", SANS, 13, "#4E3A08",
                weight=600, lh=1.2, cls="jm-pill"),
        eyebrow("intro-eyebrow", "Psychologist · Mooloolaba, Sunshine Coast"),
        h2("intro-h1", "Cultivating resilience and healing through <em>integrated care pathways</em>",
           size="clamp(38px, 4.6vw, 62px)", lh=1.04, tag="h1", maxw=820, cls="jm-h1"),
        text("intro-lede", "<p>High-quality, personalised care for adults living with trauma, PTSD, depression, "
                           "anxiety, eating disorders and complex mental health concerns, with one-to-one attention "
                           "from an experienced psychologist.</p>",
             "clamp(17px, 1.4vw, 19px)", BODY_DK, lh=1.65, maxw=720),
    ], gap_=16, width=560, grow=999)
    right = container("intro-right", [
        button("intro-cta", "Request a chat", URL["contact"], "primary", full=True),
        button("intro-meet", "Meet Jennifer", URL["about"], "ghost", full=True),
        textlink("intro-call", f"or call {PHONE}", PHONE_URL, full=True),
    ], gap_=12, width=300, grow=0, mobile_width=False)
    return section("intro", [left, right], pad=dims(8, 24, 16, 24), row=True, wrap=True, gap_=gap(28, 56),
                   align="center", justify="space-between", cls="jm-rise")


def highlights():
    items = [
        ("i_clock", "16+ years' experience", "Community practice providing trusted, compassionate and individualised care."),
        ("i_heart", "Trauma-informed care", "Safe, collaborative therapy designed specifically to facilitate recovery from traumatic experiences."),
        ("i_palette", "Arts-based interventions", "Innovative, creative tools to communicate complex experiences and emotions."),
    ]
    cards = [wave_card(f"hl-card-{i}", [
        icon(f"hl-icon-{i}", ico, 34),
        heading(f"hl-h-{i}", title, "h2", SERIF, 28, INK, weight=600, lh=1.15, ls=-0.01),
        text(f"hl-p-{i}", f"<p>{body}</p>", 16, BODY, lh=1.6),
    ], radius=22, pad=dims(32, 32, 104, 32), gap_=12) for i, (ico, title, body) in enumerate(items)]
    return section("highlights", [grid("hl-grid", cards, 300, 20)], pad=dims(56, 24, 24, 24))


def welcome():
    left = container("wel-left", [
        eyebrow("wel-eyebrow", "Welcome"),
        h2("wel-h", "Personalised care in the heart of Mooloolaba"),
        text("wel-lede", "<p>If you are living with Post Traumatic Stress Disorder or Complex PTSD, depression, "
                         "anxiety, intense emotional distress or an eating disorder, help is here.</p>", 19, BODY_DK, lh=1.7),
        text("wel-p1", "<p>The clinic is located in the heart of Mooloolaba, where I offer a high-quality, personalised "
                       "approach to mental health care. You can expect more one-to-one active attention from an "
                       "experienced psychologist who will assess and treat your mental health concerns. I treat adults "
                       "from all walks of life.</p>", 17, BODY, lh=1.75),
        text("wel-p2", "<p>I also have published research, read globally, on how early life experiences and trauma "
                       "affect our experience of the body.</p>", 17, BODY, lh=1.75),
        text("wel-p4", "<p>I can help you make sense of the origins of your problems, and build the skills and make "
                       "the changes needed for a happier and more meaningful life.</p>", 17, BODY, lh=1.75),
        text("wel-p3", "<p>In our very first session, we will work together to build a safe, collaborative plan to "
                       "help you heal and reclaim your life.</p>", 17, BODY, lh=1.75),
    ], gap_=22, width=520, grow=999)
    right = container("wel-right", [
        container("wel-portrait", [], cls="jm-portrait", min_height=px(0),
                  border_radius=dims(200, 200, 28, 28), **gradient("#A2C3D3", TEAL, 170)),
        text("wel-caption", "<p><strong>Dr Jennifer Malecki, PhD</strong><br>"
                            "Psychologist, PhD, PsyBA General | AAPi</p>", 15, BODY, lh=1.5, cls="jm-caption"),
    ], gap_=14, width=360, grow=1)
    return section("welcome", [left, right], pad=dims(72, 24, 96, 24), row=True, wrap=True, gap_=56,
                   align="center", cls="jm-tide")


def beneath():
    chips = dict(inline=True, size=15, weight=500, lh=1.2, align="center")
    left = container("ben-left", [
        eyebrow("ben-eyebrow", "Beyond symptoms"),
        h2("ben-h", "What we see is only part of the story"),
        text("ben-p1", "<p>Anxiety, low mood or overwhelming emotions are often what bring people to therapy. They are "
                       "real and they matter, but they are rarely the whole picture.</p>", 17, BODY, lh=1.75),
        text("ben-p2", "<p>Approaches such as schema therapy help us gently explore what sits underneath, like early "
                       "experiences and long-standing patterns, so we can work on causes as well as symptoms.</p>",
             17, BODY, lh=1.75),
    ], gap_=20, width=360, grow=1)
    top = container("ben-top", [
        heading("ben-above", "Above the surface", "p", SANS, 12, TEAL, weight=700, lh=1.2, ls=0.16,
                transform="uppercase", align="center"),
        icon_list("ben-above-list", ["Anxiety", "Low mood", "Intense emotions", "Panic", "Relationship strain"],
                  color=INK, cls="jm-chips", **chips),
    ], gap_=14, pad=dims(36, 28, 92, 28), align="center", cls="jm-ice-top",
        background_background="classic", background_color=MIST_LT)
    bottom = container("ben-bottom", [
        heading("ben-below", "Beneath the surface", "p", SANS, 12, MIST, weight=700, lh=1.2, ls=0.16,
                transform="uppercase", align="center"),
        icon_list("ben-below-list", ["Early life experiences", "Long-standing patterns", "Trauma held in the body",
                                     "Unmet emotional needs", "Your whole story"],
                  color="#ffffff", cls="jm-chips jm-chips-dark", _element_width="initial",
                  _element_custom_width=px(520), **chips),
        heading("ben-caption", "Therapy works with what lies beneath, at a pace that feels safe for you.", "p",
                SERIF, 24, MIST_LT, style="italic", lh=1.3, align="center", maxw=460, cls="jm-mt-auto"),
    ], gap_=16, pad=dims(28, 28, 44, 28), align="center", cls="jm-ice-bottom", min_height=px(300), grow=1)
    figure = container("ben-figure", [top, bottom], width=560, grow=999, cls="jm-iceberg",
                       overflow="hidden", border_radius=dims(28),
                       background_background="classic", background_color=TEAL)
    return section("beneath", [left, figure], pad=dims(8, 24, 104, 24), row=True, wrap=True, gap_=56,
                   align="center", cls="jm-tide")


def services():
    items = [
        ("i_waves", "Complex mental health &amp; trauma recovery",
         "Extensive experience with adults living with PTSD, personality disorders, self-harming behaviours, "
         "depression, bipolar disorder, anxiety, mood disorders, schizophrenia and other serious mental health conditions."),
        ("i_smile", "Life events &amp; emotional regulation",
         "Support through grief and loss, adjustment difficulties, major life transitions, emotional regulation "
         "challenges, anger management issues and interpersonal difficulties."),
        ("i_search", "Resolving unclear distress",
         "For people who feel depressed or anxious but are unsure why, and who struggle to resolve ongoing problems."),
    ]
    head = container("svc-head", [
        section_head("svc-head-text", [eyebrow("svc-eyebrow", "How I can help"), h2("svc-h", "Clinical areas of support")], 640),
        button("svc-all", "All services", URL["services"], "ghost"),
    ], row=True, wrap=True, justify="space-between", align="flex-end", gap_=gap(20, 48))
    cards = [wave_card(f"svc-card-{i}", [
        icon(f"svc-icon-{i}", ico, 40),
        heading(f"svc-h-{i}", title, "h3", SERIF, 30, INK, weight=600, lh=1.12, ls=-0.01),
        text(f"svc-p-{i}", f"<p>{body}</p>", 16, BODY, lh=1.65),
    ], radius=24, pad=dims(36, 36, 116, 36), gap_=14) for i, (ico, title, body) in enumerate(items)]
    return section("services", [head, grid("svc-grid", cards, 320, 20)], pad=dims(96, 24), bg=STONE, gap_=44,
                   cls="jm-tide")


def approach():
    art = container("app-art", [
        image("app-art-a", "art_ocean", cls="jm-swap-a"),
        image("app-art-b", "art_wave", cls="jm-swap-b"),
        heading("app-art-caption", "Original artwork © Jennifer Malecki", "p", SANS, 13, SAND, lh=1.2,
                cls="jm-art-caption"),
    ], cls="jm-art", border_radius=dims(28), overflow="hidden", background_background="classic",
        background_color=TEAL)
    left = container("app-left", [art], width=380, grow=1)

    stops = [("01", "Schema Therapy", "Patterns from early life"),
             ("02", "Trauma-Focused CBT", "Thoughts, feelings &amp; trauma"),
             ("03", "Dialectical Behaviour Therapy", "Skills for intense emotions")]
    stop_els = [container(f"app-stop-{n}", [
        heading(f"app-stone-{n}", n, "span", SERIF, 20, TEAL, weight=700, lh=1, cls="jm-stone",
                _flex_size="none"),
        container(f"app-stop-text-{n}", [
            heading(f"app-stop-name-{n}", name, "span", SANS, 17, INK, weight=600, lh=1.25),
            heading(f"app-stop-sub-{n}", sub, "span", SANS, 14, BODY, lh=1.35),
        ], gap_=2, grow=1, width=px(0, "%"), mobile_width=False),
        icon(f"app-stop-arrow-{n}", "i_arrow", 18, cls="jm-stop-arrow", _flex_size="none"),
    ], row=True, align="center", gap_=16, pad=dims(8, 14, 8, 0), tag="a", link=link(URL["services"]),
        cls="jm-stop", min_height=px(80), border_radius=dims(16), flex_wrap="nowrap",
        flex_wrap_mobile="nowrap") for n, name, sub in stops]

    right = container("app-right", [
        eyebrow("app-eyebrow", "My approach"),
        h2("app-h", "Evidence-based therapy that looks at your whole story"),
        text("app-p", "<p>I use a range of evidence-based therapies to support clients in their journey towards "
                      "healing and personal growth, integrating them to stabilise mental health concerns, identify "
                      "underlying causes and support recovery.</p>", 17, BODY, lh=1.75),
        container("app-path", [
            eyebrow("app-path-label", "Your care pathway", ls=0.14, _margin=dims(0, 0, 10, 64)),
            container("app-path-list", stop_els, cls="jm-care-list"),
        ]),
        container("app-mapping", [
            heading("app-mapping-h", "Arts-based therapy &amp; body mapping", "h3", SERIF, 30, INK, weight=600,
                    lh=1.15, ls=-0.01),
            text("app-mapping-p", "<p>To enrich the therapeutic process, you may choose to integrate arts-based "
                                  "techniques into therapy. Body mapping is used to explore and express aspects of the "
                                  "self, alongside your regular treatment.</p>", 16, "#33505C", lh=1.7),
            textlink("app-mapping-link", "About body mapping", URL["services"], arrow=True),
        ], gap_=12, pad=dims(32), margin=dims(8, 0, 0, 0), border_radius=dims(24),
            background_background="classic", background_color=STONE),
    ], gap_=22, width=520, grow=999)
    return section("approach", [left, right], pad=dims(104, 24), row=True, wrap=True, gap_=64, align="center",
                   cls="jm-tide")


def funding():
    items = [("Medicare", "Mental Health Care Plan with a referral from your GP or psychiatrist."),
             ("Eating Disorder Plan", "Sessions under an ED Plan arranged with your GP."),
             ("NDIS", "Self-managed and plan-managed participants."),
             ("DVA", "Eligible veterans and families, Gold or White Card with a D904 referral."),
             ("Private clients", "No referral needed. Claim through your extras cover.")]
    head = container("fund-head", [
        section_head("fund-head-text", [
            eyebrow("fund-eyebrow", "Fees &amp; rebates"),
            h2("fund-h", "Ways to access care", size="clamp(34px, 3.6vw, 48px)", lh=1.1),
            text("fund-p", "<p>Receipts are supplied for clients who wish to claim rebates from private health.</p>",
                 17, BODY, lh=1.7),
        ], 660),
        button("fund-more", "Fees, rebates &amp; referrals", URL["fees"], "ghost"),
    ], row=True, wrap=True, justify="space-between", align="flex-end", gap_=gap(20, 48))
    cards = [wave_card(f"fund-card-{i}", [
        heading(f"fund-h-{i}", title, "h3", SERIF, 24, INK, weight=600, lh=1.2, ls=-0.01),
        text(f"fund-p-{i}", f"<p>{body}</p>", 15, BODY, lh=1.55),
    ], radius=20, pad=dims(26, 26, 76, 26), gap_=8, size="sm") for i, (title, body) in enumerate(items)]
    return section("funding", [head, grid("fund-grid", cards, 220, 16)], pad=dims(0, 24, 104, 24), gap_=36,
                   cls="jm-tide")


def referrers():
    dark = dict(gap_=12, pad=dims(30), cls="jm-card jm-card-dark",
                background_background="classic", background_color="rgba(247,245,239,0.08)",
                **border(1, "rgba(162,195,211,0.35)", 22))
    head = section_head("gp-head", [
        heading("gp-pill", "Immediate availability · no wait time", "p", SANS, 14, INK, weight=700, lh=1.2,
                cls="jm-pill jm-pill-ochre"),
        h2("gp-h", "For GPs &amp; referring practitioners", color="#ffffff"),
        text("gp-p", "<p>I value collaboration with referring professionals to ensure continuity of care and "
                     "coordinated treatment planning. Referrers receive timely updates following assessment and at "
                     "key review points.</p>", 18, MIST_LT, lh=1.7),
    ], 760, gap_=18)
    cards = grid("gp-grid", [
        container("gp-card-refer", [
            heading("gp-refer-h", "How to refer", "h3", SERIF, 26, "#ffffff", weight=600, lh=1.2, ls=-0.01),
            text("gp-refer-list", f"<ul><li>Medical Objects</li><li>Phone {PHONE}</li><li>Email {EMAIL}</li></ul>",
                 16, MIST_LT, lh=1.8, cls="jm-refer-list"),
        ], **dark),
        container("gp-card-details", [
            heading("gp-details-h", "Practitioner details", "h3", SERIF, 26, "#ffffff", weight=600, lh=1.2, ls=-0.01),
            text("gp-details-p", "<p>Dr Jennifer Malecki, PhD<br>Psychologist, PsyBA General<br>Provider No. 1894363H<br>"
                                 "In person, Mooloolaba · Telehealth</p>", 16, MIST_LT, lh=1.8),
        ], **dark),
    ], 280, 20)
    actions = container("gp-actions", [
        button("gp-info", "Referrer information", URL["referrers"], "ochre"),
        button("gp-call", f"Call {PHONE}", PHONE_URL, "light"),
    ], row=True, wrap=True, gap_=12)
    return section("referrers", [head, cards, actions], pad=dims(96, 24), bg=TEAL, gap_=44, cls="jm-gp jm-tide")


def next_steps():
    """The three steps, each led by a trail of footprints. They open the closing sand section."""
    steps = [("01", "Reach out", "Phone, email or send an enquiry. A referral is optional if you are attending as a private client."),
             ("02", "A short chat", "A free 15-minute consultation to talk about what you are looking for and whether we are a good fit."),
             ("03", "Your first session", "Together we build a safe, collaborative plan. Every journey is unique, and we review progress together along the way.")]
    step_els = [container(f"step-{i}", [
        html(f"step-prints-{i}", footprints(i * 1.8)),
        heading(f"step-num-{i}", n, "span", SERIF, 56, TEAL, weight=600, lh=1),
        heading(f"step-h-{i}", title, "h3", SERIF, 28, INK, weight=600, lh=1.2, ls=-0.01),
        text(f"step-p-{i}", f"<p>{body}</p>", 16, BODY, lh=1.65),
    ], gap_=10, width=300, grow=1, cls="jm-step", tag="article") for i, (n, title, body) in enumerate(steps)]
    head = container("start-head", [
        eyebrow("start-eyebrow", "Getting started", align="center"),
        h2("start-h", "Your next step", align="center"),
        text("start-p", "<p>One step at a time, at your own pace.</p>", 17, BODY, lh=1.7, align="center"),
    ], gap_=16, align="center", width=640, grow=0, _flex_align_self="center", margin=dims(0, 0, 44, 0))
    path = container("start-path", step_els, row=True, gap_=gap(36, 48), cls="jm-steps",
                     flex_direction_mobile="column", flex_wrap="nowrap")
    return [head, path]


def breathe():
    left = container("br-left", [
        eyebrow("br-eyebrow", "A moment for you", color=MIST),
        h2("br-h", "Take a breath with the ocean", color="#ffffff"),
        text("br-p", "<p>Follow the wave: breathe in as it rises, and out as it settles back to shore. Slow breathing "
                     "is one of the simple distress-tolerance skills we can build on together.</p>", 17, MIST_LT, lh=1.7),
        container("br-actions", [
            button("br-toggle", "Pause", "", "ochre", cls="jm-breath-toggle"),
            text("br-count", "<p>In for 4 · out for 6</p>", 14, MUTED, lh=1.4, _flex_size="none"),
        ], row=True, wrap=True, align="center", gap_=gap(12, 20)),
    ], gap_=18, justify="center", width=380, grow=1,
        pad=dims("clamp(28px, 4vw, 56px)"))
    right = container("br-wave", [html("br-html", BREATH_HTML)], width=440, grow=1, cls="jm-breath-col",
                      min_height=px(360), overflow="hidden", background_background="classic", background_color=TEAL)
    card = container("br-card", [left, right], row=True, wrap=True, align="stretch", cls="jm-breathe",
                     overflow="hidden", border_radius=dims(28), background_background="classic",
                     background_color=INK)
    return section("breathe", [card], pad=dims(104, 24), cls="jm-tide")


def support_now():
    tiles = [("Emergency", "000", "tel:000", True),
             ("Lifeline, 24/7", "13 11 14", "tel:131114", False),
             ("Medicare Mental Health", "1800 595 212", "tel:1800595212", False),
             ("Open Arms (veterans), 24/7", "1800 011 046", "tel:1800011046", False)]
    tile_els = [container(f"sos-tile-{i}", [
        heading(f"sos-label-{i}", label, "span", SANS, 14, MUTED if dark else BODY, lh=1.2),
        heading(f"sos-num-{i}", number, "span", SANS, 26, "#ffffff" if dark else INK, weight=700, lh=1.2),
    ], gap_=4, pad=dims(20, 22), tag="a", link=link(url), border_radius=dims(18),
        cls="jm-tile" + (" jm-tile-emergency" if dark else ""),
        background_background="classic", background_color=INK if dark else "#EEF4F6")
        for i, (label, number, url, dark) in enumerate(tiles)]
    left = container("sos-left", [
        h2("sos-h", "Need support right now?", size="clamp(32px, 3.2vw, 44px)", lh=1.1),
        text("sos-p", "<p>This practice is not a crisis service. If you or someone else is in immediate danger, call "
                      "000 or go to your nearest hospital emergency department.</p>", 16, BODY, lh=1.65),
        textlink("sos-more", "More support services", URL["resources"], arrow=True),
    ], gap_=14, width=320, grow=1)
    tile_grid = grid("sos-grid", tile_els, 0, 12, cols_mobile=1, width=px(520), _flex_size="custom",
                     _flex_grow=999, _flex_shrink=1, width_mobile=px(100, "%"))
    tile_grid["settings"]["grid_columns_grid"] = {"unit": "fr", "size": 2, "sizes": []}
    card = wave_card("sos-card", [left, tile_grid], radius=28,
                     pad=dims("clamp(28px, 4vw, 52px)", "clamp(28px, 4vw, 52px)", "120px", "clamp(28px, 4vw, 52px)"),
                     gap_=gap(32, 56), size="lg", hover=False)
    card["settings"].update({"flex_direction": "row", "flex_wrap": "wrap", "flex_align_items": "center"})
    return section("support-now", [card], pad=dims(0, 24, 104, 24), cls="jm-tide")


def closing_cta():
    """Closing sand section: the next steps, then the invitation to get in touch."""
    invite = container("cta-invite", [
        icon("cta-wave", "i_wave_line", 28, cls="jm-wave-icon", align="center", fit_to_size="yes"),
        h2("cta-h", "I am here to listen and support your next step", size="clamp(38px, 4.4vw, 60px)", lh=1.06,
           align="center"),
        text("cta-p", "<p>I invite you to reach out by email or phone for a chat. In-person sessions in Mooloolaba, "
                      "and secure telehealth across the Sunshine Coast and surrounding areas.</p>",
             18, BODY, lh=1.7, align="center"),
        container("cta-actions", [
            button("cta-enquire", "Send an enquiry", URL["contact"], "primary"),
            button("cta-call", f"Call {PHONE}", PHONE_URL, "ghost"),
        ], row=True, wrap=True, justify="center", gap_=12),
    ], gap_=22, align="center", width=820, grow=0, _flex_align_self="center")
    divider = widget("cta-divider", "divider", {
        "style": "solid", "weight": px(1), "color": "rgba(29,80,103,0.18)", "width": px(820), "align": "center",
        "gap": px(0), "_margin": dims(72, 0, 56, 0),
    })
    return section("cta", [*next_steps(), divider, invite], pad=dims(136, 24, 120, 24), cls="jm-cta jm-tide",
                   **sand_bg())


def build_home():
    return [hero(), intro_band(), highlights(), welcome(), beneath(), services(), approach(), funding(),
            referrers(), breathe(), support_now(), closing_cta()]


# ---------------------------------------------------------------- kit (Site Settings)

def build_kit():
    t = lambda _id, title, fam, w: {"_id": _id, "title": title, "typography_typography": "custom",
                                    "typography_font_family": fam, "typography_font_weight": str(w)}
    kit = {
        "system_colors": [
            {"_id": "primary", "title": "Primary", "color": TEAL},
            {"_id": "secondary", "title": "Secondary", "color": INK},
            {"_id": "text", "title": "Text", "color": BODY},
            {"_id": "accent", "title": "Accent", "color": OCHRE},
        ],
        "custom_colors": [
            {"_id": "jmsand", "title": "Sand", "color": SAND},
            {"_id": "jmstone", "title": "Stone", "color": STONE},
            {"_id": "jmtealdk", "title": "Teal (hover)", "color": TEAL_DK},
            {"_id": "jmmist", "title": "Mist", "color": MIST},
            {"_id": "jmmistlt", "title": "Mist light", "color": MIST_LT},
            {"_id": "jmbodydk", "title": "Body dark", "color": BODY_DK},
            {"_id": "jmmuted", "title": "Muted on dark", "color": MUTED},
        ],
        "system_typography": [
            t("primary", "Primary", SERIF, 600), t("secondary", "Secondary", SERIF, 600),
            t("text", "Text", SANS, 400), t("accent", "Accent", SANS, 600),
        ],
        "custom_typography": [],
        "default_generic_fonts": "Sans-serif",
        "body_background_background": "classic", "body_background_color": SAND,
        "body_color": INK,
        **typo("body_typography", SANS, 16, 400),
        "link_normal_color": TEAL, "link_hover_color": TEAL_DK,
        "container_width": px(1240),
        "container_padding": dims(0),
        "space_between_widgets": gap(0),
        "page_title_selector": "h1.entry-title",
        "site_name": "Jennifer Malecki Psychologist",
        "site_description": "Psychologist in Mooloolaba, Sunshine Coast",
    }
    for h in ("h1", "h2", "h3", "h4", "h5", "h6"):
        kit[f"{h}_typography_typography"] = "custom"
        kit[f"{h}_typography_font_family"] = SERIF
        kit[f"{h}_typography_font_weight"] = "600"
        kit[f"{h}_color"] = INK
    return kit


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    out = {"header": build_header(), "footer": build_footer(), "home": build_home(), "kit": build_kit()}
    for name, data in out.items():
        path = DIST / f"{name}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        print(f"{path.name}: {path.stat().st_size} bytes")
