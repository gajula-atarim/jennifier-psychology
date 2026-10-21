"""Inner pages (About, Services, Fees & Rebates, For Referrers, Gallery) and their header.

Values come from the design exports in design/pages/. Shared helpers, colours and pop-ups come from
build.py, so every section stays an editable Elementor block in the same system as the Home page.

    python3 elementor/build_pages.py
"""
import json

from build import (BODY, BODY_DK, DIST, EMAIL, EMAIL_URL, INK, MIST, MIST_LT, MUTED, NAME_TITLE, OCHRE, PHONE,
                   PHONE_URL, AHPRA_REG, SAND, SANS, SERIF, STONE, TEAL, URL, border, button, container, dims,
                   eyebrow, gap, gradient, grid, heading, html, icon, icon_list, image, main_nav, media, modal, pop_text, px,
                   sand_bg, section, text, textlink, wave_card, widget)

PAGES = {"about": 50, "services": 51, "fees": 52, "referrers": 53, "gallery": 54,
         "resources": 67, "contact": 68, "support": 69, "privacy": 70}
INNER_HEADER = 55
GREY_BODY = "#3E5A66"
LINE = "#E2DCCD"


# ---------------------------------------------------------------- small building blocks

def h1(name, label, color=INK):
    return heading(name, label, "h1", SERIF, "clamp(42px, 5.4vw, 72px)", color, weight=600, lh=1.02, ls=-0.01)


def h2(name, label, size="clamp(34px, 4vw, 52px)", color=INK, lh=1.08, **kw):
    return heading(name, label, "h2", SERIF, size, color, weight=600, lh=lh, ls=-0.01, **kw)


def h3(name, label, size=30, color=INK, lh=1.12, **kw):
    return heading(name, label, "h3", SERIF, size, color, weight=600, lh=lh, ls=-0.01, **kw)


def para(name, html_, size=17, color=GREY_BODY, lh=1.75, **kw):
    return text(name, html_ if html_.startswith("<") else f"<p>{html_}</p>", size, color, lh=lh, **kw)


def call_email(name, email_label="Email Jennifer", call_style="primary", email_style="ghost", center=False):
    return container(name, [
        button(f"{name}-call", f"Call {PHONE}", PHONE_URL, call_style),
        button(f"{name}-email", email_label, EMAIL_URL, email_style),
    ], row=True, wrap=True, gap_=12, justify="center" if center else None)


def more(name, label, target):
    """Outline pill with a plus, opening a pop-up (the design's ".more" button)."""
    return button(name, label, target, "ghost", text_padding=dims(13, 18), border_width=dims(1.5),
                  selected_icon={"value": {"url": "https://jennifermalecki.wsdfy.com/wp-content/uploads/2026/10/"
                                           "jm-icon-plus.svg", "id": 40}, "library": "svg"},
                  icon_align="row-reverse", icon_indent=px(8), cls="jm-more",
                  typography_font_size=px(15))


def figure(name, key, caption, cls, *, cap_pos="bottom-center"):
    """Artwork in a shaped frame with the copyright caption over it (shape via cls in jm-site.css)."""
    return container(name, [
        image(f"{name}-img", key, cls="jm-figure-img"),
        heading(f"{name}-cap", caption, "p", SANS, 13, SAND, lh=1.2, cls=f"jm-fig-cap jm-fig-cap-{cap_pos}"),
    ], cls=f"jm-figure {cls}")


def page_hero(name, left, right=None, *, bg=STONE, cls="", pad=None):
    kids = [container(f"{name}-text", left, gap_=20, width=560, grow=999)]
    if right is not None:
        kids.append(right)
    return section(name, kids, pad=pad or dims("clamp(56px,7vw,96px)", 24, "clamp(96px,10vw,140px)", 24), bg=bg,
                   row=True, wrap=True, gap_=gap(48, 64), align="center", cls=f"jm-page-hero {cls}".strip())


def sand_cta(name, title, body, *, email_label="Email Jennifer", stone_above=False, center=True, kids=None):
    inner = kids or [
        h2(f"{name}-h", title, size="clamp(34px, 4.2vw, 52px)", lh=1.06, align="center"),
        para(f"{name}-p", body, 18, BODY_DK, 1.7, align="center"),
        call_email(f"{name}-btns", email_label, center=True),
    ]
    box = container(f"{name}-inner", inner, gap_=20, align="center" if center else None, width=820, grow=0,
                    _flex_align_self="center")
    return section(name, [box], pad=dims("clamp(96px,10vw,136px)", 24, "clamp(72px,8vw,112px)", 24),
                   cls="jm-cta jm-page-cta" + (" jm-cta-stone" if stone_above else ""), **sand_bg())


def label_value(name, label, value, last=False):
    return container(name, [
        heading(f"{name}-l", label, "p", SANS, 12, TEAL, weight=600, lh=1.3, ls=0.12, transform="uppercase"),
        text(f"{name}-v", f"<p>{value}</p>", 16, INK, lh=1.5),
    ], gap_=2, pad=dims(0, 0, 0 if last else 10, 0),
        **({} if last else {"border_border": "solid", "border_width": dims(0, 0, 1, 0), "border_color": LINE}))


def pop(mid, title, paras, extra=None):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return modal(mid, title, [pop_text(f"{mid}-body", body), *(extra or [])])


def icon_circle(name, key, size=26, pad_=15):
    return icon(name, key, size, view="stacked", shape="circle", primary_color=TEAL, secondary_color="#ffffff",
                icon_padding=px(pad_), _flex_size="none")


# ---------------------------------------------------------------- inner-page header

