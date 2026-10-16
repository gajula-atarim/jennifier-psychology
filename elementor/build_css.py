"""Builds the child theme stylesheet: the design layer Elementor controls can't express
(decorative waves, pill chips, hover motion, scroll reveal, the breathing exercise)."""
from pathlib import Path

from svg import (BREATH_W1, BREATH_W2, BREATH_W3, CARD_W1, CARD_W2, CARD_W3, CARE_LINE, CARE_PRINTS, CTA_EDGE,
                 GP_MARK, HERO_EDGE, ICE_BELOW, ICE_TIP, PORTRAIT_LINES, SURF_W1, SURF_W2, SURF_W3)

OUT = Path(__file__).resolve().parent.parent / "theme/hello-elementor-child/assets/css/jm-site.css"

CSS = """/* Jennifer Malecki — design layer for the Elementor build. */

/* Base */
body{background:#F7F5EF;color:#12323F;-webkit-font-smoothing:antialiased}
a{color:#1D5067}a:hover,a:active{color:#0d4c5c}
h1.elementor-heading-title,h2.elementor-heading-title,h3.elementor-heading-title{text-wrap:balance}
.elementor-widget-icon .elementor-icon-wrapper{line-height:0}
.elementor-widget-icon .elementor-icon svg{display:block}
.elementor-widget-text-editor p{margin:0;text-wrap:pretty}
.elementor-widget-text-editor ul{margin:0}
.elementor-widget-text-editor a{color:inherit;text-decoration:none}
.elementor-widget-text-editor strong{font-weight:700}
.jm-caption strong{color:#12323F;font-weight:700}
.elementor-button{transition:background-color .2s,color .2s,border-color .2s,transform .2s ease,box-shadow .2s ease}
/* Every pill button lifts slightly with a soft shadow on hover and keyboard focus (colours come from
   each button's Elementor hover settings); text links underline and nudge their arrow instead. */
.elementor-widget-button:not(.jm-textlink) .elementor-button:hover,.elementor-widget-button:not(.jm-textlink) .elementor-button:focus-visible{transform:translateY(-2px);box-shadow:0 10px 22px rgba(18,50,63,.2)}
.elementor-widget-button:not(.jm-textlink) .elementor-button:active{transform:none;box-shadow:0 4px 10px rgba(18,50,63,.16)}
.elementor-button:focus-visible{outline:2px solid #DDAA33;outline-offset:3px}
.jm-textlink .elementor-button-icon{transition:transform .2s ease}
.jm-textlink .elementor-button:hover .elementor-button-icon,.jm-textlink .elementor-button:focus-visible .elementor-button-icon{transform:translateX(4px)}
.jm-textlink .elementor-button:hover .elementor-button-text,.jm-textlink .elementor-button:focus-visible .elementor-button-text{text-decoration:underline;text-underline-offset:4px}

/* Icon lists: Elementor adds a hidden 4px icon margin and 5px text padding on top of the
   Gap control. Remove them so the Gap setting is the whole gap (8px in the design); this is
   what lets the top bar fit on one line at tablet widths. */
body .elementor-widget.elementor-widget-icon-list .elementor-icon-list-icon svg{margin:0}
body .elementor-widget.elementor-widget-icon-list .elementor-icon-list-icon+.elementor-icon-list-text{padding-inline-start:0}

/* Header */
/* Floating header: the crisis bar sits at the top of the page and the main header is a rounded
   glass pill floating over the hero. It scrolls away with the page (not sticky). */
#masthead{position:relative;z-index:100}
#masthead .jm-header-main{position:absolute!important;top:calc(100% + 16px);left:16px;right:16px;width:auto!important;max-width:1340px;margin:0 auto!important;z-index:100;-webkit-backdrop-filter:blur(14px) saturate(140%);backdrop-filter:blur(14px) saturate(140%);box-shadow:0 12px 32px rgba(10,30,40,.18)}
@media (max-width:767px){#masthead .jm-header-main{left:12px;right:12px;top:calc(100% + 12px)}}
/* Keep the hero message clear of the pill. */
.jm-hero .jm-hero-msg{padding-top:calc(24px + clamp(64px,7vw,96px))!important}
.jm-topbar a{color:#EBE7DB}.jm-topbar a:hover{color:#DDAA33}
/* When the crisis line wraps (tablet/phone), split it into two even lines. */
.jm-topbar .elementor-widget-text-editor p{text-wrap:balance}
@media (min-width:1025px){
 .jm-nav a.hfe-menu-item{border-radius:999px;min-height:44px;display:inline-flex!important;align-items:center;white-space:nowrap;box-sizing:border-box;transition:none}
 .jm-nav .hfe-nav-menu{gap:2px}
}
/* Tablet and mobile: hamburger toggle (44px tap target) and a full-width dropdown under the header. */
@media (max-width:1024px){
 .jm-nav .hfe-nav-menu__toggle{cursor:pointer}
 .jm-nav .hfe-nav-menu-icon{display:flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border-radius:999px;box-sizing:border-box;transition:background-color .2s}
 .jm-nav .hfe-nav-menu__toggle:hover .hfe-nav-menu-icon,.jm-nav .hfe-active-menu .hfe-nav-menu-icon{background:rgba(255,255,255,.12)}
 .jm-nav .hfe-nav-menu-icon svg{fill:none!important}
 /* Keep the closed menu out of the header row (so the toggle sits beside the logo) and open it
    as a rounded panel just under the pill. */
 .jm-nav,.jm-nav .hfe-nav-menu,.jm-nav .hfe-layout-horizontal{position:static!important}
 .jm-nav nav.hfe-nav-menu__layout-horizontal{position:absolute!important;top:calc(100% + 8px)!important;left:0!important;right:0!important;width:auto!important;margin-top:0!important;z-index:50;border-radius:24px;overflow:hidden;background:#12323F;border:1px solid rgba(255,255,255,.14);box-shadow:0 18px 36px rgba(10,30,40,.3)}
 .jm-nav nav .hfe-nav-menu{margin:0!important}
 .jm-nav nav .hfe-nav-menu>li:last-child>a.hfe-menu-item{border-bottom:0!important}
 .jm-nav nav a.hfe-menu-item{border-radius:0}
}

/* Hero */
.jm-hero{position:relative;overflow:hidden}
.jm-hero .elementor-background-video-hosted{object-position:center 40%}
.jm-hero::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:clamp(36px,5vw,72px);background:HERO_EDGE center bottom/100% 100% no-repeat;z-index:3;pointer-events:none}
.jm-hero-msg{position:relative;z-index:2;animation:jmHeroMsg 6s ease forwards}
@keyframes jmHeroMsg{0%{opacity:0;transform:translateY(12px)}12%{opacity:1;transform:none}84%{opacity:1}100%{opacity:0;visibility:hidden}}
.jm-lined .elementor-heading-title{display:flex;align-items:center;justify-content:center;gap:14px}
.jm-lined .elementor-heading-title::before,.jm-lined .elementor-heading-title::after{content:"";display:block;flex:none;width:36px;height:1px;background:#DDAA33}

/* Intro */
.jm-rise{animation:jmRise 1.1s cubic-bezier(.2,.7,.2,1) both}
@keyframes jmRise{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
.jm-pill .elementor-heading-title{display:inline-flex;align-items:center;gap:10px;background:#F4E6BF;border-radius:999px;padding:6px 14px;text-wrap:balance}
.jm-pill .elementor-heading-title::before{content:"";display:block;flex:none;width:8px;height:8px;border-radius:50%;background:#C08A12}
.jm-pill-ochre .elementor-heading-title{background:#DDAA33;padding:8px 16px}
.jm-pill-ochre .elementor-heading-title::before{width:9px;height:9px;background:#12323F}

/* Cards */
.jm-card{transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s ease,border-color .35s ease,background-color .35s ease}
.jm-card:hover{transform:translateY(-6px);box-shadow:0 20px 44px rgba(18,50,63,.14);border-color:#A2C3D3!important}
.jm-card .elementor-widget-icon svg{transition:transform .35s ease}
.jm-card:hover .elementor-widget-icon svg{transform:scale(1.1) rotate(-4deg)}
.jm-card-dark:hover{background:rgba(247,245,239,.15)!important;box-shadow:0 20px 44px rgba(0,0,0,.28)}

/* Rolling waves at the foot of a card */
.jm-wave-card{position:relative;overflow:hidden}
.jm-wave-card>.elementor-element,.jm-wave-card>.e-con-inner{position:relative;z-index:1}
.jm-wave-card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:96px;pointer-events:none;
 background-image:CARD_W3,CARD_W2,CARD_W1;background-size:200% 100%;background-repeat:repeat-x;
 animation:jmCardWaves 4080s linear infinite;transition:height .5s ease}
.jm-wave-card:hover::after{height:122px}
.jm-wave-sm::after{height:66px}.jm-wave-sm:hover::after{height:82px}
.jm-wave-lg::after{height:110px}.jm-wave-lg:hover::after{height:122px}
/* Each layer drifts one wave period per its design duration (back 48s, middle 40s reversed, front 34s);
   4080s is their least common multiple, so the loop is seamless. */
@keyframes jmCardWaves{from{background-position:0 0,0 0,0 0}to{background-position:12000% 0,-10200% 0,8500% 0}}
/* Same for the surface and breathing waves: 28s, 22s reversed, 18s (LCM 2772s). */
@keyframes jmWaves{from{background-position:0 0,0 0,0 0}to{background-position:15400% 0,-12600% 0,9900% 0}}

/* Scroll reveal */
@keyframes jmTide{from{transform:translateY(16px);opacity:.6}to{transform:none;opacity:1}}
@keyframes jmSink{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
@supports (animation-timeline:view()){
 .jm-tide{animation:jmTide ease-out both;animation-timeline:view();animation-range:entry 0% entry 30%}
 .jm-chips-dark .elementor-icon-list-item{animation:jmSink linear both;animation-timeline:view()}
 /* Each chip sinks in soon after it enters the viewport (finished ~18% into its trip), staggered
    so they arrive one after another; all five are in place well before the card is centred. */
 .jm-chips-dark .elementor-icon-list-item:nth-child(1){animation-range:cover 2% cover 10%}
 .jm-chips-dark .elementor-icon-list-item:nth-child(2){animation-range:cover 4% cover 12%}
 .jm-chips-dark .elementor-icon-list-item:nth-child(3){animation-range:cover 6% cover 14%}
 .jm-chips-dark .elementor-icon-list-item:nth-child(4){animation-range:cover 8% cover 16%}
 .jm-chips-dark .elementor-icon-list-item:nth-child(5){animation-range:cover 10% cover 18%}
}

/* Welcome portrait placeholder */
.jm-portrait{position:relative;overflow:hidden;aspect-ratio:4/5}
.jm-portrait::after{content:"";position:absolute;left:0;right:0;bottom:0;height:28%;background:PORTRAIT_LINES center/100% 100% no-repeat;pointer-events:none}
/* With a photo: it fills the arch (the framed photo is already 4:5, so nothing important is cropped). */
.jm-portrait>.jm-portrait-img{position:absolute!important;inset:0;margin:0}
.jm-portrait-img>*,.jm-portrait-img a{display:block;height:100%}
.jm-portrait-img img{width:100%;height:100%;max-width:none;object-fit:cover;object-position:50% 100%;display:block}
.jm-portrait:has(.jm-portrait-img img)::after{display:none}

/* Beneath the surface */
.jm-ice-top{position:relative}
.jm-ice-top::after{content:"";position:absolute;inset:0 0 -1px;pointer-events:none;
 background-image:SURF_W3,SURF_W2,SURF_W1,ICE_TIP;
 background-size:200% 64px,200% 64px,200% 64px,300px 68px;
 background-repeat:repeat-x,repeat-x,repeat-x,no-repeat;
 background-position:0 100%,0 100%,0 100%,50% calc(100% - 30px);
 animation:jmSurface 2772s linear infinite}
@keyframes jmSurface{to{background-position:15400% 100%,-12600% 100%,9900% 100%,50% calc(100% - 30px)}}
.jm-ice-top>.elementor-element{position:relative;z-index:1}
.jm-ice-bottom{position:relative}
.jm-ice-bottom::after{content:"";position:absolute;left:12%;top:0;width:76%;height:92%;background:ICE_BELOW center/100% 100% no-repeat;pointer-events:none}
.jm-ice-bottom>.elementor-element{position:relative;z-index:1}
.jm-mt-auto{margin-top:auto!important}
.jm-chips .elementor-icon-list-items{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0!important}
.jm-chips .elementor-icon-list-items .elementor-icon-list-item{margin:0!important;background:#fff;border-radius:999px;padding:8px 16px}
.jm-chips .elementor-icon-list-item::after{display:none!important}
.jm-chips-dark .elementor-icon-list-items{gap:10px}
.jm-chips-dark .elementor-icon-list-items .elementor-icon-list-item{background:rgba(247,245,239,.1);border:1px solid rgba(162,195,211,.5);padding:9px 18px}

/* Approach: artwork and care pathway */
.jm-art{position:relative;overflow:hidden;aspect-ratio:4/5}
.jm-art>.elementor-widget-image{position:absolute!important;inset:0;margin:0}
.jm-art>.elementor-widget-image>*,.jm-art>.elementor-widget-image a{display:block;height:100%}
.jm-art .elementor-widget-image img{width:100%;height:100%;max-width:none;object-fit:cover;display:block;pointer-events:none;user-select:none}
.jm-swap-a{animation:jmSwapA 20s ease-in-out infinite}
.jm-swap-b{animation:jmSwapB 20s ease-in-out infinite}
@keyframes jmSwapA{0%,40%{opacity:1;transform:scale(1)}50%,90%{opacity:0;transform:scale(1.04)}100%{opacity:1;transform:scale(1)}}
@keyframes jmSwapB{0%,40%{opacity:0;transform:scale(1.04)}50%,90%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(1.04)}}
.jm-art>.jm-art-caption{position:absolute!important;left:20px;bottom:20px;z-index:2;width:auto!important;max-width:calc(100% - 40px)}
/* Gallery collage: the ocean painting large at the top left, the wave painting smaller at the bottom
   right in a sand-coloured mat, overlapping it. */
.jm-collage{position:relative;width:100%;aspect-ratio:450/690}
.jm-collage>.jm-art{position:absolute!important;margin:0!important}
.jm-collage>.jm-art-main{left:0;top:0;width:76%!important;aspect-ratio:4/5;box-shadow:0 24px 48px rgba(18,50,63,.18)}
.jm-collage>.jm-art-inset{right:0;bottom:0;width:60%!important;aspect-ratio:10/13;z-index:2;border:8px solid #F7F5EF;box-shadow:0 24px 48px rgba(18,50,63,.22)}
.jm-collage>.jm-art-inset>.jm-art-caption{left:12px;bottom:12px;max-width:calc(100% - 24px)}
.jm-art-caption .elementor-heading-title{display:inline-block;background:rgba(18,50,63,.82);padding:8px 14px;border-radius:999px}
.jm-care-list{position:relative}
/* Tiny footprints walk between the stones (stops are 80px, so one left-right pair lands in each gap). */
.jm-care-list::after{content:"";position:absolute;left:0;top:40px;bottom:40px;width:48px;background:CARE_PRINTS 0 24px/48px 32px repeat-y;pointer-events:none}
.jm-care-list>.elementor-element{position:relative;z-index:1}
.jm-stop{text-decoration:none;transition:background-color .3s ease}
.jm-stop:hover,.jm-stop:focus-visible{background:rgba(162,195,211,.25)}
.jm-stone .elementor-heading-title{width:48px;height:48px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;border-radius:50% 46% 52% 48%/48% 52% 46% 50%;background:#F7F5EF;border:2px solid #1D5067;box-shadow:0 0 0 3px #F7F5EF;transition:background-color .3s ease,color .3s ease,transform .3s ease,border-color .3s ease}
.jm-stop:hover .jm-stone .elementor-heading-title,.jm-stop:focus-visible .jm-stone .elementor-heading-title{background:#DDAA33;border-color:#DDAA33;color:#12323F;transform:scale(1.08)}
.jm-stop-arrow{opacity:0;transform:translateX(-8px);transition:opacity .3s ease,transform .3s ease}
.jm-stop:hover .jm-stop-arrow,.jm-stop:focus-visible .jm-stop-arrow{opacity:1;transform:none}

/* For GPs */
.jm-gp{position:relative;overflow:hidden}
.jm-gp::after{content:"";position:absolute;right:-140px;top:-120px;width:560px;height:560px;opacity:.12;background:GP_MARK center/contain no-repeat;pointer-events:none}
.jm-gp>.e-con-inner{position:relative;z-index:1}
.jm-refer-list ul{padding-left:20px}

/* Next step: footprints on sand */
.jm-step{position:relative;overflow:hidden}
.jm-prints{display:flex;justify-content:space-around;align-items:center;height:58px;margin:-6px 0 4px}
.jm-prints span{display:block}
.jm-prints span:nth-child(odd){transform:translateY(-9px) rotate(90deg)}
.jm-prints span:nth-child(even){transform:translateY(9px) rotate(90deg) scaleX(-1)}
.jm-prints svg{display:block;width:24px;height:38px;fill:#9C7A45;opacity:0;animation:jmWalk 8s ease-in-out infinite}
@keyframes jmWalk{0%{opacity:0;transform:scale(.55)}5%{opacity:.85;transform:scale(1.08)}8%{transform:none}62%{opacity:.85}80%{opacity:0}100%{opacity:0}}
/* Paused until the steps row scrolls into view (see jm-site.js); the delays then count from that moment. */
.jm-walk-pending .jm-prints svg{animation-play-state:paused}


/* Breathe with the ocean */
.jm-breath-col{position:relative;overflow:hidden}
.jm-breath-col>.elementor-widget-html{position:absolute!important;inset:0;margin:0}
.jm-breath-col>.elementor-widget-html>*{height:100%}
.jm-breath{position:absolute;inset:0;overflow:hidden}
.jm-breath-words{position:absolute;top:40px;left:0;right:0;height:56px;font-family:'Cormorant Garamond',Georgia,serif;font-size:44px;font-weight:600;line-height:1.2;color:#fff;text-align:center;z-index:1}
.jm-breath-words span{position:absolute;left:0;right:0;padding:0 16px}
.jm-breath-words .jm-b-idle{font-size:30px;color:#DCE8EE;opacity:0}
.jm-breath-sea{position:absolute;left:0;right:0;bottom:0;height:78%;overflow:hidden}
.jm-breath-rise{position:absolute;left:0;right:0;top:0;bottom:-40%;animation:jmBreathe 10s ease-in-out infinite}
.jm-breath-waves{position:absolute;left:0;right:0;top:0;height:60%;background-image:BREATH_W3,BREATH_W2,BREATH_W1;background-size:200% 100%;background-repeat:repeat-x;animation:jmWaves 2772s linear infinite}
.jm-breath-body{position:absolute;left:0;right:0;top:calc(60% - 2px);bottom:0;background:#7EB1CB;opacity:.55}
@keyframes jmBreathe{0%{transform:translateY(62%)}40%{transform:translateY(0)}100%{transform:translateY(62%)}}
/* One 10s breath shared by the wave and the words: in for 4s while the wave rises to its crest (0-40%),
   out for 6s while it settles back (40-100%). The words hand over exactly at the crest. */
.jm-b-in{animation:jmBIn 10s linear infinite}
.jm-b-out{animation:jmBOut 10s linear infinite}
@keyframes jmBIn{0%{opacity:0;transform:scale(.94)}3%{opacity:1}37%{opacity:1;transform:scale(1.06)}40%{opacity:0;transform:scale(1.06)}100%{opacity:0;transform:scale(.94)}}
@keyframes jmBOut{0%,40%{opacity:0;transform:scale(1.06)}43%{opacity:1;transform:scale(1.06)}97%{opacity:1;transform:scale(.94)}100%{opacity:0;transform:scale(.94)}}
/* Pause freezes the wave and the words together so they never drift apart. */
.jm-breath.is-paused .jm-breath-rise,.jm-breath.is-paused .jm-breath-waves,.jm-breath.is-paused .jm-b-in,.jm-breath.is-paused .jm-b-out{animation-play-state:paused}
.jm-breath.is-paused .jm-b-in,.jm-breath.is-paused .jm-b-out{visibility:hidden}
.jm-breath.is-paused .jm-b-idle{opacity:1}

/* Support now: phone tiles */
.jm-tile{text-decoration:none;transition:transform .3s ease,box-shadow .3s ease,background-color .3s ease}
.jm-tile:hover,.jm-tile:focus-visible{transform:translateY(-4px);box-shadow:0 14px 30px rgba(18,50,63,.16)}
.jm-tile:hover{background-color:#E2EDF1!important}
.jm-tile-emergency:hover{background-color:#1D5067!important}

/* Closing call to action: shoreline edge */
.jm-cta{position:relative}
.jm-cta::after{content:"";position:absolute;left:0;right:0;top:-1px;height:clamp(40px,5.5vw,84px);background:CTA_EDGE center top/100% 100% no-repeat;pointer-events:none}
.jm-cta>.e-con-inner{position:relative;z-index:1}

/* Footer */
.jm-footer a{color:#EBE7DB}.jm-footer a:hover{color:#DDAA33}

/* Stacked layouts (tablet/phone): keep the portrait and the artwork at a comfortable size, centred,
   instead of stretching across the whole column. */
@media (max-width:1024px){
 .jm-portrait,.jm-portrait~.jm-caption{width:100%!important;max-width:440px!important;margin-inline:auto!important}
 .jm-collage{max-width:520px;margin-inline:auto}
}

/* Motion preferences */
@media (prefers-reduced-motion:reduce){
 .jm-rise,.jm-tide,.jm-chips-dark .elementor-icon-list-item,.jm-wave-card::after,.jm-ice-top::after,.jm-breath-waves{animation:none!important}
 .jm-swap-a{animation:none;opacity:1}.jm-swap-b{animation:none;opacity:0}
 .jm-prints svg{animation:none;opacity:.85}
 .jm-card,.jm-tile,.jm-card .elementor-widget-icon svg,.jm-wave-card::after,.jm-stop,.jm-stone .elementor-heading-title,.jm-stop-arrow{transition:none}
 .jm-card:hover,.jm-tile:hover,.jm-card:hover .elementor-widget-icon svg{transform:none}
 .elementor-button,.elementor-button:hover,.elementor-button:focus-visible,.jm-textlink .elementor-button-icon{transform:none!important}
}
"""

TOKENS = {
    "HERO_EDGE": HERO_EDGE, "CTA_EDGE": CTA_EDGE, "GP_MARK": GP_MARK, "PORTRAIT_LINES": PORTRAIT_LINES,
    "ICE_TIP": ICE_TIP, "ICE_BELOW": ICE_BELOW, "CARE_LINE": CARE_LINE, "CARE_PRINTS": CARE_PRINTS,
    "CARD_W1": CARD_W1, "CARD_W2": CARD_W2, "CARD_W3": CARD_W3,
    "SURF_W1": SURF_W1, "SURF_W2": SURF_W2, "SURF_W3": SURF_W3,
    "BREATH_W1": BREATH_W1, "BREATH_W2": BREATH_W2, "BREATH_W3": BREATH_W3,
}


def build() -> str:
    css = CSS
    # Longest names first so CARD_W1 doesn't clip a longer token.
    for name in sorted(TOKENS, key=len, reverse=True):
        css = css.replace(name, TOKENS[name])
    return css


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build())
    print(OUT, len(OUT.read_text()))