def build_inner_header():
    crisis = container("ih-crisis", [
        text("ih-crisis-left", '<p><strong class="jm-urgent">Need urgent help?</strong><span>Emergency '
                               '<a href="tel:000">000</a></span><span>Lifeline <a href="tel:131114">13 11 14</a>'
                               f'</span><a href="{URL["support"]}">All support lines →</a></p>',
             14, SAND, lh=1.4, cls="jm-crisis-line", _flex_size="shrink"),
        icon_list("ih-crisis-right", [(PHONE, PHONE_URL), (EMAIL, EMAIL_URL)], inline=True, size=14, color="#ffffff",
                  hover=OCHRE, weight=600, lh=1.4, space=20, hide_mobile="hidden-mobile", _flex_size="none"),
    ], boxed=True, row=True, wrap=True, justify="space-between", align="center", gap_=gap(6, 24),
        pad=dims(10, 24), cls="jm-topbar jm-inner-topbar", background_background="classic", background_color=TEAL)

    bar = container("ih-bar", [
        image("ih-logo", "logo_dark", height=72, url=URL["home"], _flex_size="none", cls="jm-inner-logo",
              height_mobile=px(56)),
        container("ih-actions", [
            html("ih-buttons", f'<div class="jm-rounds"><a class="jm-round" href="{PHONE_URL}" aria-label="Call {PHONE}">'
                           '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                           '</div>'),
            main_nav("ih-nav"),
        ], row=True, align="center", gap_=10, flex_wrap="nowrap", flex_wrap_mobile="nowrap", grow=0,
            cls="jm-inner-actions"),
    ], boxed=True, row=True, justify="space-between", align="center", gap_=16, pad=dims(10, 24),
        flex_wrap="nowrap", flex_wrap_mobile="nowrap", cls="jm-inner-bar",
        background_background="classic", background_color="rgba(247,245,239,0.94)",
        border_border="solid", border_width=dims(0, 0, 1, 0), border_color=LINE)

    return [crisis, bar]


# ---------------------------------------------------------------- About

AREAS = ["Alcohol Use", "Anger Management", "Anxiety", "Behavioural Issues", "Bipolar Disorder", "Body Image",
         "Depression", "Dissociative Disorders (DID)", "Domestic Violence", "Drug Abuse", "Emotional Disturbance",
         "Grief", "Impulse Control Disorders", "Mood Disorders", "Narcissistic Personality (NPD)",
         "Personality Disorders", "Psychosis", "Self-Harming", "Sexual Abuse", "Suicidal Ideation",
         "Thinking Disorders", "Veterans"]


def about_page():
    hero = page_hero("ab-hero", [
        eyebrow("ab-eyebrow", "About", color=MIST),
        h1("ab-h1", NAME_TITLE, color="#ffffff"),
        heading("ab-role", "Principal Psychologist | AAPi (General Psychologist)", "p", SANS, 18, OCHRE, weight=600,
                lh=1.4),
        para("ab-lede", "I invite you to reach out by email or phone for a confidential chat. I am here to listen and "
                        "support your next step.", "clamp(17px, 1.4vw, 19px)", SAND, 1.7, maxw=640),
        call_email("ab-hero-btns", call_style="ochre", email_style="light"),
    ])
    photo_hero(hero, "hero_poster", "center 60%")

    practice = section("ab-practice", [
        container("ab-practice-head", [eyebrow("ab-practice-eyebrow", "The practice"),
                                       h2("ab-practice-h", "About the Practice")], gap_=14, width=300, grow=1),
        container("ab-practice-body", [
            para("ab-practice-p1", "The clinic is located in the heart of Mooloolaba, where I offer a high-quality, "
                                   "personalised approach to mental health care. You will receive active, one-to-one "
                                   "care from an experienced psychologist dedicated to assessing and treating a range of "
                                   "mental health concerns, including PTSD, depression, anxiety, personality dynamics, "
                                   "and eating disorders.", 19, BODY_DK, 1.8),
            para("ab-practice-p2", "I treat adults from all walks of life. I have also published research on how early "
                                   "life experiences affect our experience of the body.", 17, GREY_BODY, 1.8),
            para("ab-practice-p3", "My goal is to assist you to make sense of the origins of your difficulties, helping "
                                   "you build practical skills and make the changes needed to work towards a more "
                                   "meaningful life.", 17, GREY_BODY, 1.8),
            container("ab-practice-more", [more("ab-qual", "Qualifications &amp; registration", "#jm-pop-qual"),
                                           more("ab-research", "Research &amp; publications", "#jm-pop-research")],
                      row=True, wrap=True, gap_=10, pad=dims(6, 0, 0, 0)),
        ], gap_=18, width=600, grow=999),
    ], pad=dims("clamp(56px,7vw,96px)", 24), row=True, wrap=True, gap_=gap(32, 64), cls="jm-tide")

    stops = [("01", "Schema Therapy", "Patterns, origins and root emotional wounds"),
             ("02", "Cognitive Behavioural Therapy (CBT)", "Thoughts, feelings and behaviours"),
             ("03", "Dialectical Behaviour Therapy (DBT)", "Mindfulness, emotional regulation and distress tolerance"),
             ("04", "Body mapping", "Arts-based, embodied exploration of the self")]
    stop_els = [container(f"ab-stop-{n}", [
        heading(f"ab-stone-{n}", n, "span", SERIF, 20, TEAL, weight=700, lh=1, cls="jm-stone", _flex_size="none"),
        container(f"ab-stop-text-{n}", [
            heading(f"ab-stop-name-{n}", name, "span", SANS, 17, INK, weight=600, lh=1.25),
            heading(f"ab-stop-sub-{n}", sub, "span", SANS, 14, GREY_BODY, lh=1.35),
        ], gap_=2, grow=1, width=px(0, "%"), mobile_width=False),
        icon(f"ab-stop-arrow-{n}", "i_arrow", 18, cls="jm-stop-arrow", _flex_size="none"),
    ], row=True, align="center", gap_=16, pad=dims(6, 14, 6, 0), tag="a", link={"url": URL["services"]},
        cls="jm-stop", min_height=px(72), border_radius=dims(16), flex_wrap="nowrap", flex_wrap_mobile="nowrap")
        for n, name, sub in stops]
    approach_art = container("ab-app-art", [
        figure("ab-app-fig", "art_wave", "Original artwork © Jennifer Malecki", "jm-ar-45 jm-arch-wide",
               cap_pos="top-center"),
        heading("ab-app-quote", "“I aim to look beyond symptoms, asking holistic questions to understand your whole "
                                "story.”", "p", SERIF, "clamp(20px, 1.9vw, 25px)", SAND, weight=500, lh=1.3,
                style="italic", cls="jm-quote-card"),
    ], width=380, grow=1, cls="jm-quote-wrap", _element_custom_width=px(500))
    approach = section("ab-approach", [
        approach_art,
        container("ab-app-text", [
            eyebrow("ab-app-eyebrow", "How I work"),
            h2("ab-app-h", "About My Approach", size="clamp(36px, 4.2vw, 56px)", lh=1.05),
            para("ab-app-p", "I use a range of evidence-based therapies to support clients on their journey towards "
                             "healing and personal growth. My approach incorporates Schema Therapy, Cognitive "
                             "Behavioural Therapy (CBT), and Dialectical Behaviour Therapy (DBT). I aim to look beyond "
                             "symptoms, asking holistic questions to understand your whole story and help you truly "
                             "reclaim your life.", 17, GREY_BODY, 1.8),
            container("ab-app-path", stop_els, cls="jm-care-list jm-care-stone"),
            container("ab-app-note", [
                icon("ab-app-note-icon", "i_palette", 34, color=TEAL, _flex_size="none"),
                para("ab-app-note-p", "To enrich the therapeutic process, you may choose to integrate arts-based "
                                      "techniques into your sessions. Body mapping is used to explore and express "
                                      "aspects of the self, supporting your therapy goals and fostering deep healing.",
                     16, BODY_DK, 1.75),
            ], row=True, gap_=16, align="flex-start", pad=dims(24, 26), border_radius=dims(22),
                flex_wrap="nowrap", flex_wrap_mobile="nowrap", **sand_bg()),
        ], gap_=20, width=520, grow=999),
    ], pad=dims("clamp(64px,8vw,112px)", 24), bg=STONE, row=True, wrap=True, gap_=gap(48, 72), align="center",
        cls="jm-tide")

    areas = section("ab-areas", [
        container("ab-areas-head", [
            eyebrow("ab-areas-eyebrow", "What I can help with", color=MIST),
            h2("ab-areas-h", "Practice Areas", size="clamp(36px, 4.2vw, 56px)", color="#ffffff", lh=1.05),
            para("ab-areas-p", "I treat adults from all walks of life.", 17, MIST_LT, 1.75),
            heading("ab-areas-num", "22", "p", SERIF, "clamp(64px, 7vw, 96px)", OCHRE, weight=700, lh=1),
            heading("ab-areas-num-l", "Areas of practice", "p", SANS, 14, MIST, weight=600, lh=1.2, ls=0.12,
                    transform="uppercase", _margin=dims(-8, 0, 0, 0)),
            call_email("ab-areas-btns", call_style="ochre", email_style="light"),
        ], gap_=16, width=300, grow=1),
        icon_list("ab-areas-list", [(a, None, "i_wave_mini") for a in AREAS], size=17, color=SAND, weight=500, lh=1.3,
                  icon_size=22, icon_color=OCHRE, cls="jm-areas", _element_width="initial",
                  _element_custom_width=px(620), _flex_size="custom", _flex_grow=999, _flex_shrink=1),
    ], pad=dims("clamp(64px,8vw,112px)", 24), bg=TEAL, row=True, wrap=True, gap_=gap(40, 64), align="flex-start",
        cls="jm-gp jm-areas-section")

    day = lambda n, label, title, sub, key, mon=False: container(f"ab-day-{n}", [
        heading(f"ab-day-{n}-d", label, "p", SANS, 13, INK if mon else MIST, weight=700, ls=0.12, transform="uppercase"),
        icon(f"ab-day-{n}-i", key, 26, color=INK if mon else "#ffffff"),
        heading(f"ab-day-{n}-t", title, "p", SERIF, 24, INK if mon else "#ffffff", weight=700, lh=1.1),
        heading(f"ab-day-{n}-s", sub, "p", SANS, 14, INK if mon else MIST_LT, lh=1.3),
    ], gap_=8, pad=dims(20), justify="space-between", min_height=px(150), border_radius=dims(22),
        background_background="classic", background_color=OCHRE if mon else TEAL)
    days = [day("mon", "Monday", "Face-to-face", "In-Clinic", "i_map_pin", True)] + [
        day(d.lower(), d, "Telehealth", "Online", "i_monitor") for d in ("Tuesday", "Wednesday", "Thursday", "Friday")]

    in_person = container("ab-inperson", [
        container("ab-inperson-cap", [
            heading("ab-inperson-h", "In person at Mooloolaba", "p", SERIF, 28, INK, weight=600, lh=1.15),
            text("ab-inperson-a", "<p>Unit 1, 38 Burnett Street, Mooloolaba QLD 4557</p>", 15, GREY_BODY, lh=1.5),
        ], gap_=4, pad=dims(20, 22), border_radius=dims(20), background_background="classic",
            background_color="rgba(247,245,239,0.94)"),
    ], width=320, grow=1, min_height=px(360), justify="flex-end", pad=dims(16), border_radius=dims(28),
        overflow="hidden", cls="jm-photo-card", background_background="classic",
        background_image={"url": "https://jennifermalecki.wsdfy.com/wp-content/uploads/2026/10/"
                                 "jm-photo-point-cartwright.jpg", "id": 48},
        background_position="center center", background_size="cover", background_repeat="no-repeat")
    telehealth = wave_card("ab-tele", [
        icon_circle("ab-tele-i", "i_monitor"),
        h3("ab-tele-h", "Telehealth", size="clamp(28px, 3vw, 38px)", lh=1.1),
        para("ab-tele-p", "Telehealth allows clients to access psychological support from the comfort and privacy of "
                          "their own home, reducing travel time and increasing accessibility for individuals with busy "
                          "schedules, health concerns, caregiving responsibilities, or those living in rural and "
                          "regional areas.", 17, GREY_BODY, 1.8),
    ], radius=28, pad=dims("clamp(28px,3.4vw,44px)", "clamp(28px,3.4vw,44px)", 120, "clamp(28px,3.4vw,44px)"),
        gap_=16, hover=False)
    telehealth["settings"].update({"width": px(480), "_flex_size": "custom", "_flex_grow": 999, "_flex_shrink": 1,
                                   "width_mobile": px(100, "%")})

    week = section("ab-week", [
        container("ab-week-head", [
            container("ab-week-head-text", [
                eyebrow("ab-week-eyebrow", "Your week"),
                h2("ab-week-h", "In person and by Telehealth"),
                para("ab-week-p", "I offer therapy sessions by Telehealth and in person at Mooloolaba in a supportive "
                                  "environment.", 17, GREY_BODY, 1.75),
            ], gap_=12, width=720, grow=0),
            heading("ab-week-appt", "By Appointment Only", "p", SANS, 15, TEAL, weight=600, lh=1.2,
                    cls="jm-appt-pill", _flex_size="none"),
        ], row=True, wrap=True, justify="space-between", align="flex-end", gap_=gap(14, 40)),
        grid("ab-days", days, 170, 12),
        container("ab-week-cards", [in_person, telehealth], row=True, wrap=True, gap_=20, align="stretch"),
    ], pad=dims("clamp(64px,8vw,112px)", 24, "clamp(64px,8vw,112px)", 24), gap_=28, cls="jm-tide")

    next_ = sand_cta("ab-next", "", "", kids=[
        eyebrow("ab-next-eyebrow", "Your next step"),
        h2("ab-next-h", "What Next", size="clamp(36px, 4.4vw, 58px)", lh=1.06),
        para("ab-next-p1", "In our initial sessions, we will work collaboratively to understand your unique needs and "
                           "establish clear, meaningful treatment goals. Together, we will map out a personalised "
                           "treatment plan—drawing on evidence-based therapies and embodied insights—to serve as a "
                           "clear roadmap guiding our way forward on your journey to healing.", 18, BODY_DK, 1.8),
        para("ab-next-p2", "Your therapeutic timeline is flexible and uniquely tailored to your pace and clinical needs. "
                           "If you are accessing care under a Medicare Mental Health Care Plan, we will structure our "
                           "initial timing around your allocated subsidised sessions, regularly reviewing your goals "
                           "together to ensure your plan continues to support your ongoing healing.", 17, "#33475A",
             1.8),
        call_email("ab-next-btns"),
    ], center=False)
    next_["elements"][0]["settings"]["width"] = px(880)

    qual = modal("jm-pop-qual", "Qualifications &amp; registration", [pop_text("qual-body", (
        "<h3>Qualifications</h3><p>Bachelor of Social Science (Psychology)<br>Bachelor of Arts Honours (Psychology)"
        "<br>Doctor of Philosophy (PhD)</p>"
        "<h3>Registration</h3><p>General Psychologist, Psychology Board of Australia (AHPRA)<br>"
        f"AHPRA {AHPRA_REG}</p>"
        "<h3>Membership</h3><p>Australian Association of Psychologists Inc. (AAPi)</p>"
        "<h3>Medicare</h3><p>Provider No. 1894363H</p>"))])
    links = [("Google Scholar", "https://scholar.google.com/citations?user=Icxwr4UAAAAJ&hl=en"),
             ("Psychology Today", "https://www.psychologytoday.com/au/counselling/jennifer-malecki-assoc-pty-ltd-"
                                  "mooloolaba-qld/1722996"),
             ("Trauma Support directory", "https://www.traumasupport.com.au/practitioner-directory/practitioner/"
                                          "jennifer-malecki/"),
             ("Sphere in the Know", "https://www.sphereintheknow.com/jennifer-malecki"),
             ("AAPi Find a Psychologist", "https://www.aapi.org.au/Web/Shared_Content/Smart-Suite/Smart-Maps/Public/"
                                          "Find_a_Psychologist_Profile.aspx?Practice=8094"),
             ("LinkedIn", "https://www.linkedin.com/in/jennifer-malecki-97749095/")]
    research = modal("jm-pop-research", "Research &amp; publications", [
        pop_text("research-p", "<p>I have also published research on how early life experiences affect our experience "
                               "of the body.</p>"),
        icon_list("research-links", [(f'{t}<span aria-hidden="true">↗</span>', u) for t, u in links], size=15,
                  color=TEAL, hover="#ffffff", weight=600, lh=1.2, cls="jm-link-pills"),
    ])
    for row in research["elements"][0]["elements"][-1]["settings"]["icon_list"]:
        row["link"]["is_external"] = "on"
        row["link"]["nofollow"] = ""
    return [hero, practice, approach, areas, week, next_, qual, research]


# ---------------------------------------------------------------- Services

THERAPIES = [
    ("trauma", "01", "Trauma Focused Therapy",
     "Trauma can deeply disrupt your sense of safety, leaving your mind and body stuck in a constant state of survival.",
     ["Trauma can deeply disrupt your sense of safety, leaving your mind and body stuck in a constant state of "
      "survival. Together, we work at a pace that feels safe for you to gently process these overwhelming past "
      "experiences, helping you resolve the root causes of distress so you can reconnect with yourself and move "
      "forward."]),
    ("schema", "02", "Schema therapy",
     "When we experience complex stress or trauma early in life, we often develop deep, rigid patterns of thinking and "
     "feeling—called 'schemas'—to help us cope.",
     ["When we experience complex stress or trauma early in life, we often develop deep, rigid patterns of thinking "
      "and feeling—called 'schemas'—to help us cope. While these patterns protected us back then, they can leave us "
      "feeling stuck in repetitive loops of anxiety, self-doubt, or relationship difficulties as adults. Schema therapy "
      "goes beneath surface-level symptom management. Together, we work to identify these underlying patterns, "
      "understand their origins, and heal the root emotional wounds so you can break free from old cycles and build a "
      "healthier, more fulfilling life."]),
    ("dbt", "03", "Dialectical Behaviour Therapy (DBT)",
     "When emotions feel overwhelmingly intense, it can be incredibly difficult to find your footing or navigate daily "
     "life.",
     ["When emotions feel overwhelmingly intense, it can be incredibly difficult to find your footing or navigate daily "
      "life. Dialectical Behaviour Therapy (DBT) is a practical, skills-based approach designed to help you regain your "
      "balance. The word 'dialectical' simply means balancing two opposite truths: accepting yourself exactly as you "
      "are right now, while actively working to change the patterns that cause you pain. Together, we focus on "
      "building practical tools for mindfulness, emotional regulation, and distress tolerance, empowering you to "
      "navigate life’s challenges safely and with greater confidence."]),
    ("cbt", "04", "Cognitive Behavioural Therapy (CBT)",
     "Cognitive Behavioural Therapy (CBT) is a foundational, evidence-based approach that helps us look at the "
     "practical connections between our thoughts, feelings, and behaviours.",
     ["Cognitive Behavioural Therapy (CBT) is a foundational, evidence-based approach that helps us look at the "
      "practical connections between our thoughts, feelings, and behaviours. While standard CBT is excellent for "
      "identifying immediate habits and learning day-to-day symptom management, I view it as an entry point rather than "
      "the final destination. In our sessions, we utilize these practical behavioural skills as a stable baseline, "
      "allowing us to safely step deeper into holistic frameworks—like schema therapy and body mapping—to resolve the "
      "underlying roots of complex trauma."]),
]


def services_page():
    hero = page_hero("sv-hero", [
        eyebrow("sv-eyebrow", "Services", color=MIST),
        h1("sv-h1", "What I do", color="#ffffff"),
        para("sv-lede", "I use a range of evidence-based therapies to support clients in their journey towards healing "
                        "and personal growth. My approach incorporates schema therapy, cognitive behavioural therapy "
                        "(CBT), and dialectical behaviour therapy (DBT). I aim to look beyond symptoms, asking holistic "
                        "questions to understand your whole story and help you truly reclaim your life.",
             "clamp(17px, 1.4vw, 19px)", SAND, 1.75, maxw=760),
        call_email("sv-hero-btns", call_style="ochre", email_style="light"),
    ])
    photo_hero(hero, "hero_poster", "center 35%")

    cards = [wave_card(f"sv-card-{key}", [
        heading(f"sv-num-{key}", num, "span", SERIF, 34, "#6A8CA3", weight=600, lh=1),
        h3(f"sv-h-{key}", title, size=23, lh=1.2),
        para(f"sv-p-{key}", short, 15, GREY_BODY, 1.6),
        more(f"sv-more-{key}", "Read more", f"#jm-pop-{key}"),
    ], radius=20, pad=dims(24, 24, 72, 24), gap_=10, size="sm") for key, num, title, short, _ in THERAPIES]
    for c in cards:
        c["settings"]["css_classes"] += " jm-ther-card"
    therapies = section("sv-ther", [
        container("sv-ther-head", [
            eyebrow("sv-ther-eyebrow", "Therapies"),
            h2("sv-ther-h", "Evidence-based therapies"),
            para("sv-ther-p", "To enrich the therapeutic process, you may choose to integrate arts-based techniques into "
                              "therapy. Body mapping is used to explore and express aspects of the self, enhancing "
                              "treatment outcomes and supporting healing.", 17, GREY_BODY, 1.75),
        ], gap_=14, width=700, grow=0),
        grid("sv-ther-grid", cards, 240, 16, grid_columns_grid=px("repeat(4, minmax(0, 1fr))"),
             grid_columns_grid_tablet=px("repeat(2, minmax(0, 1fr))"),
             grid_columns_grid_mobile={"unit": "fr", "size": 1, "sizes": []}),
    ], pad=dims("clamp(56px,7vw,96px)", 24), gap_=36, cls="jm-tide")

    body_map = section("sv-bm", [
        container("sv-bm-art", [figure("sv-bm-fig", "art_ocean", "Original artwork © Jennifer Malecki",
                                       "jm-ar-45 jm-r28", cap_pos="bottom-left")], width=340, grow=1,
                  cls="jm-fig-col jm-fig-col-460"),
        container("sv-bm-text", [
            eyebrow("sv-bm-eyebrow", "05 · Arts-based practice", color=MIST),
            h2("sv-bm-h", "Body Mapping &amp; Embodied Practice", color="#ffffff"),
            para("sv-bm-p", "My trauma-informed practice recognises that complex stress lives in both the mind and the "
                            "body. By moving beyond traditional talk therapy, we utilise embodied practices like body "
                            "mapping—tracing an outline of the body to create a life-sized map representing aspects of "
                            "your unique lived experiences—safely allowing your story to be visually shared and "
                            "understood.", 18, MIST_LT, 1.8),
            textlink("sv-bm-more", "About body mapping", "#jm-pop-bodymap", arrow=True, button_text_color=OCHRE,
                     hover_color="#E8BE57"),
        ], gap_=18, width=520, grow=999),
    ], pad=dims("clamp(56px,7vw,96px)", 24), bg=TEAL, row=True, wrap=True, gap_=gap(40, 64), align="center",
        cls="jm-tide")

    sess_card = lambda n, d, t, s: container(f"sv-sess-{n}", [
        eyebrow(f"sv-sess-{n}-d", d, ls=0.12),
        h3(f"sv-sess-{n}-t", t, size=26, lh=1.15),
        para(f"sv-sess-{n}-s", s, 15, GREY_BODY, 1.5),
    ], gap_=8, pad=dims(26), background_background="classic", background_color="#ffffff",
        **border(1, LINE, 20))
    sessions = section("sv-sess", [
        h2("sv-sess-h", "How sessions are offered", size="clamp(30px, 3.4vw, 44px)", lh=1.1),
        grid("sv-sess-grid", [sess_card("mon", "Monday", "Face-to-face Consultations (In-Clinic)",
                                        "Unit 1, 38 Burnett Street, Mooloolaba"),
                              sess_card("tue", "Tuesday – Friday", "Telehealth Consultations (Online)",
                                        "By Appointment Only")], 280, 16),
    ], pad=dims("clamp(56px,7vw,96px)", 24), gap_=28, cls="jm-tide")

    cta = sand_cta("sv-cta", "I am here to listen and support your next step",
                   "I invite you to reach out by email or phone for a chat.")
    pops = [pop(f"jm-pop-{key}", title, long) for key, _, title, _, long in THERAPIES]
    from build import bodymap_modal
    return [hero, therapies, body_map, sessions, cta, *pops, bodymap_modal()]


# ---------------------------------------------------------------- Fees & Rebates

def fees_page():
    rebate = wave_card("fe-rebate", [
        heading("fe-rebate-l", "Current Medicare Rebates (2026/2027)", "p", SANS, 13, MIST, weight=600, ls=0.14,
                transform="uppercase", lh=1.3),
        heading("fe-rebate-v", "$101.55", "p", SERIF, "clamp(56px, 6vw, 80px)", "#ffffff", weight=700, lh=1),
        heading("fe-rebate-s", "Medicare Rebate per session", "p", SANS, 17, MIST_LT, lh=1.4),
        para("fe-rebate-n", "For up to 10 sessions per calendar year with a valid Mental Health Care Plan.", 14,
             MUTED, 1.6),
    ], radius=28, pad=dims(36, 36, 110, 36), gap_=10, hover=False)
    rebate["settings"].update({"background_background": "classic", "background_color": TEAL,
                               "border_border": "none", "width": px(340), "_flex_size": "custom",
                               "_flex_grow": 1, "_flex_shrink": 1, "width_mobile": px(100, "%"),
                               "css_classes": rebate["settings"]["css_classes"] + " jm-rebate-card"})
    hero = page_hero("fe-hero", [
        eyebrow("fe-eyebrow", "Fees &amp; Rebates", color=MIST),
        h1("fe-h1", "Fees &amp; Rebates", color="#ffffff"),
        para("fe-lede", "Sessions are charged at a standard consultation rate. If you have a valid Mental Health Care "
                        "Plan from your GP, you will be eligible to claim a Medicare rebate per session (for up to 10 "
                        "sessions per calendar year).", "clamp(17px, 1.4vw, 19px)", SAND, 1.75, maxw=680),
    ], rebate)
    photo_hero(hero, "photo_beach", "center 60%")

    card = lambda n, key, title, kids: wave_card(f"fe-card-{n}", [
        icon(f"fe-card-{n}-i", key, 36, color=TEAL), h3(f"fe-card-{n}-h", title), *kids,
    ], radius=24, pad=dims(32, 32, 116, 32), gap_=14)
    pay = section("fe-pay", [grid("fe-pay-grid", [
        card("pay", "i_card", "Accepted Payment Methods", [
            icon_list("fe-pay-list", ["Bank Transfer (Electronic Funds Transfer)", "Mastercard", "Visa"], inline=True,
                      size=15, weight=500, lh=1.3, cls="jm-chips jm-chips-left jm-chips-outline")]),
        card("phi", "i_shield", "Private Health Insurance", [
            para("fe-phi-p", "Once your invoice is settled, we will issue a formal receipt so you can claim your private "
                             "health insurance rebate directly with your fund. (Please note: Health insurance funds "
                             "generally do not cover cancellation fees).", 16, GREY_BODY, 1.7)]),
        card("change", "i_calendar", "Changing Your Appointment", [
            para("fe-change-p", "Your session time is reserved exclusively for you.", 16, GREY_BODY, 1.7),
            more("fe-change-more", "Cancellation policy", "#jm-pop-cancel")]),
    ], 340, 20)], pad=dims("clamp(56px,7vw,96px)", 24), cls="jm-tide")

    way = lambda n, title, sub, target=None: wave_card(f"fe-way-{n}", [
        heading(f"fe-way-{n}-h", title, "p", SERIF, 26, INK, weight=600, lh=1.15),
        para(f"fe-way-{n}-s", sub, 15, GREY_BODY, 1.5),
        *([textlink(f"fe-way-{n}-more", "Details +", target, text_padding=dims(4, 0), typography_font_size=px(14))]
          if target else []),
    ], radius=20, pad=dims(26, 26, 76, 26), gap_=8, size="sm")
    ways = section("fe-ways", [
        container("fe-ways-head", [
            eyebrow("fe-ways-eyebrow", "Referrals &amp; plans"),
            h2("fe-ways-h", "Ways to access care"),
            para("fe-ways-p", "I can provide services using Medicare Health Care Plan, ED Plan, DVA or NDIS Plan and "
                              "supply receipts for clients who wish to claim rebates from private health.", 17,
                 GREY_BODY, 1.75),
        ], gap_=14, width=720, grow=0),
        grid("fe-ways-grid", [way("medicare", "Medicare", "Mental Health Care Plans", "#jm-pop-medicare"),
                              way("ed", "ED Plan", "Eating Disorder Plan"),
                              way("dva", "DVA &amp; Open Arms", "Veterans and their families", "#jm-pop-dva-fees"),
                              way("ndis", "NDIS", "Self-managed and plan-managed participants"),
                              way("private", "Private clients", "No referral needed; claim through your extras cover")],
             220, 16),
    ], pad=dims("clamp(56px,7vw,96px)", 24), bg=STONE, gap_=32, cls="jm-tide")

    cta = sand_cta("fe-cta", "Questions about fees or rebates?",
                   "Feel free to reach out by email or phone to ask any questions or to discuss taking the next step "
                   "toward your healing.", stone_above=True)

    open_arms = container("dva-openarms", [
        heading("dva-oa-l", "Open Arms – Veterans &amp; Families Counselling", "p", SANS, 13, MIST, weight=600, ls=0.12,
                transform="uppercase", lh=1.3),
        text("dva-oa-p", "<p>An additional or after-hours resource for veterans and their families.</p>", 16,
             MIST_LT, lh=1.6),
        text("dva-oa-n", '<p><a href="tel:1800011046">1800 011 046</a></p>', 24, "#ffffff", weight=700, lh=1.2,
             cls="jm-modal-bignum"),
    ], gap_=6, pad=dims(20, 22), border_radius=dims(16), background_background="classic", background_color=TEAL)
    pops = [
        pop("jm-pop-cancel", "Changing Your Appointment", [
            "Your session time is reserved exclusively for you. If you need to cancel or change your appointment, "
            "please provide at least 2 full business days' notice. Regrettably, cancellations made within this "
            "2-business-day window or on the day of the appointment will incur a cancellation fee."]),
        pop("jm-pop-medicare", "Medicare Rebates (Mental Health Care Plans)", [
            "To claim a Medicare rebate, you will need a valid Mental Health Care Plan (MHCP) and a referral letter from "
            "your GP or psychiatrist prior to your first session.",
            "Under this plan, eligible clients can receive a Medicare rebate for up to 10 individual psychology sessions "
            "per calendar year."],
            [pop_text("medicare-how", "<ul>"
                      "<li><strong>How it Works:</strong> You pay the session fee on the day, and the rebate is processed "
                      "directly back into your bank account via Medicare—usually within 3 days.</li>"
                      "<li><strong>Easy Payments:</strong> All payments are securely processed at the end of your session "
                      "using digital payment options.</li>"
                      "<li><strong>No Complex Forms:</strong> You don't need to fill out any compliance paperwork online. "
                      "We will sort out all the details together during our initial phone call or first session.</li>"
                      "</ul>")]),
        modal("jm-pop-dva-fees", "DVA (Department of Veterans' Affairs)", [
            pop_text("dva-fees-body", "<ul>"
                     "<li><strong>Accepted DVA Cards:</strong> We accept <strong>Gold</strong> and <strong>White</strong> "
                     "Veteran Cards, including treatment provided under <strong>Non-Liability Health Care (NLHC)</strong> "
                     "arrangements (which covers all mental health conditions for eligible current or former ADF members "
                     "who have served at least one day).</li>"
                     "<li><strong>No-Gap / Bulk Billing Policy:</strong> We bill DVA directly with <strong>no out-of-pocket "
                     "gap fees or co-payments</strong> for eligible services.</li>"
                     "<li><strong>Referral Requirements:</strong> We require a referral from your General Practitioner "
                     "(GP), psychiatrist, or medical specialist.</li>"
                     "<li><strong>Provider Registration Status:</strong> I am registered with Medicare under the "
                     "<strong>Better Access</strong> scheme as a psychologist (which is a statutory requirement for DVA "
                     "allied mental health services).</li>"
                     "</ul>"),
            open_arms]),
    ]
    return [hero, pay, ways, cta, *pops]


# ---------------------------------------------------------------- For Referrers

def referrers_page():
    details = container("rf-details", [
        h2("rf-details-h", "Referral details", size=30, lh=1.1),
        container("rf-dl", [
            label_value("rf-d-name", "Practitioner", NAME_TITLE),
            label_value("rf-d-prov", "Medicare Provider No.", "1894363H"),
            label_value("rf-d-ahpra", "AHPRA", AHPRA_REG),
            label_value("rf-d-mo", "Medical Objects", "[Medical Objects ID — to be supplied]"),
            label_value("rf-d-contact", "Phone / email", f'<a href="{PHONE_URL}">{PHONE}</a><br>'
                                                         f'<a href="{EMAIL_URL}">{EMAIL}</a>'),
            label_value("rf-d-addr", "Address", "Unit 1, 38 Burnett Street, Mooloolaba QLD 4557", last=True),
        ], gap_=12),
    ], gap_=16, pad=dims(32), width=340, grow=1, border_radius=dims(28), tag="aside", cls="jm-ref-details",
        background_background="classic", background_color=SAND)
    hero = page_hero("rf-hero", [
        heading("rf-pill", "Immediate room for new referrals · no wait time", "p", SANS, 14, INK, weight=700, lh=1.2,
                cls="jm-pill jm-pill-ochre"),
        eyebrow("rf-eyebrow", "For GPs &amp; referring practitioners", color=MIST),
        h1("rf-h1", "For Referrers", color="#ffffff"),
        para("rf-lede", "Jennifer values collaboration with referring professionals to ensure continuity of care and "
                        "coordinated treatment planning. Referrals are welcomed from GPs via Mental Health Care Plans, "
                        "as well as through private arrangements.", "clamp(17px, 1.4vw, 19px)", MIST_LT, 1.75),
        call_email("rf-hero-btns", "Email a referral", "ochre", "light"),
    ], details, bg=TEAL, cls="jm-gp jm-ref-hero")
    photo_hero(hero, "photo_cartwright", "center 22%")
    hero["settings"]["flex_align_items"] = "flex-start"

    tcard = lambda n, t, p: wave_card(f"rf-type-{n}", [h3(f"rf-type-{n}-h", t, size=28, lh=1.15),
                                                       para(f"rf-type-{n}-p", p, 16, GREY_BODY, 1.6)],
                                      radius=22, pad=dims(28, 28, 104, 28), gap_=8)
    types = section("rf-types", [
        container("rf-types-head", [
            eyebrow("rf-types-eyebrow", "Referral pathways"),
            h2("rf-types-h", "Referral Types Accepted"),
            para("rf-types-p", "She accepts referrals from your General Practitioner (GP) via Mental Health Care Plans, "
                               "NDIS referrals, and works with clients supported by the Department of Veterans' Affairs "
                               "(DVA). These can be made by phone or email.", 17, GREY_BODY, 1.75),
        ], gap_=14, width=760, grow=0),
        grid("rf-types-grid", [tcard("gp", "General Practitioner (GP)", "Mental Health Care Plan referrals."),
                               tcard("ndis", "NDIS", "Self-managed and plan-managed NDIS referrals."),
                               tcard("dva", "Department of Veterans' Affairs (DVA)",
                                     "Referrals supported for eligible veterans."),
                               tcard("mo", "Medical Objects", "Referrals can be made via Medical Objects.")], 260, 16),
    ], pad=dims("clamp(56px,7vw,96px)", 24), gap_=32, cls="jm-tide")

    step = lambda n, t, p: container(f"rf-step-{n}", [
        heading(f"rf-step-{n}-n", str(n), "span", SERIF, 20, "#ffffff", weight=700, lh=1, cls="jm-step-num",
                _flex_size="none"),
        container(f"rf-step-{n}-t", [h3(f"rf-step-{n}-h", t, size=24, lh=1.2),
                                     para(f"rf-step-{n}-p", p, 16, GREY_BODY, 1.5)], gap_=4, grow=1,
                  width=px(0, "%"), mobile_width=False),
    ], row=True, gap_=18, align="flex-start", pad=dims(22, 24), border_radius=dims(20), flex_wrap="nowrap",
        flex_wrap_mobile="nowrap", background_background="classic", background_color=SAND)
    delivery = section("rf-del", [
        container("rf-del-head", [
            eyebrow("rf-del-eyebrow", "Working together"),
            h2("rf-del-h", "Service Delivery"),
            para("rf-del-p", "Services are available in person at the Mooloolaba clinic and via secure telehealth for "
                             "clients across the Sunshine Coast and surrounding areas. Referrers receive timely updates "
                             "following assessment and at key review points.", 17, GREY_BODY, 1.75),
            more("rf-del-more", "Presentations I work with", "#jm-pop-areas"),
        ], gap_=16, width=320, grow=1),
        container("rf-del-steps", [step(1, "In-Person Therapy", "Available at our Mooloolaba clinic."),
                                   step(2, "Telehealth Services", "Secure online therapy for clients across the "
                                                                  "Sunshine Coast and surrounding areas."),
                                   step(3, "Referrer Communication", "Referrers receive timely updates following "
                                                                     "assessment and at key review points.")],
                  gap_=14, width=520, grow=999),
    ], pad=dims("clamp(56px,7vw,96px)", 24), bg=STONE, row=True, wrap=True, gap_=gap(32, 64), align="flex-start",
        cls="jm-tide")

    cta = sand_cta("rf-cta", "Make a referral", "Referrals can be made by phone or email, or via Medical Objects.",
                   email_label="Email a referral", stone_above=True)
    areas = modal("jm-pop-areas", "Practice Areas", [
        pop_text("areas-p", "<p>Extensive experience working with adults with PTSD, personality disorders, self-harming "
                            "behaviours, depression, bipolar disorder, anxiety, mood disorders, schizophrenia, and other "
                            "serious mental health conditions.</p>"),
        icon_list("areas-pills", AREAS, inline=True, size=15, weight=500, lh=1.3,
                  cls="jm-chips jm-chips-left jm-chips-outline"),
    ])
    areas["elements"][0]["settings"]["css_classes"] += " jm-modal-wide"
    return [hero, types, delivery, cta, areas]


# ---------------------------------------------------------------- Gallery

GALLERY = [
    ("art", "art_ocean", "[Artwork title]", "Acrylic, palette knife", "45"),
    ("coast", "photo_beach", "Mooloolaba", "Photograph", "43"),
    ("art", "art_wave", "[Artwork title]", "Acrylic, palette knife", "43"),
    ("coast", "photo_cartwright", "Point Cartwright", "Photograph", "45"),
    ("art", None, "[Artwork title]", "[Medium]", "11"),
    ("coast", None, "[Rainforest image]", "Photograph", "43"),
]


def gallery_page():
    filters = html("ga-filters", '<div class="jm-filters" role="group" aria-label="Filter gallery">'
                                 '<button type="button" class="jm-filter" data-filter="all" aria-pressed="true">All</button>'
                                 '<button type="button" class="jm-filter" data-filter="art" aria-pressed="false">Artworks</button>'
                                 '<button type="button" class="jm-filter" data-filter="coast" aria-pressed="false">Coast &amp; landscape</button>'
                                 '</div>')
    filters["settings"]["_flex_size"] = "none"
    hero = page_hero("ga-hero", [
        eyebrow("ga-eyebrow", "Gallery", color=MIST),
        h1("ga-h1", "Art, ocean &amp; the Sunshine Coast", color="#ffffff"),
        para("ga-lede", "Original artwork by Jennifer Malecki, alongside the beach and coastal landscapes of Mooloolaba. "
                        "Select any image to view it larger.", "clamp(17px, 1.4vw, 19px)", SAND, 1.7),
    ], filters, pad=dims("clamp(56px,7vw,96px)", 24, "clamp(96px,10vw,130px)", 24))
    hero["settings"].update({"flex_align_items": "flex-end", "flex_justify_content": "space-between",
                             "flex_gap": gap(24, 56)})
    hero["elements"][0]["settings"]["width"] = px(620)
    photo_hero(hero, "hero_poster", "center 70%")
    hero["elements"][0]["settings"]["flex_gap"] = gap(18)

    items = []
    for i, (cat, key, title, kind, ratio) in enumerate(GALLERY, 1):
        if key:
            media_el = image(f"ga-item-{i}-img", key, cls=f"jm-g-img jm-ar-{ratio}")
        else:
            media_el = heading(f"ga-item-{i}-ph", "[Artwork — to be supplied, max 1200 px wide, watermarked]"
                               if cat == "art" else "[Sunshine Coast hinterland or rainforest photo — to be supplied]",
                               "p", SANS, 15, TEAL, weight=600, lh=1.4, align="center",
                               cls=f"jm-g-placeholder jm-ar-{ratio}")
        items.append(container(f"ga-item-{i}", [
            media_el,
            container(f"ga-item-{i}-cap", [
                heading(f"ga-item-{i}-t", title, "p", SANS, 15, INK, weight=600, lh=1.5, cls="jm-g-title"),
                heading(f"ga-item-{i}-k", kind, "p", SANS, 15, GREY_BODY, lh=1.5, cls="jm-g-kind",
                        _flex_size="none"),
            ], row=True, justify="space-between", gap_=12, flex_wrap="nowrap", flex_wrap_mobile="nowrap"),
        ], gap_=12, cls=f"jm-g-item jm-g-{cat}"))
    grid_ = section("ga-grid", [grid("ga-grid-inner", items, 340, 24, grid_columns_grid=px(
        "repeat(auto-fill, minmax(min(340px, 100%), 1fr))"), css_classes="jm-gallery")], pad=dims("clamp(40px,5vw,72px)", 24, "clamp(56px,7vw,96px)", 24))
    cta = sand_cta("ga-cta", "", "", kids=[
        h2("ga-cta-h", "All images are protected by copyright", size="clamp(32px, 3.8vw, 48px)", align="center"),
        para("ga-cta-p", "Artworks and photographs on this website are © Jennifer Malecki and are shown at reduced "
                         "resolution with a watermark. They may not be copied, downloaded, reproduced or used in any "
                         "form without written permission.", 17, BODY_DK, 1.7, align="center"),
    ])
    return [hero, grid_, cta]


# ---------------------------------------------------------------- shared for the last four pages

CRISIS_LINES = [
    ("Lifeline", "24/7 crisis support and suicide prevention", "13 11 14", "131114"),
    ("Beyond Blue", "24/7 mental health information and advice", "1300 22 4636", "1300224636"),
    ("13YARN", "24/7 crisis support for Aboriginal and Torres Strait Islander people", "13 92 76", "139276"),
    ("Suicide Call Back Service", "24/7 telephone and online counselling", "1300 659 467", "1300659467"),
    ("DVConnect Womensline", "24/7 Queensland domestic violence and safety support", "1800 811 811", "1800811811"),
]
OPEN_ARMS = ("Open Arms – Veterans &amp; Families Counselling",
             "An additional or after-hours resource for veterans and their families.", "1800 011 046", "1800011046")
WHITE_CARD = dict(background_background="classic", background_color="#ffffff")


def link_box(name, kids, url, *, external=False, cls="", **kw):
    """A whole card that is one link (Elementor container rendered as <a>)."""
    return container(name, kids, tag="a", link={"url": url, "is_external": "on" if external else ""},
                     cls=cls, **kw)


def photo_hero(sec, key, pos="center center"):
    """Coastal photo behind an inner-page hero (the teal shade over it is in jm-site.css)."""
    sec["settings"].update({"background_background": "classic", "background_color": INK,
                            "background_image": media(key), "background_position": pos,
                            "background_size": "cover", "background_repeat": "no-repeat"})
    sec["settings"]["css_classes"] += " jm-hero-photo"
    return sec


def hero_text_only(name, kids, *, bg=STONE, maxw=None, pad=None):
    sec = section(name, [container(f"{name}-text", kids, gap_=18, **({"width": maxw, "grow": 0} if maxw else {}))],
                  pad=pad or dims("clamp(56px,7vw,96px)", 24, "clamp(96px,10vw,130px)", 24), bg=bg,
                  cls="jm-page-hero")
    return sec


# ---------------------------------------------------------------- Resources

RESOURCE_GROUPS = [
    ("trauma", "i_res_heart", "#DCE8EE", "Trauma &amp; Specialized Information", [
        ("Blue Knot Foundation", "National Centre of Excellence for Complex Trauma support and resources",
         "https://blueknot.org.au/"),
        ("The Butterfly Foundation", "National support and information for eating disorders and body image concerns",
         "https://butterfly.org.au/"),
        ("SANE Australia", "Resources, guidance, and peer support forums for complex mental health",
         "https://www.sane.org/")]),
    ("ground", "i_sprout", "#E6EFE6", "Grounding &amp; Mindfulness Tools", [
        ("Smiling Mind", "A free, Australian-developed mobile application offering evidence-based mindfulness "
                         "practices to help ground the nervous system.", "https://www.smilingmind.com.au/"),
        ("BeyondNow", "An interactive app created by Beyond Blue to help you easily build and keep a personal safety "
                      "plan on your phone for times of high distress.",
         "https://www.beyondblue.org.au/get-support/beyondnow-suicide-safety-planning")]),
    ("dissoc", "i_layers", "#E4E1EE", "Trauma &amp; Dissociation Support", [
        ("Phoenix Australia", "The National Centre for Excellence in Post-Traumatic Mental Health, providing "
                              "evidence-based recovery information for individuals experiencing PTSD.",
         "https://www.phoenixaustralia.org/")]),
    ("eating", "i_person", "#F4E6BF", "Eating Disorders &amp; Body Experience", [
        ("Eating Disorders Queensland (EDQ)", "A fantastic state-based organisation providing community support, "
                                              "resources, and hope for individuals living with eating disorders and "
                                              "their support networks.", "https://eatingdisordersqueensland.org.au/"),
        ("National Eating Disorders Collaboration (NEDC)", "A federally funded body offering clean, evidence-based "
                                                            "fact sheets about eating disorders.",
         "https://nedc.com.au/")]),
    ("complex", "i_signal", "#EBE7DB", "Complex Mental Health &amp; Personality Dynamics", [
        ("Project Air Strategy", "A universally respected Australian initiative providing high-quality personality "
                                 "disorder resources, fact sheets, and guidebooks for individuals and families.",
         "https://www.projectairstrategy.org/")]),
    ("apps", "i_smartphone", "#DDEBEF", "Practical Grounding Apps (Mind-Body Connection)", [
        ("The Tapping Solution App", "An introductory tool utilizing Emotional Freedom Techniques (EFT) that clients can "
                                     "use independently to explore somatic grounding and lower acute physiological "
                                     "stress.", "https://www.thetappingsolution.com/")]),
]
RES_FILTERS = [("all", "All"), ("trauma", "Trauma"), ("ground", "Grounding"), ("dissoc", "Dissociation"),
               ("eating", "Eating disorders"), ("complex", "Complex mental health"), ("apps", "Apps")]


def line_card(name, label, number, tel, *, ochre=False):
    return link_box(name, [
        text(f"{name}-l", f"<p>{label}</p>", 14, "#3A2C08" if ochre else GREY_BODY, lh=1.45),
        heading(f"{name}-n", number, "p", SANS, 26, INK, weight=700, lh=1.1),
    ], f"tel:{tel}", cls="jm-line", gap_=10, justify="space-between", min_height=px(120), pad=dims(20, 22),
        background_background="classic", background_color=OCHRE if ochre else "#ffffff",
        **border(1, OCHRE if ochre else LINE, 18))


def resources_page():
    hero = hero_text_only("rs-hero", [
        eyebrow("rs-eyebrow", "Resources", color=MIST),
        h1("rs-h1", "Resources", color="#ffffff"),
        para("rs-lede", "The informational resources and external links provided below are intended for educational "
                        "and support purposes only, and do not replace professional psychological care or medical "
                        "advice. If you or someone you know is in acute distress or experiencing an immediate safety "
                        "risk, please utilise the crisis contacts below or present to your nearest hospital emergency "
                        "department.", "clamp(17px, 1.4vw, 19px)", SAND, 1.75, maxw=860),
    ])
    photo_hero(hero, "photo_cartwright", "center 22%")

    lines = [line_card("rs-line-000", "Emergency Services · immediate danger or medical emergencies", "000", "000",
                       ochre=True)] + [
        line_card(f"rs-line-{tel}", f"{name} · {desc}", num, tel) for name, desc, num, tel in CRISIS_LINES]
    crisis = section("rs-crisis", [container("rs-crisis-panel", [
        container("rs-crisis-head", [
            h2("rs-crisis-h", "Immediate Crisis &amp; 24/7 Support", size="clamp(32px, 3.6vw, 46px)", color="#ffffff",
               lh=1.1),
            button("rs-crisis-btn", "Open the Support page", URL["support"], "ochre"),
        ], row=True, wrap=True, justify="space-between", align="flex-end", gap_=gap(16, 40)),
        grid("rs-crisis-grid", lines, 0, 12, grid_columns_grid=px("repeat(3, minmax(0, 1fr))"),
             grid_columns_grid_tablet=px("repeat(2, minmax(0, 1fr))"),
             grid_columns_grid_mobile={"unit": "fr", "size": 1, "sizes": []}),
    ], gap_=24, pad=dims("clamp(28px,4vw,48px)"), border_radius=dims(28), background_background="classic",
        background_color=INK)], pad=dims("clamp(40px,5vw,64px)", 24, 24, 24))

    cards = []
    for i, (key, ico, tint, title, rows) in enumerate(RESOURCE_GROUPS, 1):
        row_els = [link_box(f"rs-{key}-row-{j}", [
            container(f"rs-{key}-row-{j}-t", [
                heading(f"rs-{key}-row-{j}-n", n, "p", SANS, 17, INK, weight=700, lh=1.35),
                text(f"rs-{key}-row-{j}-d", f"<p>{d}</p>", 15, GREY_BODY, lh=1.6),
            ], gap_=3, grow=1, width=px(0, "%"), mobile_width=False),
            icon(f"rs-{key}-row-{j}-go", "i_up_right", 16, view="framed", shape="circle", primary_color=TEAL,
                 icon_padding=px(9), border_width=dims(1.5), cls="jm-res-go", _flex_size="none"),
        ], u, external=True, cls="jm-res-row", row=True, align="center", gap_=14, pad=dims(16, 18),
            flex_wrap="nowrap", flex_wrap_mobile="nowrap", background_background="classic",
            background_color="rgba(255,255,255,0.78)", **border(1, "rgba(29,80,103,0.12)", 16))
            for j, (n, d, u) in enumerate(rows, 1)]
        card = wave_card(f"rs-card-{key}", [
            container(f"rs-card-{key}-top", [
                icon(f"rs-card-{key}-i", ico, 24, view="stacked", shape="circle", primary_color=TEAL,
                     secondary_color=SAND, icon_padding=px(14), cls="jm-blob", _flex_size="none"),
                heading(f"rs-card-{key}-num", f"0{i}", "span", SERIF, 15, "#6A8CA3", weight=700, ls=0.08),
            ], row=True, align="center", gap_=14, flex_wrap="nowrap", flex_wrap_mobile="nowrap"),
            h2(f"rs-card-{key}-h", title, size="clamp(26px, 2.6vw, 34px)", lh=1.12),
            container(f"rs-card-{key}-rows", row_els, gap_=10),
        ], radius=28, pad=dims(30, 30, 100, 30), gap_=16, hover=False)
        card["settings"].update({**gradient("#FBFAF6", tint), **border(1, "#D9D3C4", 28),
                                 "css_classes": card["settings"]["css_classes"] + f" jm-res-card jm-res-{key}"})
        cards.append(card)

    chips = html("rs-filters", '<div class="jm-filters jm-res-filters" role="group" aria-label="Filter resources">' +
                 "".join(f'<button type="button" class="jm-filter jm-filter-sm" data-filter="{k}" '
                         f'aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in RES_FILTERS) +
                 '</div>')
    tools = section("rs-tools", [
        container("rs-tools-head", [
            container("rs-tools-head-text", [eyebrow("rs-tools-eyebrow", "Further support"),
                                             h2("rs-tools-h", "Trusted resources &amp; tools")], gap_=12, width=620,
                      grow=0),
            chips,
        ], row=True, wrap=True, justify="space-between", align="flex-end", gap_=gap(20, 40)),
        container("rs-cards", cards, cls="jm-res-cols"),
    ], pad=dims("clamp(48px,6vw,88px)", 24, "clamp(56px,7vw,96px)", 24), gap_=28)

    cta = sand_cta("rs-cta", "I am here to listen and support your next step",
                   "I invite you to reach out by email or phone for a chat.")
    return [hero, crisis, tools, cta]


# ---------------------------------------------------------------- Contact

def contact_tile(name, key, label, value_html, *, url=None, size=18, weight=700, extra=None):
    kids = [
        icon(f"{name}-i", key, 22, view="stacked", shape="circle", primary_color="#EEF4F6", secondary_color=TEAL,
             icon_padding=px(13), _flex_size="none"),
        container(f"{name}-t", [
            eyebrow(f"{name}-l", label, ls=0.12),
            text(f"{name}-v", value_html, size, INK, weight=weight, lh=1.5, cls="jm-tile-value"),
            *(extra or []),
        ], gap_=4, grow=1, width=px(0, "%"), mobile_width=False),
    ]
    common = dict(row=True, gap_=16, align="flex-start", pad=dims(24), flex_wrap="nowrap", flex_wrap_mobile="nowrap",
                  cls="jm-contact-tile", **WHITE_CARD, **border(1, LINE, 20))
    return link_box(name, kids, url, **common) if url else container(name, kids, **common)


def contact_page():
    hero = hero_text_only("ct-hero", [
        eyebrow("ct-eyebrow", "Contact", color=MIST),
        h1("ct-h1", "Contact Me", color="#ffffff"),
        para("ct-lede", "Feel free to reach out by email or phone to ask any questions or to discuss taking the next "
                        "step toward your healing.", "clamp(17px, 1.4vw, 19px)", SAND, 1.75, maxw=820),
        para("ct-p", "When you reach out by phone, you will speak directly with me. I manage my own enquiries to ensure "
                     "that from your very first phone call, you are met with a safe, confidential, and deeply "
                     "personalised introduction to care.", 17, MIST_LT, 1.75, maxw=820),
    ])
    photo_hero(hero, "photo_beach", "center 55%")
    address = "Unit 1, 38 Burnett Street, Mooloolaba QLD 4557"
    tiles = container("ct-tiles", [
        contact_tile("ct-phone", "i_phone", "Phone", f"<p>{PHONE}</p>", url=PHONE_URL, size=24),
        contact_tile("ct-email", "i_mail_line", "Email", "<p class=\"jm-email-v\">" + EMAIL.replace("@", "@<wbr>") + "</p>", url=EMAIL_URL, size=19),
        contact_tile("ct-loc", "i_map_pin", "Practice Location", f"<p>Heart of Mooloolaba<br>{address}</p>",
                     weight=600),
        contact_tile("ct-hours", "i_clock_sm", "Opening Hours", "<p>By Appointment Only</p>", extra=[
            para("ct-hours-p", "Monday: Face-to-face Consultations (In-Clinic)<br>Tuesday – Friday: Telehealth "
                               "Consultations (Online)", 16, GREY_BODY, 1.6)]),
    ], gap_=12, width=380, grow=1)
    q = "Unit+1%2C+38+Burnett+Street%2C+Mooloolaba+QLD+4557"
    map_col = container("ct-map-col", [
        widget("ct-map", "google_maps", {"address": address, "zoom": {"unit": "px", "size": 16},
                                        "height": {"unit": "px", "size": 420}, "_css_classes": "jm-map",
                                        "prevent_scroll": "yes"}),
        container("ct-map-btns", [
            button("ct-map-open", "Open in Google Maps", f"https://www.google.com/maps/search/?api=1&query={q}",
                   "primary"),
            button("ct-map-dir", "Get directions", f"https://www.google.com/maps/dir/?api=1&destination={q}", "ghost"),
        ], row=True, wrap=True, gap_=12),
    ], gap_=16, width=520, grow=999)
    for b in map_col["elements"][1]["elements"]:
        b["settings"]["link"]["is_external"] = "on"
    details = section("ct-details", [tiles, map_col], pad=dims("clamp(40px,5vw,72px)", 24, "clamp(56px,7vw,96px)", 24),
                      row=True, wrap=True, gap_=32, align="stretch", cls="jm-tide")

    enquiry = sand_cta("ct-enq", "", "", center=False, kids=[
        container("ct-enq-head", [
            icon("ct-enq-i", "i_lock", 22, view="stacked", shape="circle", primary_color=SAND, secondary_color=TEAL,
                 icon_padding=px(13), _flex_size="none"),
            h2("ct-enq-h", "Making an Enquiry", size="clamp(32px, 3.8vw, 48px)"),
        ], row=True, align="center", gap_=14, flex_wrap="nowrap", flex_wrap_mobile="nowrap"),
        para("ct-enq-p", "To protect your privacy, please limit initial text or email messages to basic contact details "
                         "and scheduling requests. We will safely discuss your clinical history and personal goals "
                         "together during your initial consultation.", 18, BODY_DK, 1.8),
        call_email("ct-enq-btns"),
        para("ct-enq-help", f'If you need help right now, please call 000 or Lifeline on 13 11 14, or see the '
                            f'<a href="{URL["support"]}"><strong>Support page</strong></a>.', 15, "#33475A", 1.6,
             cls="jm-inline-links"),
    ])
    return [hero, details, enquiry]


# ---------------------------------------------------------------- Support

def call_card(name, title, desc, number, tel):
    return link_box(name, [
        container(f"{name}-t", [
            heading(f"{name}-h", title, "p", SANS, 20, INK, weight=700, lh=1.3),
            text(f"{name}-d", f"<p>{desc}</p>", 15, GREY_BODY, lh=1.5),
            heading(f"{name}-n", number, "p", SANS, 26, TEAL, weight=700, lh=1.2),
        ], gap_=4, grow=1, width=px(0, "%"), mobile_width=False),
        icon(f"{name}-i", "i_phone", 20, view="stacked", shape="circle", primary_color=TEAL, secondary_color="#ffffff",
             icon_padding=px(14), _flex_size="none"),
    ], f"tel:{tel}", cls="jm-call", row=True, justify="space-between", align="center", gap_=16, pad=dims(22, 24),
        flex_wrap="nowrap", flex_wrap_mobile="nowrap", **WHITE_CARD, **border(1, LINE, 20))


def support_page():
    sos = link_box("sp-000", [
        heading("sp-000-l", "Emergency Services", "p", SANS, 14, INK, weight=700, ls=0.12, transform="uppercase"),
        heading("sp-000-n", "000", "p", SERIF, "clamp(72px, 8vw, 104px)", INK, weight=700, lh=1),
        text("sp-000-d", "<p>For immediate danger or medical emergencies</p>", 16, INK, lh=1.5),
        heading("sp-000-tap", "Tap to call", "span", SANS, 15, "#ffffff", weight=600, lh=1.2, cls="jm-tap-pill",
                _margin=dims(8, 0, 0, 0)),
    ], "tel:000", cls="jm-sos-card", gap_=6, pad=dims(32), width=300, grow=1, border_radius=dims(28),
        background_background="classic", background_color=OCHRE)
    hero = page_hero("sp-hero", [
        eyebrow("sp-eyebrow", "Support", color=MIST),
        h1("sp-h1", "If you need help right now", color="#ffffff"),
        para("sp-lede", "If you or someone you know is in acute distress or experiencing an immediate safety risk, please "
                        "utilise the crisis contacts below or present to your nearest hospital emergency department.",
             "clamp(17px, 1.4vw, 19px)", MIST_LT, 1.75),
        para("sp-note", "This practice is not a crisis service.", 15, MUTED, 1.6),
    ], sos, bg=INK, pad=dims("clamp(56px,7vw,96px)", 24, "clamp(96px,10vw,130px)", 24))
    hero["elements"][0]["settings"]["flex_gap"] = gap(18)

    calls = [call_card(f"sp-call-{tel}", n, d, num, tel) for n, d, num, tel in CRISIS_LINES + [OPEN_ARMS]]
    lines = section("sp-lines", [
        h2("sp-lines-h", "Immediate Crisis &amp; 24/7 Support", size="clamp(32px, 3.8vw, 48px)"),
        grid("sp-lines-grid", calls, 440, 14),
    ], pad=dims("clamp(48px,6vw,80px)", 24, "clamp(56px,7vw,96px)", 24), gap_=28)

    card = lambda n, title, body, btns: container(f"sp-next-{n}", [
        h2(f"sp-next-{n}-h", title, size=30, lh=1.15), para(f"sp-next-{n}-p", body, 16, GREY_BODY, 1.7),
        container(f"sp-next-{n}-btns", btns, row=True, wrap=True, gap_=10),
    ], gap_=12, pad=dims(32), border_radius=dims(24), background_background="classic", background_color=SAND)
    beyond = button("sp-bn-btn", "Open BeyondNow ↗", "https://www.beyondblue.org.au/get-support/"
                    "beyondnow-suicide-safety-planning", "ghost")
    beyond["settings"]["link"]["is_external"] = "on"
    after = section("sp-next", [grid("sp-next-grid", [
        card("bn", "BeyondNow", "An interactive app created by Beyond Blue to help you easily build and keep a personal "
                                "safety plan on your phone for times of high distress.", [beyond]),
        card("res", "More resources", "Trauma, eating disorders, complex mental health and grounding tools.",
             [button("sp-res-btn", "Go to Resources", URL["resources"], "ghost")]),
        card("con", "Contact Jennifer", "By Appointment Only. For non-urgent enquiries, reach out by email or phone.",
             [button("sp-con-call", PHONE, PHONE_URL, "primary"), button("sp-con-email", "Email", EMAIL_URL, "ghost")]),
    ], 340, 20)], pad=dims("clamp(56px,7vw,88px)", 24), bg=STONE)
    return [hero, lines, after]


# ---------------------------------------------------------------- Privacy & disclaimer

def toc_pill(name, label, url):
    return button(name, label, url, "ghost", button_text_color=INK, background_color=SAND, border_width=dims(1),
                  border_color="#D6CFBD", button_background_hover_color=SAND, hover_color=TEAL_DK_,
                  button_hover_border_color=TEAL, text_padding=dims(13, 18), typography_font_size=px(15))


TEAL_DK_ = "#0d4c5c"


def privacy_page():
    narrow = dict(boxed_width=880)
    hero = section("pv-hero", [container("pv-hero-text", [
        eyebrow("pv-eyebrow", "Legal", color=MIST),
        heading("pv-h1", "Privacy policy &amp; website disclaimer", "h1", SERIF, "clamp(40px, 5vw, 64px)", "#ffffff",
                weight=600, lh=1.04, ls=-0.01),
        container("pv-toc", [toc_pill("pv-toc-p", "Privacy policy", "#privacy"),
                             toc_pill("pv-toc-d", "Website disclaimer", "#disclaimer")],
                  row=True, wrap=True, gap_=10, pad=dims(6, 0, 0, 0), tag="nav"),
    ], gap_=18)], pad=dims("clamp(56px,7vw,88px)", 24, "clamp(88px,9vw,120px)", 24), bg=STONE, cls="jm-page-hero",
        **narrow)
    photo_hero(hero, "photo_beach", "center 60%")

    privacy = section("pv-privacy", [
        h2("pv-p-h", "Privacy policy", size="clamp(32px, 3.6vw, 46px)", lh=1.1),
        para("pv-p-p", "To protect your privacy, please limit initial text or email messages to basic contact details "
                       "and scheduling requests. We will safely discuss your clinical history and personal goals "
                       "together during your initial consultation.", 17, BODY_DK, 1.8),
        text("pv-p-ph", "<p>[Jennifer's full privacy policy text — to be supplied]</p>", 16, TEAL, lh=1.6,
             cls="jm-placeholder-box"),
        container("pv-p-enq", [
            eyebrow("pv-p-enq-l", "Privacy enquiries", ls=0.12),
            text("pv-p-enq-t", f"<p>Jennifer Malecki &amp; Associates Pty Ltd · ABN 63 687 967 193<br>"
                               f"Unit 1, 38 Burnett Street, Mooloolaba QLD 4557<br>"
                               f'<a href="{PHONE_URL}">{PHONE}</a> · <a href="{EMAIL_URL}">{EMAIL}</a></p>', 16, BODY_DK,
                 lh=1.7, cls="jm-inline-links"),
        ], gap_=6, pad=dims(24), **WHITE_CARD, **border(1, LINE, 20)),
    ], pad=dims("clamp(48px,6vw,80px)", 24, 24, 24), gap_=20, _element_id="privacy", cls="jm-anchor", **narrow)

    bar = container("pv-d-bar", [
        text("pv-d-bar-t", '<p>This website is not a crisis service. In an emergency call <a href="tel:000">'
                           '<strong>000</strong></a>.</p>', 16, SAND, lh=1.6, cls="jm-bar-links"),
        button("pv-d-bar-btn", "Support lines", URL["support"], "ochre"),
    ], row=True, wrap=True, justify="space-between", align="center", gap_=gap(12, 24), pad=dims(24),
        border_radius=dims(20), background_background="classic", background_color=INK)
    disclaimer = section("pv-disclaimer", [
        h2("pv-d-h", "Website disclaimer", size="clamp(32px, 3.6vw, 46px)", lh=1.1),
        text("pv-d-body", f"<p><strong>{NAME_TITLE}</strong> | AHPRA Reg: PSY 0001410118</p>"
                          "<p><em>Educational Content Only: The information on this website is not a substitute for "
                          "professional psychological treatment and does not constitute a clinical relationship. This "
                          "site is not monitored 24/7.</em></p>"
                          "<p><strong>In a Crisis?</strong> This is not an emergency service. If you are in immediate "
                          'danger, please call <a href="tel:000"><strong>000</strong></a>, visit an emergency '
                          'department, or contact <a href="https://www.lifeline.org.au/" target="_blank" '
                          'rel="noopener">Lifeline</a> <strong>on <a href="tel:131114">13 11 14</a></strong> or '
                          '<a href="https://www.beyondblue.org.au/" target="_blank" rel="noopener">Beyond Blue</a> '
                          '<strong>on <a href="tel:1300224636">1300 22 4636</a></strong>.</p>', 17, BODY_DK, lh=1.8,
             cls="jm-inline-links jm-prose"),
        para("pv-d-copy", "Artworks and photographs on this website are © Jennifer Malecki and may not be copied, "
                          "downloaded, reproduced or used in any form without written permission.", 17, BODY_DK, 1.8),
        bar,
    ], pad=dims("clamp(40px,5vw,64px)", 24, "clamp(56px,7vw,96px)", 24), gap_=20, _element_id="disclaimer",
        cls="jm-anchor", **narrow)
    return [hero, privacy, disclaimer]


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    out = {"header-inner": build_inner_header(), "about": about_page(), "services": services_page(),
           "fees": fees_page(), "referrers": referrers_page(), "gallery": gallery_page(),
           "resources": resources_page(), "contact": contact_page(), "support": support_page(),
           "privacy": privacy_page()}
    for name, data in out.items():
        path = DIST / f"{name}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        print(f"{path.name}: {path.stat().st_size} bytes")
