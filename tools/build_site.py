#!/usr/bin/env python3
"""Generate the multi-page Harmonix glass mockup site from the single-file source."""
import re, random, os, time

VER = str(int(time.time()))
SRC = "harmonix-earn-glass.html"
OUT = "harmonix-glass-deploy"

src = open(SRC).read()

# ---------- 1. split source ----------
style_m = re.search(r"<style>(.*?)</style>", src, re.S)
base_css = style_m.group(1)
# strip EXTRA blocks re-ingested from a previous build cycle (they get re-appended below)
base_css = base_css.split("/* ---------- subpage components")[0]

main_start = src.index('<main class="main">')
shell_head = src[:main_start]              # meta, title, sprite svg, <div class="app">, sidebar, up to main
shell_head = shell_head.replace(style_m.group(0), '<link rel="stylesheet" href="assets/style.css?v=' + VER + '">\n<script src="assets/app.js?v=' + VER + '" defer></script>')
shell_head = re.sub(r'(<script src="assets/app\.js[^"]*" defer></script>\s*)+', lambda m: m.group(0).split('</script>')[0] + '</script>', shell_head)

home_main = src[main_start:]               # <main> ... </main></div>
SHELL_TAIL = "</div>\n"

# ---------- 1b. sidebar footer: auditor logos + socials + docs ----------
VERICHAINS_SVG = open("verichains.svg").read().strip()
SHIELDIFY_SVG = open("shieldify.svg").read().strip()
ZENITH_SVG = open("zenith.svg").read().strip()

SIDE_FOOT = ('<div class="side-foot">'
  '<div class="audit-label">Audited by</div>'
  '<div class="audit-logos">'
  '<a href="https://github.com/harmonixfi/core-smart-contract/tree/main/audits" aria-label="Verichains audits">' + VERICHAINS_SVG + '</a>'
  '<a href="https://github.com/harmonixfi/core-smart-contract/blob/main/audits/Harmonix%20Finance%20-%20Zenith%20Audit%20Report.pdf" aria-label="Zenith audit report">' + ZENITH_SVG + '</a>'
  '<a href="https://github.com/shieldify-security/audits-portfolio/blob/main/reports/HarmonixFinance-Hyperliquid-Security-Review.pdf" aria-label="Shieldify security review">' + SHIELDIFY_SVG + '</a>'
  '</div>'
  '<div class="socials">'
  '<a href="https://twitter.com/harmonixfi" aria-label="Harmonix on X"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M12.6 1h2.2L9.9 6.6 15.6 15h-4.5L7.6 10.3 3.6 15H1.4l5.2-6L1.1 1h4.6l3.2 4.3L12.6 1Zm-.8 12.7h1.2L4.9 2.2H3.6l8.2 11.5Z"/></svg></a>'
  '<a href="https://discord.gg/UqtmNj4Ryt" aria-label="Harmonix Discord"><svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M13.5 3.2A13 13 0 0 0 10.3 2.2l-.15.3c1 .25 1.9.62 2.8 1.15a10.6 10.6 0 0 0-9.9 0c.9-.53 1.8-.9 2.8-1.15L5.7 2.2a13 13 0 0 0-3.2 1C.9 6.2.5 9.1.7 12c1.2.9 2.4 1.45 3.6 1.8l.75-1.2c-.65-.25-1.25-.55-1.8-.9l.4-.3c2.2 1 4.5 1 6.7 0l.4.3c-.55.35-1.15.65-1.8.9l.75 1.2c1.2-.35 2.4-.9 3.6-1.8.25-3.35-.45-6.2-1.8-8.8ZM5.6 10.3c-.7 0-1.25-.6-1.25-1.35S4.9 7.6 5.6 7.6s1.25.6 1.25 1.35-.55 1.35-1.25 1.35Zm4.8 0c-.7 0-1.25-.6-1.25-1.35S9.7 7.6 10.4 7.6s1.25.6 1.25 1.35-.55 1.35-1.25 1.35Z"/></svg></a>'
  '<a href="https://t.me/harmonix_chat" aria-label="Harmonix Telegram"><svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M14.7 1.6c.25-.1.5.1.45.4l-2.1 11.3c-.06.3-.4.45-.66.3l-3.2-2-1.65 1.7c-.22.22-.6.12-.68-.18l-1.1-3.3L2 8.7c-.32-.12-.32-.6 0-.72L14.7 1.6ZM5.9 9.4l.55 2.1 1-1.05-1.55-1.05Zm6.6-6-8.1 4.4 2.4.85 4.4-3.55c.2-.16.44.1.28.3L8.4 9l3.4 2.15L13.5 3.4h-1Z"/></svg></a>'
  '<a href="https://github.com/harmonixfi" aria-label="Harmonix GitHub"><svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 .8a7.2 7.2 0 0 0-2.28 14.03c.36.07.5-.16.5-.35v-1.22c-2 .44-2.43-.97-2.43-.97-.32-.83-.8-1.05-.8-1.05-.66-.45.05-.44.05-.44.73.05 1.11.75 1.11.75.65 1.1 1.7.8 2.1.6.07-.47.26-.8.46-.98-1.6-.18-3.3-.8-3.3-3.56 0-.79.28-1.43.74-1.94-.07-.18-.32-.92.07-1.9 0 0 .6-.2 1.98.74a6.9 6.9 0 0 1 3.6 0c1.37-.94 1.97-.75 1.97-.75.4 1 .15 1.73.08 1.91.46.5.74 1.15.74 1.94 0 2.77-1.7 3.38-3.32 3.56.27.22.5.67.5 1.35v2c0 .2.13.42.5.35A7.2 7.2 0 0 0 8 .8Z"/></svg></a>'
  '<a href="https://harmonixfi.github.io/harmonix-docs-v2/harmonix-docs-v2.html" aria-label="Harmonix Docs"><svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M2.5 3.2C2.5 2.54 3.04 2 3.7 2h8.6c.66 0 1.2.54 1.2 1.2v9.6c0 .66-.54 1.2-1.2 1.2H3.7c-.66 0-1.2-.54-1.2-1.2V3.2Z"/><path d="M5.5 2v12M8.5 5.5h3M8.5 8h3" stroke-linecap="round"/></svg></a>'
  '</div></div>')

# OG app lockup: cream tile + dark loop mark (restore if a previous cycle removed it)
if '<rect y="0.0996094"' not in shell_head:
    shell_head = shell_head.replace('aria-label="Harmonix logo">',
        'aria-label="Harmonix logo"><rect y="0.0996094" width="56" height="56" rx="16.925" fill="#F1F1EB"></rect>', 1)
shell_head = shell_head.replace('C29.8701 17.1871 26.3825 20.5101 23.519 25.4528L22.0539 24.6069Z" fill="#F1F1EB">',
                                'C29.8701 17.1871 26.3825 20.5101 23.519 25.4528L22.0539 24.6069Z" fill="#173132">')
assert '<rect y="0.0996094"' in shell_head, "logo tile missing"

if '<div class="audit">Audited by <strong>Verichains</strong></div>' in shell_head:
    shell_head = shell_head.replace('<div class="audit">Audited by <strong>Verichains</strong></div>', SIDE_FOOT)
else:
    shell_head, _n = re.subn(r'<div class="side-foot">.*?</div></div>', SIDE_FOOT, shell_head, count=1, flags=re.S)
    assert _n == 1, "existing side-foot not replaced"
assert 'Zenith audit report' in shell_head, "zenith logo not injected"

# ---------- 1c. home strip fixes: Asset column header, drop text asset col, delta-neutral USDC icon ----------
home_main = home_main.replace(
    '<span>Vault</span><span>Net APY</span><span>TVL</span><span>Asset</span><span>Rewards</span><span></span>',
    '<span>Asset</span><span>Net APY</span><span>TVL</span><span>Rewards</span><span></span>')
home_main = re.sub(r'\s*<div class="row"><span class="k">Asset</span><span class="v">[^<]*</span></div>', '', home_main)
assert 'class="k">Asset<' not in home_main

_usdc_head_icon = None  # set below once USDC_ICON is defined; delta swap happens in a function

def fix_delta_icon(html, usdc_icon):
    pat = re.compile(r'<span class="coin hype" aria-hidden="true">(?:(?!</span>).)*</span>(\s*<h3>USDC — \$HYPE Delta Neutral Vault</h3>)', re.S)
    out, n = pat.subn(lambda m: usdc_icon + m.group(1), html, count=1)
    if n == 0:
        # already swapped in a previous build cycle — verify and pass through
        assert re.search(r'fill="#2775CA"[^\0]*?<h3>USDC — \$HYPE Delta Neutral Vault</h3>', html), "delta-neutral icon missing entirely"
        return html
    return out

base_css = base_css.replace('minmax(280px, 2fr) 0.8fr 1fr 0.9fr 0.9fr 128px', 'minmax(280px, 2fr) 0.9fr 1.1fr 1fr 128px')

# cinematic tile-style backdrop: dark vignetted edges, luminous bloom behind the content
_old_bg = """      radial-gradient(1300px 750px at 55% -12%, rgba(150, 200, 165, 0.50), transparent 62%),
      radial-gradient(950px 620px at 78% 22%, rgba(88, 146, 108, 0.42), transparent 66%),
      radial-gradient(800px 560px at 18% 38%, rgba(64, 116, 85, 0.35), transparent 68%),
      linear-gradient(180deg, #35634a 0%, #24503a 26%, #17392a 52%, #0c231a 78%, #071510 100%);"""
_prev_bg = """      radial-gradient(140% 140% at 50% 42%, transparent 52%, rgba(2, 9, 5, 0.62) 100%),
      radial-gradient(1150px 820px at 64% 36%, rgba(86, 168, 116, 0.50), transparent 60%),
      radial-gradient(760px 560px at 22% 76%, rgba(40, 96, 64, 0.34), transparent 70%),
      radial-gradient(1700px 1150px at 50% 46%, rgba(22, 56, 38, 0.55), transparent 82%),
      linear-gradient(155deg, #0b1a12 0%, #143726 36%, #0e2a1a 62%, #05100a 100%);"""
# marketing-tile haze on a graphite-grey ground
_prev_bg2 = """      radial-gradient(150% 150% at 50% 44%, transparent 55%, rgba(4, 13, 9, 0.50) 100%),
      radial-gradient(1400px 950px at 63% 38%, rgba(98, 172, 126, 0.42), transparent 64%),
      radial-gradient(1000px 700px at 30% 70%, rgba(52, 108, 76, 0.28), transparent 72%),
      linear-gradient(150deg, #13291d 0%, #1d4530 38%, #143223 68%, #0b2015 100%);"""
_prev_bg3 = """      radial-gradient(150% 150% at 50% 44%, transparent 55%, rgba(6, 7, 7, 0.50) 100%),
      radial-gradient(1400px 950px at 63% 38%, rgba(150, 160, 152, 0.20), transparent 64%),
      radial-gradient(1000px 700px at 30% 70%, rgba(110, 122, 114, 0.14), transparent 72%),
      linear-gradient(150deg, #1c1e1d 0%, #26292a 38%, #1d201e 68%, #131514 100%);"""
_prev_bg4 = """      radial-gradient(150% 150% at 50% 44%, transparent 58%, rgba(0, 0, 0, 0.45) 100%),
      radial-gradient(1200px 800px at 60% 28%, rgba(255, 255, 255, 0.04), transparent 60%),
      linear-gradient(160deg, #17181a 0%, #101112 45%, #0b0c0d 100%);"""
# OG app dark-mode ground: deep teal #0F2122 family
_new_bg = """      radial-gradient(150% 150% at 50% 44%, transparent 58%, rgba(0, 0, 0, 0.40) 100%),
      radial-gradient(1200px 800px at 60% 28%, rgba(226, 246, 161, 0.05), transparent 60%),
      linear-gradient(160deg, #142c2d 0%, #0f2122 48%, #0b1a1b 100%);"""
for _cand in (_old_bg, _prev_bg, _prev_bg2, _prev_bg3, _prev_bg4):
    if _cand in base_css:
        base_css = base_css.replace(_cand, _new_bg)
        break
else:
    assert "rgba(226, 246, 161, 0.05)" in base_css, "backdrop missing entirely"

# family-style contrast: near-black elevated cards, brighter text
for _old, _new in [
    ("--glass: rgba(255, 255, 255, 0.08);", "--glass: rgba(17, 19, 18, 0.58);"),
    ("--glass-strong: rgba(255, 255, 255, 0.12);", "--glass-strong: rgba(30, 32, 31, 0.72);"),
    ("--glass-inner: rgba(255, 255, 255, 0.07);", "--glass-inner: rgba(255, 255, 255, 0.055);"),
    ("--glass-border: rgba(255, 255, 255, 0.13);", "--glass-border: rgba(255, 255, 255, 0.10);"),
    ("--text-0: #f4f7f3;", "--text-0: #f8faf8;"),
    ("--text-1: rgba(244, 247, 243, 0.72);", "--text-1: rgba(248, 250, 248, 0.80);"),
    ("--text-2: rgba(244, 247, 243, 0.52);", "--text-2: rgba(248, 250, 248, 0.56);"),
    # gemini-dark elevated pills
    ("--glass: rgba(17, 19, 18, 0.58);", "--glass: rgba(30, 31, 33, 0.62);"),
    ("--glass-strong: rgba(30, 32, 31, 0.72);", "--glass-strong: rgba(43, 45, 47, 0.72);"),
    ("background: #101211;", "background: #0b0c0c;"),
    ("background: rgba(15, 17, 16, 0.62);", "background: rgba(18, 19, 20, 0.66);"),
    # OG app dark-mode exact surfaces
    ("--glass: rgba(30, 31, 33, 0.62);", "--glass: rgba(24, 49, 50, 0.66);"),
    ("--glass-strong: rgba(43, 45, 47, 0.72);", "--glass-strong: rgba(28, 59, 60, 0.76);"),
    ("background: #0b0c0c;", "background: #0c191a;"),
    ("background: rgba(18, 19, 20, 0.66);", "background: rgba(12, 25, 26, 0.72);"),
    ("background: rgba(18, 19, 20, 0.80);", "background: rgba(12, 25, 26, 0.86);"),
    ("background: rgba(18, 19, 20, 0.88);", "background: rgba(12, 25, 26, 0.90);"),
    ("background: rgba(26, 27, 28, 0.94);", "background: rgba(16, 35, 36, 0.94);"),
    ("--text-2: rgba(248, 250, 248, 0.56);", "--text-2: #a1a1aa;"),
]:
    if _old in base_css:
        base_css = base_css.replace(_old, _new)

# neutralize the remaining green-tinted chrome surfaces
for _old, _new in [
    ("background: #061410;", "background: #101211;"),
    ("background: rgba(6, 18, 13, 0.60);", "background: rgba(15, 17, 16, 0.62);"),
    ("background: rgba(18, 19, 20, 0.80);", "background: rgba(18, 19, 20, 0.80);"),
    ("background: rgba(18, 19, 20, 0.88);", "background: rgba(18, 19, 20, 0.88);"),
]:
    if _old in base_css:
        base_css = base_css.replace(_old, _new)

# ---------- 2. nav hrefs + active state ----------
# ---------- 1d. mobile shell: fixed glass header + bottom tab bar ----------
_lockup_m = re.search(r'<svg viewBox="0 0 236 57".*?</svg>', shell_head, re.S)
LOCKUP_SVG = _lockup_m.group(0) if _lockup_m else ''

MOBILE_HTML = ('<header class="mhead">'
  '<a href="index.html" class="mlogo-a" aria-label="Harmonix home">' + LOCKUP_SVG.replace('aria-label="Harmonix logo"', 'aria-label="Harmonix logo" class="mlogo"') + '</a>'
  '<span style="display:flex;gap:8px;align-items:center"><button class="theme-btn" aria-label="Toggle light/dark theme"></button>'
  '<button class="connect-btn">Connect</button></span>'
  '</header>'
  '<nav class="mnav" aria-label="Mobile">'
  '<a class="mn" href="index.html"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75"/></svg><span>Home</span></a>'
  '<a class="mn" href="perps.html"><svg width="17" height="17" viewBox="0 0 15 15" fill="none" aria-hidden="true"><path d="M2 11.5 5.5 7l2.5 2.5L13 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M9.5 3.5H13V7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Perps</span></a>'
  '<a class="mn" href="swap.html"><svg width="17" height="17" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10.47 2.22a.75.75 0 0 1 1.06 0l2.25 2.25a.75.75 0 0 1 0 1.06l-2.25 2.25a.75.75 0 1 1-1.06-1.06l.97-.97H5.75a.75.75 0 0 1 0-1.5h5.69l-.97-.97a.75.75 0 0 1 0-1.06Zm-4.94 6a.75.75 0 0 1 0 1.06l-.97.97h5.69a.75.75 0 0 1 0 1.5H4.56l.97.97a.75.75 0 1 1-1.06 1.06l-2.25-2.25a.75.75 0 0 1 0-1.06l2.25-2.25a.75.75 0 0 1 1.06 0Z" clip-rule="evenodd"/></svg><span>Swap</span></a>'
  '<a class="mn" href="stake.html"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75 2.25 12l4.179 2.25m0-4.5 5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0 4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0-5.571 3-5.571-3"/></svg><span>Stake</span></a>'
  '<a class="mn" href="portfolio.html"><svg width="17" height="17" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M5.33 17.33c0-2.51 0-3.77.78-4.55.78-.78 2.04-.78 4.56-.78h10.66c2.52 0 3.77 0 4.55.78.78.78.78 2.04.78 4.55V20c0 3.77 0 5.66-1.17 6.83C24.32 28 22.44 28 18.67 28h-5.34c-3.77 0-5.65 0-6.83-1.17-1.17-1.17-1.17-3.06-1.17-6.83v-2.67Z"/><path stroke-linecap="round" d="M21.33 10.67V9.33a5.33 5.33 0 0 0-10.66 0v1.34"/></svg><span>Portfolio</span></a>'
  '</nav>')

if 'hmx_theme' not in shell_head:
    shell_head = shell_head.replace('<meta charset="utf-8">',
        '<meta charset="utf-8">\n<script>document.documentElement.setAttribute("data-theme", (function(){try{return localStorage.getItem("hmx_theme")||"light"}catch(e){return "light"}})());</script>', 1)
assert 'hmx_theme' in shell_head

if 'name="viewport"' not in shell_head:
    shell_head = shell_head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">', 1)
assert 'name="viewport"' in shell_head

if 'class="mhead"' not in shell_head:
    shell_head = shell_head.replace('<div class="app">', MOBILE_HTML + '\n<div class="app">', 1)
if 'mhead' in shell_head and 'theme-btn' not in shell_head.split('<div class="app">')[0]:
    shell_head = shell_head.replace('<button class="connect-btn">Connect</button></header>',
        '<span style="display:flex;gap:8px;align-items:center"><button class="theme-btn" aria-label="Toggle light/dark theme"></button><button class="connect-btn">Connect</button></span></header>', 1)
assert 'class="mhead"' in shell_head

NAV = {
    "Home": "index.html",
    "Protection Vault": "protection.html",
    "Stake HAR": "stake-har.html",
    "Yield Markets": "index.html",
    "Perps": "perps.html",
    "Swap": "swap.html",
    "Stake": "stake.html",
    "Portfolio": "portfolio.html",
    "Analytics": "analytics.html",
    "Referral Program": "referral.html",
    "Points": "points.html",
}

def make_shell(active_label, title):
    h = shell_head
    for label, href in NAV.items():
        pat = re.compile(r'<a href="[^"]*"( class="active" aria-current="page")?>(\s*<svg(?:(?!</a>).)*?</svg>\s*' + re.escape(label) + r'\s*</a>)', re.S)
        cls = ' class="active" aria-current="page"' if label == active_label else ''
        h, n = pat.subn(lambda m: '<a href="' + href + '"' + cls + '>' + m.group(2), h, count=1)
        assert n == 1, "nav link not found: " + label
    h = h.replace("<title>Harmonix — Yield Markets (Glass Redesign)</title>",
                  "<title>Harmonix — " + title + "</title>")
    return h

TOPBAR = '''    <div class="topbar">
      <h1>{title}</h1>
      <div class="topbar-actions">
        <button class="theme-btn" aria-label="Toggle light/dark theme"></button>
        <button class="chain-btn" aria-haspopup="listbox" aria-label="Switch network, current: HyperEVM">
          <span class="cicon" aria-hidden="true"><svg viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="11" fill="#072723"/><path d="M18.9666 10.8871C18.9812 12.1981 18.7068 13.4507 18.1679 14.6475C17.3984 16.3517 15.5534 17.7452 13.8685 16.2619C12.4945 15.0529 12.2396 12.5986 10.181 12.2393C7.45717 11.9092 7.39163 15.0675 5.61217 15.4244C3.62879 15.8274 2.9709 12.4918 3.00004 10.9769C3.02917 9.46209 3.43215 7.33305 5.15578 7.33305C7.13915 7.33305 7.27267 10.336 9.79014 10.1734C12.2833 10.0035 12.327 6.87908 13.9559 5.54146C15.3615 4.3859 17.0148 5.23315 17.8426 6.62418C18.6097 7.91083 18.9472 9.42082 18.9641 10.8871H18.9666Z" fill="#50D2C1"/></svg></span>
          HyperEVM
          <svg class="chev" width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <button class="connect-btn">Connect wallet</button>
      </div>
    </div>
'''

_MNAV_MAP = {"Home": "index.html", "Perps": "perps.html", "Swap": "swap.html", "Stake": "stake.html", "Portfolio": "portfolio.html"}

def mark_mnav(html, active):
    mh = _MNAV_MAP.get(active)
    if mh:
        html = html.replace('class="mn" href="' + mh + '"', 'class="mn active" href="' + mh + '"', 1)
    return html

def page(fname, active, title, content):
    html = make_shell(active, title)
    html += '<main class="main">\n' + TOPBAR.format(title=title) + content + '\n  </main>\n' + SHELL_TAIL
    html = mark_mnav(html, active)
    open(os.path.join(OUT, fname), "w").write(html)
    print("wrote", fname, len(html))

# ---------- 3. extra shared CSS for subpages ----------
EXTRA_CSS = """
  /* ---------- subpage components ---------- */
  .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 22px; }
  .tile {
    background: var(--glass); border: 1px solid var(--glass-border); border-radius: var(--radius);
    box-shadow: var(--shadow); padding: 16px 20px;
    backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
  }
  .tile .label { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.11em; color: var(--text-2); }
  .tile .value { font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; margin-top: 3px; letter-spacing: -0.01em; }
  .tile .value.lime { color: var(--lime); }
  .tile .sub { font-size: 11.5px; color: var(--text-3); }

  .panel {
    background: var(--glass); border: 1px solid var(--glass-border); border-radius: var(--radius);
    box-shadow: var(--shadow); padding: 20px;
    backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
  }
  .panel h2 { margin: 0 0 4px; font-size: 17px; font-weight: 600; letter-spacing: -0.01em; }
  .panel .muted { color: var(--text-2); font-size: 13px; }

  .empty-state { text-align: center; padding: 56px 20px; color: var(--text-2); font-size: 14px; }
  .empty-state .big { font-size: 16px; font-weight: 600; color: var(--text-1); margin-bottom: 6px; }
  .empty-state .connect-btn { margin-top: 18px; }

  .ghost-btn {
    background: rgba(47, 174, 78, 0.16); color: #62d98b; border: none; border-radius: var(--radius-sm);
    font: 600 13.5px var(--font); padding: 10px 22px; cursor: pointer;
    box-shadow: inset 0 0 0 1px rgba(98, 217, 139, 0.22);
    transition: background 0.16s, color 0.16s;
  }
  .ghost-btn:hover { background: linear-gradient(180deg, #41cc63, #2cb04e); color: #fff; }

  /* centered card pages (swap / stake) */
  .center-wrap { display: flex; justify-content: center; padding-top: 12px; }
  .center-card { width: 440px; max-width: 100%; }
  .swap-box {
    background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: var(--radius-sm);
    padding: 14px 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px;
  }
  .swap-box + .swap-box { margin-top: 8px; }
  .swap-box .amt { font-size: 24px; font-weight: 600; color: var(--text-0); font-variant-numeric: tabular-nums; }
  .swap-box .lbl { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-2); margin-bottom: 4px; }
  .swap-box .bal { font-size: 11px; color: var(--text-3); margin-top: 4px; }
  .token-pill {
    display: inline-flex; align-items: center; gap: 7px; background: var(--glass-strong);
    border: 1px solid var(--glass-border); border-radius: 999px; padding: 6px 12px 6px 7px;
    font-weight: 600; font-size: 14px; color: var(--text-0); flex: none;
  }
  .token-pill .coin { width: 22px; height: 22px; }
  .swap-arrow { display: flex; justify-content: center; margin: 2px 0; color: var(--text-2); }
  .kv { display: flex; justify-content: space-between; font-size: 12.5px; color: var(--text-2); padding: 4px 2px; }
  .kv b { color: var(--text-1); font-weight: 500; font-variant-numeric: tabular-nums; }
  .cta {
    width: 100%; margin-top: 14px; padding: 13px; border: none; border-radius: var(--radius-sm);
    background: linear-gradient(180deg, #38bd58, #27a246); color: #fff; font: 600 14.5px var(--font);
    cursor: pointer; box-shadow: inset 0 1px 0 rgba(255,255,255,0.28), 0 4px 16px rgba(47,174,78,0.22);
    transition: background 0.16s, box-shadow 0.16s;
  }
  .cta:hover { background: linear-gradient(180deg, #41cc63, #2cb04e); }
  .fine { text-align: center; font-size: 11px; color: var(--text-3); margin-top: 12px; }

  /* tables (points / stake validators) */
  .gtable { width: 100%; border-collapse: collapse; font-size: 13.5px; }
  .gtable th { text-align: left; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.11em; color: var(--text-2); font-weight: 500; padding: 8px 12px; }
  .gtable td { padding: 11px 12px; border-top: 1px solid var(--glass-border); color: var(--text-1); font-variant-numeric: tabular-nums; }
  .gtable td:first-child, .gtable th:first-child { padding-left: 4px; }
  .gtable .r { text-align: right; }
  .gtable th.r { text-align: right; }
  .mono { color: var(--text-1); }

  /* ---------- perps ---------- */
  .perps-grid { display: grid; grid-template-columns: 1fr 300px 320px; gap: 12px; align-items: start; }
  .pairbar {
    grid-column: 1 / -1; display: flex; align-items: center; gap: 28px; flex-wrap: wrap;
    background: var(--glass); border: 1px solid var(--glass-border); border-radius: var(--radius);
    box-shadow: var(--shadow); padding: 12px 20px;
    backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
  }
  .pairbar .pair { display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 16px; }
  .pairbar .pair .coin { width: 26px; height: 26px; }
  .pstat .label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-2); }
  .pstat .v { font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; margin-top: 1px; }
  .pstat .v.up { color: #62d98b; }
  .pstat .v.lime { color: var(--lime); }

  .chart-panel { padding: 14px 16px 8px; }
  .tf { display: flex; gap: 4px; margin-bottom: 10px; }
  .tf button {
    background: transparent; border: none; border-radius: 7px; color: var(--text-2);
    font: 500 12px var(--font); padding: 5px 11px; cursor: pointer;
  }
  .tf button.active { background: rgba(215, 251, 95, 0.14); color: var(--lime); }
  .candles { width: 100%; height: auto; display: block; }

  .ob-head, .ob-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; font-size: 12px; font-variant-numeric: tabular-nums; }
  .ob-head { color: var(--text-2); font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.08em; padding: 0 6px 8px; }
  .ob-row { padding: 3px 6px; border-radius: 5px; position: relative; color: var(--text-1); }
  .ob-row span:nth-child(2), .ob-row span:nth-child(3) { text-align: right; }
  .ob-row.ask span:first-child { color: #f2716e; }
  .ob-row.bid span:first-child { color: #62d98b; }
  .ob-row .depth { position: absolute; right: 0; top: 0; bottom: 0; border-radius: 5px; z-index: -1; }
  .ob-row.ask .depth { background: rgba(242, 113, 110, 0.10); }
  .ob-row.bid .depth { background: rgba(98, 217, 139, 0.10); }
  .ob-row { z-index: 0; }
  .spread { text-align: center; font-size: 11.5px; color: var(--text-2); padding: 7px 0; border-top: 1px solid var(--glass-border); border-bottom: 1px solid var(--glass-border); margin: 6px 0; }

  .seg { display: flex; gap: 4px; background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: 999px; padding: 3px; }
  .seg button { flex: 1; background: transparent; border: none; border-radius: 999px; color: var(--text-2); font: 600 12.5px var(--font); padding: 7px 0; cursor: pointer; }
  .seg button.active { background: rgba(255, 255, 255, 0.10); color: var(--text-0); }
  .seg.buysell { margin-top: 10px; }
  .seg.buysell button.buy.active { background: linear-gradient(180deg, #38bd58, #27a246); color: #fff; }
  .seg.buysell button.sell.active { background: #a03c3a; color: #fff; }

  .field { margin-top: 10px; }
  .field .flabel { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-2); margin-bottom: 5px; }
  .field .fbox {
    display: flex; justify-content: space-between; align-items: center;
    background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: var(--radius-sm);
    padding: 10px 14px; font-size: 15px; font-weight: 600; color: var(--text-3);
  }
  .field .fbox .unit { color: var(--text-2); font-size: 12.5px; font-weight: 500; }
  .trade-rows { margin-top: 12px; }
  .positions-panel { grid-column: 1 / -1; }
  .ptabs { display: flex; gap: 2px; border-bottom: 1px solid var(--glass-border); margin-bottom: 0; }
  .ptabs button { background: transparent; border: none; color: var(--text-2); font: 500 13px var(--font); padding: 10px 14px; cursor: pointer; border-bottom: 2px solid transparent; }
  .ptabs button.active { color: var(--text-0); border-bottom-color: var(--lime); }

  @media (max-width: 1200px) { .perps-grid { grid-template-columns: 1fr 1fr; } .chart-wrap { grid-column: 1 / -1; } }

  /* referral / points */
  .code-box {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    background: var(--glass-inner); border: 1px dashed var(--glass-border-hover); border-radius: var(--radius-sm);
    padding: 14px 18px; font-size: 18px; font-weight: 600; letter-spacing: 0.06em;
  }
  .steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-top: 18px; }
  .step { background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: var(--radius-sm); padding: 14px 16px; font-size: 13px; color: var(--text-1); }
  .step b { display: block; color: var(--text-0); margin-bottom: 4px; font-weight: 600; }
  .step .n { color: var(--lime); font-weight: 600; margin-right: 6px; }
"""

open(os.path.join(OUT, "assets", "style.css"), "w").write(base_css + EXTRA_CSS)

# token icon snippets (from app.harmonix.fi)
HYPE_ICON = '<span class="coin" aria-hidden="true"><svg viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="11" fill="#072723"/><path d="M18.9666 10.8871C18.9812 12.1981 18.7068 13.4507 18.1679 14.6475C17.3984 16.3517 15.5534 17.7452 13.8685 16.2619C12.4945 15.0529 12.2396 12.5986 10.181 12.2393C7.45717 11.9092 7.39163 15.0675 5.61217 15.4244C3.62879 15.8274 2.9709 12.4918 3.00004 10.9769C3.02917 9.46209 3.43215 7.33305 5.15578 7.33305C7.13915 7.33305 7.27267 10.336 9.79014 10.1734C12.2833 10.0035 12.327 6.87908 13.9559 5.54146C15.3615 4.3859 17.0148 5.23315 17.8426 6.62418C18.6097 7.91083 18.9472 9.42082 18.9641 10.8871H18.9666Z" fill="#50D2C1"/></svg></span>'
USDC_ICON = '<span class="coin" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 47 47" fill="none"><path d="M23.6665 46.5C36.4124 46.5 46.6665 36.2459 46.6665 23.5C46.6665 10.7541 36.4124 0.5 23.6665 0.5C10.9206 0.5 0.666504 10.7541 0.666504 23.5C0.666504 36.2459 10.9206 46.5 23.6665 46.5Z" fill="#2775CA"/><path d="M29.991 27.139C29.991 23.7849 27.9785 22.6349 23.9535 22.1558C21.0785 21.7724 20.5035 21.0058 20.5035 19.664C20.5035 18.3221 21.4619 17.4599 23.3785 17.4599C25.1035 17.4599 26.0619 18.0349 26.541 19.4724C26.6369 19.7599 26.9244 19.9515 27.2119 19.9515H28.7451C29.1285 19.9515 29.416 19.664 29.416 19.2808V19.1849C29.0326 17.0765 27.3076 15.4474 25.1035 15.2558V12.9558C25.1035 12.5724 24.816 12.2849 24.3369 12.189H22.8994C22.516 12.189 22.2285 12.4765 22.1326 12.9558V15.1599C19.2576 15.5433 17.4369 17.4599 17.4369 19.8558C17.4369 23.0183 19.3535 24.264 23.3785 24.7433C26.0619 25.2224 26.9244 25.7974 26.9244 27.3308C26.9244 28.8642 25.5826 29.9183 23.7619 29.9183C21.2701 29.9183 20.4076 28.864 20.1201 27.4265C20.0244 27.0433 19.7369 26.8515 19.4494 26.8515H17.8201C17.4369 26.8515 17.1494 27.139 17.1494 27.5224V27.6183C17.5326 30.014 19.066 31.739 22.2285 32.2183V34.5183C22.2285 34.9015 22.516 35.189 22.9951 35.2849H24.4326C24.816 35.2849 25.1035 34.9974 25.1994 34.5183V32.2183C28.0744 31.739 29.991 29.7265 29.991 27.139Z" fill="white"/><path d="M18.7775 37.2032C11.3025 34.52 7.46905 26.1825 10.2484 18.8032C11.6859 14.7782 14.8484 11.7116 18.7775 10.2741C19.1609 10.0825 19.3525 9.79502 19.3525 9.3157V7.97411C19.3525 7.5907 19.1609 7.3032 18.7775 7.20752C18.6815 7.20752 18.49 7.20752 18.394 7.3032C9.28996 10.1782 4.30654 19.8575 7.18154 28.9616C8.90654 34.3282 13.0275 38.4491 18.394 40.1741C18.7775 40.3657 19.1609 40.1741 19.2565 39.7907C19.3525 39.695 19.3525 39.5991 19.3525 39.4075V38.0657C19.3525 37.7782 19.065 37.395 18.7775 37.2032ZM28.9359 7.3032C28.5525 7.11161 28.169 7.3032 28.0734 7.68661C27.9775 7.78252 27.9775 7.8782 27.9775 8.07002V9.41161C27.9775 9.79502 28.265 10.1782 28.5525 10.37C36.0275 13.0532 39.8609 21.3907 37.0816 28.77C35.644 32.795 32.4815 35.8616 28.5525 37.2991C28.169 37.4907 27.9775 37.7782 27.9775 38.2575V39.5991C27.9775 39.9825 28.169 40.27 28.5525 40.3657C28.6484 40.3657 28.84 40.3657 28.9359 40.27C38.04 37.395 43.0234 27.7157 40.1484 18.6116C38.4234 13.1491 34.2066 9.0282 28.9359 7.3032Z" fill="white"/></svg></span>'

home_main = fix_delta_icon(home_main, USDC_ICON)
if 'theme-btn' not in home_main:
    home_main = home_main.replace('<div class="topbar-actions">',
        '<div class="topbar-actions">\n        <button class="theme-btn" aria-label="Toggle light/dark theme"></button>', 1)
assert 'theme-btn' in home_main, "home topbar toggle missing"

# ---------- 4. candles svg ----------
random.seed(7)
def candles_svg():
    w, h, n = 760, 300, 46
    cw = w / n
    price = 44.0
    out = ['<svg class="candles" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (w, h)]
    # grid lines
    for gy in range(1, 6):
        y = h * gy / 6
        out.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>' % (y, w, y))
    lo_p, hi_p = 42.0, 46.5
    def ymap(p): return h - (p - lo_p) / (hi_p - lo_p) * h
    for i in range(n):
        o = price
        c = price + random.uniform(-0.55, 0.62)
        c = max(lo_p + 0.2, min(hi_p - 0.2, c))
        hi = max(o, c) + random.uniform(0.05, 0.35)
        lo = min(o, c) - random.uniform(0.05, 0.35)
        color = "#4fc776" if c >= o else "#e0605d"
        x = i * cw + cw * 0.5
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (x, ymap(hi), x, ymap(lo), color))
        bx = i * cw + cw * 0.18
        bw = cw * 0.64
        y1, y2 = ymap(max(o, c)), ymap(min(o, c))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="%s"/>' % (bx, y1, bw, max(2, y2 - y1), color))
        price = c
    # last price line
    out.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="rgba(215,251,95,0.5)" stroke-width="1" stroke-dasharray="4 4"/>' % (ymap(price), w, ymap(price)))
    out.append('<rect x="%d" y="%.1f" width="52" height="18" rx="4" fill="#2c4a1f"/><text x="%d" y="%.1f" font-size="11" fill="#d7fb5f" font-family="Poppins, sans-serif">%.2f</text>' % (w-56, ymap(price)-9, w-52, ymap(price)+4, price))
    out.append('</svg>')
    return "".join(out), price

CANDLES, LAST = candles_svg()
CANDLES2, LAST2 = candles_svg()

def orderbook(center):
    rows = []
    p = center + 0.30
    for i in range(6):
        sz = random.uniform(80, 2400)
        rows.append('<div class="ob-row ask"><span>%.2f</span><span>%.1f</span><span>%.1f</span><span class="depth" style="width:%d%%"></span></div>' % (p, sz, sz*1.4, random.randint(12, 85)))
        p -= 0.05
    rows.append('<div class="spread">Spread 0.05 (0.011%)</div>')
    p = center - 0.02
    for i in range(6):
        sz = random.uniform(80, 2400)
        rows.append('<div class="ob-row bid"><span>%.2f</span><span>%.1f</span><span>%.1f</span><span class="depth" style="width:%d%%"></span></div>' % (p, sz, sz*1.4, random.randint(12, 85)))
        p -= 0.05
    return "\n          ".join(rows)

TICKER_JS = '''    <script>
    (function () {
      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      document.querySelectorAll("[data-px]").forEach(function (el) {
        var p = parseFloat(el.dataset.px);
        var arrow = el.parentElement.querySelector(".mk-arrow");
        var lastDir = 0;
        setInterval(function () {
          var d = (Math.random() - 0.485) * 0.06;
          p = Math.max(0.5, p + d);
          el.textContent = p.toFixed(2);
          var dir = d >= 0 ? 1 : -1;
          el.classList.toggle("px-up", dir > 0);
          el.classList.toggle("px-down", dir < 0);
          if (arrow) {
            if (dir !== lastDir) {
              arrow.classList.remove("show");
              setTimeout(function () {
                arrow.textContent = dir > 0 ? "\\u25B2" : "\\u25BC";
                arrow.classList.toggle("px-up", dir > 0);
                arrow.classList.toggle("px-down", dir < 0);
                arrow.classList.add("show");
              }, 360);
            }
            lastDir = dir;
          }
        }, 1400);
      });
    })();
    </script>
'''

PERPS = '''    <section class="perps-grid">
      <div class="pairbar">
        <div class="pair">''' + HYPE_ICON + '''HYPE-USD <svg class="chev" width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></div>
        <div class="pstat"><div class="label">Mark</div><div class="v"><span data-px="''' + ('%.2f' % LAST) + '''">''' + ('%.2f' % LAST) + '''</span><span class="mk-arrow" aria-hidden="true"></span></div></div>
        <div class="pstat"><div class="label">24h Change</div><div class="v up">+1.04 / +2.34%</div></div>
        <div class="pstat"><div class="label">24h Volume</div><div class="v">$48,214,930</div></div>
        <div class="pstat"><div class="label">Open Interest</div><div class="v">$12,608,112</div></div>
        <div class="pstat"><div class="label">Funding / Countdown</div><div class="v lime">0.0013% <span style="color:var(--text-3);font-weight:500">42m 18s</span></div></div>
      </div>

      <div class="panel chart-panel chart-wrap">
        <div class="tf"><button data-tf="1m">1m</button><button data-tf="5m">5m</button><button data-tf="15m">15m</button><button class="active" data-tf="1h">1h</button><button data-tf="4h">4h</button><button data-tf="1d">1d</button></div>
        ''' + CANDLES + '''
        <p class="chart-cap">1h candles. Mark price ticks live with momentum colouring.</p>
      </div>

      <div class="panel">
        <div class="ptabs" style="margin:-6px -6px 10px"><button class="active" data-obtab="book">Order book</button><button data-obtab="trades">Recent trades</button></div>
        <div class="ob-wrap">
        <div class="ob-head"><span>Price</span><span>Size</span><span>Total</span></div>
        ''' + orderbook(LAST) + '''
        </div>
        <div class="tr-wrap" hidden></div>
      </div>

      <div class="panel" id="trade-panel" data-price="''' + ('%.2f' % LAST) + '''">
        <div class="seg"><button class="active">Cross</button><button id="lev-btn">20x</button><button>One-way</button></div>
        <div class="seg" style="margin-top:8px"><button class="active" data-mode="market">Market</button><button data-mode="limit">Limit</button><button data-mode="pro">Pro</button></div>
        <div class="seg buysell"><button class="buy active" data-side="long">Buy / Long</button><button class="sell" data-side="short">Sell / Short</button></div>
        <div class="trade-rows">
          <div class="kv"><span>Available to trade</span><b data-bal="USDC">0.00 USDC</b></div>
          <div class="kv"><span>Current position</span><b>0.00 HYPE</b></div>
        </div>
        <div class="field">
          <div class="flabel">Size</div>
          <div class="fbox"><input class="finput" id="size-in" inputmode="decimal" placeholder="0.00" aria-label="Order size in USDC"><span class="unit">USDC</span></div>
        </div>
        <div class="field" id="limit-field" hidden>
          <div class="flabel">Limit price</div>
          <div class="fbox"><input class="finput" id="limit-in" inputmode="decimal" placeholder="''' + ('%.2f' % LAST) + '''" aria-label="Limit price"><span class="unit">USD</span></div>
        </div>
        <button class="cta" id="trade-cta">Connect wallet to trade</button>
        <div class="trade-rows">
          <div class="kv"><span>Liquidation price</span><b id="lq">N/A</b></div>
          <div class="kv"><span>Order value</span><b id="ov">N/A</b></div>
          <div class="kv"><span>Margin required</span><b id="mr">N/A</b></div>
          <div class="kv"><span>Slippage</span><b>Est. 0.10% / Max 3%</b></div>
          <div class="kv"><span>Fees</span><b>0.0350% / 0.0150%</b></div>
        </div>
      </div>

      <div class="panel positions-panel">
        <div class="ptabs"><button class="active">Balances</button><button>Positions</button><button>Open orders</button><button>TWAP</button><button>Trade history</button><button>Funding history</button></div>
        <div class="empty-state" id="acct-note">Connect wallet to view your account</div>
      </div>
    </section>
    <p class="fine">Harmonix Perps — routed through Hyperliquid with the Harmonix builder code.</p>
''' + TICKER_JS

SWAP = '''    <section class="perps-grid">
      <div class="pairbar">
        <div class="pair">''' + HYPE_ICON + '''HYPE/USDC <span style="font-size:10px;font-weight:600;letter-spacing:0.1em;color:var(--text-2);background:var(--glass-inner);border:1px solid var(--glass-border);border-radius:999px;padding:3px 9px;">SPOT</span> <svg class="chev" width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></div>
        <div class="pstat"><div class="label">Last price</div><div class="v"><span data-px="''' + ('%.2f' % LAST2) + '''">''' + ('%.2f' % LAST2) + '''</span><span class="mk-arrow" aria-hidden="true"></span></div></div>
        <div class="pstat"><div class="label">24h Change</div><div class="v up">+0.86 / +1.94%</div></div>
        <div class="pstat"><div class="label">24h Volume</div><div class="v">$9,481,203</div></div>
        <div class="pstat"><div class="label">24h High</div><div class="v">''' + ('%.2f' % (LAST2 + 0.42)) + '''</div></div>
        <div class="pstat"><div class="label">24h Low</div><div class="v">''' + ('%.2f' % (LAST2 - 2.31)) + '''</div></div>
      </div>

      <div class="panel chart-panel chart-wrap">
        <div class="tf"><button data-tf="1m">1m</button><button data-tf="5m">5m</button><button data-tf="15m">15m</button><button class="active" data-tf="1h">1h</button><button data-tf="4h">4h</button><button data-tf="1d">1d</button></div>
        ''' + CANDLES2 + '''
        <p class="chart-cap">1h candles, HYPE/USDC spot. Last price ticks live.</p>
      </div>

      <div class="panel">
        <div class="ptabs" style="margin:-6px -6px 10px"><button class="active" data-obtab="book">Order book</button><button data-obtab="trades">Recent trades</button></div>
        <div class="ob-wrap">
        <div class="ob-head"><span>Price</span><span>Size</span><span>Total</span></div>
        ''' + orderbook(LAST2) + '''
        </div>
        <div class="tr-wrap" hidden></div>
      </div>

      <div class="panel" id="swap-panel" data-rate="''' + ('%.2f' % LAST2) + '''">
        <div class="seg"><button class="active">Market</button><button>Limit</button><button>TWAP</button></div>
        <div class="seg buysell"><button class="buy active" data-dir="buy">Buy HYPE</button><button class="sell" data-dir="sell">Sell HYPE</button></div>
        <div class="trade-rows">
          <div class="kv"><span>Available USDC</span><b data-balv="USDC">0.00</b></div>
          <div class="kv"><span>Available HYPE</span><b data-balv="HYPE">0.00</b></div>
        </div>
        <div class="field">
          <div class="flabel">You pay</div>
          <div class="fbox"><input class="finput" id="pay-in" inputmode="decimal" placeholder="0.00" aria-label="Amount you pay"><span class="unit" id="pay-unit">USDC</span></div>
        </div>
        <div class="swap-arrow" style="margin-top:8px"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 3v10m0 0 4-4m-4 4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="field" style="margin-top:2px">
          <div class="flabel">You receive</div>
          <div class="fbox"><input class="finput" id="rcv-in" readonly placeholder="0.00" aria-label="Amount you receive"><span class="unit" id="rcv-unit">HYPE</span></div>
        </div>
        <button class="cta" id="swap-cta">Connect wallet to swap</button>
        <div class="trade-rows">
          <div class="kv"><span>Rate</span><b id="rate-lbl">1 HYPE = ''' + ('%.2f' % LAST2) + ''' USDC</b></div>
          <div class="kv"><span>Max slippage</span><b>0.50%</b></div>
          <div class="kv"><span>Fees</span><b>0.0400% + builder 0.0100%</b></div>
        </div>
      </div>

      <div class="panel positions-panel">
        <div class="ptabs"><button class="active">Balances</button><button>Open orders</button><button>Trade history</button></div>
        <div class="empty-state" id="acct-note">Connect wallet to view your account</div>
      </div>
    </section>
    <p class="fine">Harmonix Spot — Hyperliquid spot markets, routed with the Harmonix builder code.</p>
''' + TICKER_JS

STAKE = '''    <div class="tiles">
      <div class="tile"><div class="label">Staking APR</div><div class="value lime">2.31%</div></div>
      <div class="tile"><div class="label">Total staked</div><div class="value">381,204 HYPE</div></div>
      <div class="tile"><div class="label">Your stake</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
    </div>
    <div class="panel">
      <h2>Stake with validators</h2>
      <p class="muted" style="margin:0 0 10px">Delegate HYPE to a validator and earn network staking rewards.</p>
      <table class="gtable">
        <thead><tr><th>Validator</th><th class="r">APR</th><th class="r">Commission</th><th class="r">Total staked</th><th class="r"></th></tr></thead>
        <tbody>
          <tr><td>Harmonix Validator</td><td class="r" style="color:#62d98b">2.31%</td><td class="r">4%</td><td class="r">204,118 HYPE</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
          <tr><td>Hyper Foundation 1</td><td class="r" style="color:#62d98b">2.28%</td><td class="r">5%</td><td class="r">122,551 HYPE</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
          <tr><td>Nansen x HypurrCollective</td><td class="r" style="color:#62d98b">2.24%</td><td class="r">5%</td><td class="r">54,535 HYPE</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
        </tbody>
      </table>
    </div>
'''

PROTECTION = '''    <div class="hero">
      <div>
        <h2>Protection Vault</h2>
        <p>Downside-protected yield. Deposit once, stay hedged automatically.</p>
      </div>
      <div class="hero-stats">
        <span>Vaults <b>1</b></span>
        <span class="sep" aria-hidden="true"></span>
        <span>Best APY <span class="apy">5.20%</span></span>
      </div>
    </div>
    <div class="panel">
      <h2>HYPE Protection Vault</h2>
      <p class="muted" style="margin:0 0 14px">Holds spot HYPE while dynamically hedging drawdowns with perps. Yield from funding and covered strategies.</p>
      <div class="tiles" style="margin-bottom:14px">
        <div class="tile"><div class="label">Net APY</div><div class="value lime">5.20%</div></div>
        <div class="tile"><div class="label">TVL</div><div class="value">$1.24M</div></div>
        <div class="tile"><div class="label">Max drawdown target</div><div class="value">-5%</div></div>
      </div>
      <button class="ghost-btn">Deposit</button>
    </div>
'''

STAKE_HAR = '''    <div class="tiles">
      <div class="tile"><div class="label">HAR price</div><div class="value">$0.042</div></div>
      <div class="tile"><div class="label">Total HAR staked</div><div class="value">18.4M</div></div>
      <div class="tile"><div class="label">Your stake</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
    </div>
    <div class="panel">
      <h2>Stake HAR</h2>
      <p class="muted" style="margin:0 0 14px">Lock HAR to boost your vault rewards and share protocol revenue. Longer locks, bigger multipliers.</p>
      <div class="steps" style="margin-top:0">
        <div class="step"><b>1 month</b>1.0x points multiplier</div>
        <div class="step"><b>3 months</b>1.5x points multiplier</div>
        <div class="step"><b>12 months</b>3.0x points multiplier</div>
      </div>
      <button class="cta" style="max-width:260px">Connect wallet to stake</button>
    </div>
'''

PORTFOLIO = '''    <div class="tiles">
      <div class="tile"><div class="label">Total balance</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Deposited</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Unclaimed rewards</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Points</div><div class="value">0</div></div>
    </div>
    <div class="panel">
      <div class="empty-state">
        <div class="big">Nothing here yet</div>
        Connect your wallet to see your deposits, positions and rewards.
        <div><button class="connect-btn">Connect wallet</button></div>
      </div>
    </div>
'''

def area_chart():
    pts = [(0,150),(60,146),(120,138),(180,140),(240,126),(300,118),(360,104),(420,96),(480,78),(540,72),(600,56),(660,44),(720,30)]
    line = " ".join("%d,%d" % p for p in pts)
    fill = "0,170 " + line + " 720,170"
    return ('<svg viewBox="0 0 720 170" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(215,251,95,0.35)"/><stop offset="1" stop-color="rgba(215,251,95,0)"/></linearGradient></defs>'
            '<polygon points="' + fill + '" fill="url(#ag)"/>'
            '<polyline points="' + line + '" fill="none" stroke="#d7fb5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="720" cy="30" r="3.5" fill="#d7fb5f"/></svg>')

ANALYTICS = '''    <div class="tiles">
      <div class="tile"><div class="label">Total value locked</div><div class="value">$7.86M</div><div class="sub">+4.2% this week</div></div>
      <div class="tile"><div class="label">Active vaults</div><div class="value">4</div></div>
      <div class="tile"><div class="label">Best APY</div><div class="value lime">8.42%</div></div>
      <div class="tile"><div class="label">Depositors</div><div class="value">1,241</div></div>
    </div>
    <div class="panel" style="margin-bottom:14px">
      <h2>TVL — last 90 days</h2>
      <p class="muted" style="margin:0 0 12px">Protocol-wide, all vaults.</p>
      ''' + area_chart() + '''
    </div>
    <div class="panel">
      <h2>TVL by vault</h2>
      <table class="gtable" style="margin-top:6px">
        <thead><tr><th>Vault</th><th class="r">TVL</th><th class="r">Share</th></tr></thead>
        <tbody>
          <tr><td>HyperEVM $KHYPE Vault</td><td class="r">$2.90M</td><td class="r">49.9%</td></tr>
          <tr><td>HyperEVM $HYPE Vault</td><td class="r">$1.99M</td><td class="r">34.3%</td></tr>
          <tr><td>USDC — $HYPE Delta Neutral</td><td class="r">$606.5K</td><td class="r">10.4%</td></tr>
          <tr><td>HIP-3 haUSDC Vault</td><td class="r">$314.3K</td><td class="r">5.4%</td></tr>
        </tbody>
      </table>
    </div>
'''

REFERRAL = '''    <div class="tiles">
      <div class="tile"><div class="label">Friends invited</div><div class="value">0</div></div>
      <div class="tile"><div class="label">Referral earnings</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Your share</div><div class="value lime">10%</div><div class="sub">of referred fees</div></div>
    </div>
    <div class="panel">
      <h2>Your referral code</h2>
      <p class="muted" style="margin:0 0 14px">Share your code — you earn 10% of your friends' fees, they get a points boost.</p>
      <div class="code-box"><span>harmonix.fi/r/••••••</span><button class="ghost-btn">Connect to reveal</button></div>
      <div class="steps">
        <div class="step"><b><span class="n">1</span>Connect</b>Link your wallet to generate a personal code.</div>
        <div class="step"><b><span class="n">2</span>Share</b>Send your link to friends and communities.</div>
        <div class="step"><b><span class="n">3</span>Earn</b>Collect a share of their fees, forever.</div>
      </div>
    </div>
'''

POINTS = '''    <div class="tiles">
      <div class="tile"><div class="label">Your points</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
      <div class="tile"><div class="label">Season</div><div class="value">S1</div><div class="sub">ends Sep 30, 2026</div></div>
      <div class="tile"><div class="label">Points distributed</div><div class="value">12.6M</div></div>
    </div>
    <div class="panel" style="margin-bottom:14px">
      <h2>How to earn</h2>
      <div class="steps" style="margin-top:10px">
        <div class="step"><b>Deposit in vaults</b>1 point per $1 per day, boosted by HAR staking.</div>
        <div class="step"><b>Trade perps &amp; swap</b>Points on volume routed through Harmonix.</div>
        <div class="step"><b>Refer friends</b>Earn 10% of your referrals' points.</div>
      </div>
    </div>
    <div class="panel">
      <h2>Leaderboard</h2>
      <table class="gtable" style="margin-top:6px">
        <thead><tr><th>Rank</th><th>Address</th><th class="r">Points</th></tr></thead>
        <tbody>
          <tr><td>1</td><td class="mono">0x7f3a…9c21</td><td class="r">842,110</td></tr>
          <tr><td>2</td><td class="mono">0x1bd4…08ee</td><td class="r">611,489</td></tr>
          <tr><td>3</td><td class="mono">0xc02f…44a7</td><td class="r">590,732</td></tr>
          <tr><td>4</td><td class="mono">0x98e1…d3b0</td><td class="r">402,175</td></tr>
          <tr><td>5</td><td class="mono">0x33aa…71c9</td><td class="r">387,960</td></tr>
        </tbody>
      </table>
    </div>
'''

# ---------- 4b. upgraded secondary pages (override the simple versions above) ----------
EXTRA2_CSS = """
  /* dashboard grids + charts */
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .grid2 > .panel { min-width: 0; }
  @media (max-width: 1150px) { .grid2 { grid-template-columns: 1fr; } }
  .tile { position: relative; overflow: hidden; }
  .tile .spark { position: absolute; right: 14px; bottom: 14px; opacity: 0.85; }
  .delta { font-size: 11.5px; font-weight: 600; margin-left: 8px; }
  .delta.up { color: #62d98b; }
  .delta.down { color: #f2716e; }
  .axis { font-size: 10px; fill: rgba(244,247,243,0.36); font-family: Poppins, sans-serif; }

  .hbar-row { display: grid; grid-template-columns: 30px minmax(120px, 220px) 1fr auto auto; gap: 12px; align-items: center; padding: 9px 2px; font-size: 13px; }
  .hbar-row + .hbar-row { border-top: 1px solid var(--glass-border); }
  .hbar-row .coin { width: 24px; height: 24px; }
  .hbar-track { height: 8px; border-radius: 4px; background: var(--glass-inner); overflow: hidden; }
  .hbar-track i { display: block; height: 100%; border-radius: 4px; background: linear-gradient(90deg, rgba(215,251,95,0.45), #d7fb5f); }
  .hbar-row .val { font-variant-numeric: tabular-nums; font-weight: 600; }
  .hbar-row .pct { font-variant-numeric: tabular-nums; color: var(--text-2); font-size: 12px; width: 48px; text-align: right; }

  .progress { height: 9px; border-radius: 5px; background: var(--glass-inner); border: 1px solid var(--glass-border); overflow: hidden; margin-top: 10px; }
  .progress i { display: block; height: 100%; border-radius: 5px; background: linear-gradient(90deg, rgba(215,251,95,0.5), #d7fb5f); }

  .avatar { width: 26px; height: 26px; border-radius: 50%; background: var(--glass-strong); border: 1px solid var(--glass-border); display: inline-grid; place-items: center; font-size: 11px; font-weight: 600; color: var(--text-1); margin-right: 9px; }

  .tier { text-align: left; }
  .tier .mult { font-size: 30px; font-weight: 600; color: var(--lime); letter-spacing: -0.02em; }
  .tier .dur { font-size: 13px; font-weight: 600; margin-bottom: 2px; }
  .tier .est { font-size: 12px; color: var(--text-2); margin: 6px 0 12px; }

  .legend { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 12px; font-size: 12.5px; color: var(--text-1); }
  .legend .sw { display: inline-block; width: 9px; height: 9px; border-radius: 3px; margin-right: 6px; }

  .you-row td { color: var(--lime) !important; font-weight: 600; }

  /* sidebar footer: audits + socials */
  .side-foot { margin-top: auto; padding: 16px 10px 4px; border-top: 1px solid rgba(255, 255, 255, 0.07); display: flex; flex-direction: column; gap: 10px; }
  .side-foot .audit-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-3); }
  .audit-logos { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; align-items: center; justify-items: start; }
  .audit-logos a { display: flex; align-items: center; opacity: 0.65; transition: opacity 0.15s; color: #cfd8d2; min-height: 24px; }
  .audit-logos a:hover { opacity: 1; }
  .audit-logos svg { height: 17px; width: auto; display: block; }
  .audit-logos a:first-child { grid-column: 1 / -1; }
  .audit-logos a:first-child svg { height: 28px; }

  /* token reward icon — global sizing (used in rows AND tiles) */
  .ricon { width: 22px; height: 22px; border-radius: 50%; overflow: hidden; display: inline-grid; place-items: center; flex: none; }
  .ricon svg { width: 100%; height: 100%; display: block; }

  /* clickable vault rows */
  a.card { text-decoration: none; color: inherit; cursor: pointer; }
  a.card:focus-visible { outline: 2px solid var(--lime); outline-offset: 2px; }

  /* kamino-style vault overview */
  .vhead { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-bottom: 14px; }
  .vhead-l { display: flex; align-items: center; gap: 14px; min-width: 0; }
  .vhead-l .coin { width: 42px; height: 42px; }
  .vhead-l h2 { margin: 0; font-size: 22px; letter-spacing: -0.01em; }
  .chip-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
  .chip-sm {
    font-size: 11px; font-weight: 500; color: var(--text-1);
    background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: 999px; padding: 3px 10px;
  }
  .chip-sm b { color: var(--text-0); font-weight: 600; }
  .vtabs { display: flex; gap: 2px; border-bottom: 1px solid var(--glass-border); margin-bottom: 16px; }
  .vtabs button { background: transparent; border: none; color: var(--text-2); font: 600 13.5px var(--font); padding: 10px 16px; cursor: pointer; border-bottom: 2px solid transparent; }
  .vtabs button.active { color: var(--text-0); border-bottom-color: var(--lime); }
  .halfmax { display: flex; gap: 6px; }
  .halfmax button {
    background: var(--glass-inner); border: 1px solid var(--glass-border); border-radius: 7px;
    color: var(--text-1); font: 600 11px var(--font); padding: 4px 10px; cursor: pointer;
  }
  .halfmax button:hover { color: var(--text-0); border-color: var(--glass-border-hover); }
  .wallet-line { display: flex; align-items: center; justify-content: space-between; font-size: 11.5px; color: var(--text-3); margin-top: 6px; }
  .legend-dot { display: inline-block; width: 8px; height: 8px; border-radius: 3px; margin-right: 6px; vertical-align: 0; }
  .growth-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 14px; }
  .growth-grid .g .n { font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; color: #62d98b; }
  .growth-grid .g .l { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.09em; color: var(--text-2); margin-top: 2px; }
  .rail { position: sticky; top: 14px; }
  @media (max-width: 1150px) { .rail { position: static; } }
  .backlink { color: var(--text-2); text-decoration: none; font-size: 13px; transition: color 0.15s; }
  .backlink:hover { color: var(--text-0); }
  .vault-hero-head { display: flex; align-items: center; gap: 14px; min-width: 0; }
  .vault-hero-head .coin { width: 40px; height: 40px; }
  .vault-hero-head h2 { margin: 0 0 2px; }
  .vault-hero-head p { margin: 0; }
  .socials { display: flex; gap: 7px; margin-top: 2px; }
  .socials a { width: 30px; height: 30px; border-radius: 8px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.09); display: grid; place-items: center; color: var(--text-1); transition: color 0.15s, background 0.15s, border-color 0.15s; }
  .socials a:hover { color: #fff; background: rgba(255, 255, 255, 0.10); border-color: rgba(255, 255, 255, 0.2); }
  .socials a:focus-visible { outline: 2px solid var(--lime); outline-offset: 1px; }

  /* living numbers: momentum colouring + crossfading arrow (benji-style) */
  .pstat .v, [data-px] { transition: color 0.45s ease; }
  .px-up { color: #62d98b !important; }
  .px-down { color: #f2716e !important; }
  .mk-arrow { display: inline-block; font-size: 9px; margin-left: 5px; vertical-align: 1px; opacity: 0; transition: opacity 0.35s ease, color 0.45s ease; }
  .mk-arrow.show { opacity: 0.9; }

  /* breathing endpoint on sparklines */
  .spark circle { animation: dotbreathe 2.6s ease-in-out infinite; }
  @keyframes dotbreathe { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

  /* interactive layer */
  .finput { background: transparent; border: none; outline: none; color: var(--text-0); font: 600 15px var(--font); width: 100%; min-width: 0; }
  .finput::placeholder { color: var(--text-3); }
  .fbox { color: var(--text-0); }
  .cta.sell { background: linear-gradient(180deg, #e0605d, #c04a47); box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 4px 16px rgba(224,96,93,0.25); }
  .cta.sell:hover { background: linear-gradient(180deg, #e8706d, #cb5350); }
  .connect-btn.addr { font-variant-numeric: tabular-nums; letter-spacing: 0.02em; }
  .toasts { position: fixed; bottom: 22px; left: 50%; transform: translateX(-50%); z-index: 120; display: flex; flex-direction: column; gap: 8px; align-items: center; pointer-events: none; }
  .toast {
    background: rgba(26, 27, 28, 0.94); border: 1px solid var(--glass-border-hover); color: var(--text-0);
    font: 500 13px var(--font); padding: 10px 20px; border-radius: 999px; white-space: nowrap; max-width: 92vw;
    overflow: hidden; text-overflow: ellipsis;
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    opacity: 0; transform: translateY(8px); transition: opacity 0.25s, transform 0.25s;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  }
  .toast.show { opacity: 1; transform: none; }

  /* quiet chart captions */
  .chart-cap { margin: 8px 2px 0; font-size: 11.5px; color: var(--text-3); }

  /* quieter column headers, benji-style muting */
  .list-head { color: var(--text-3); }
  .fine { opacity: 0.85; }

  /* living counters */
  .bignum { font-size: 24px; font-weight: 600; color: #62d98b; margin-top: 10px; font-variant-numeric: tabular-nums; }

  /* ---------- phone ---------- */
  .mhead, .mnav { display: none; }
  @media (max-width: 760px) {
    .sidebar { display: none; }
    .app { display: block; }
    .main { padding: 66px 14px 86px; }
    .mhead {
      display: flex; position: fixed; top: 0; left: 0; right: 0; z-index: 60;
      align-items: center; justify-content: space-between; padding: 10px 14px;
      background: rgba(18, 19, 20, 0.80);
      backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .mhead .mlogo-a { display: flex; }
    .mhead .mlogo { height: 22px; width: auto; display: block; }
    .mhead .connect-btn { padding: 7px 16px; font-size: 12.5px; }
    .mnav {
      display: flex; position: fixed; bottom: 0; left: 0; right: 0; z-index: 60;
      background: rgba(18, 19, 20, 0.88);
      backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding: 7px 4px calc(7px + env(safe-area-inset-bottom));
    }
    .mn { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; color: var(--text-2); text-decoration: none; font-size: 10px; font-weight: 500; padding: 3px 0; }
    .mn.active { color: var(--lime); }
    .mn:focus-visible { outline: 2px solid var(--lime); outline-offset: 1px; border-radius: 6px; }

    .topbar { padding: 12px 0 14px; }
    .topbar h1 { font-size: 21px; }
    .topbar .connect-btn, .topbar .chain-btn { display: none; }
    .banner { font-size: 12px; }
    .hero { padding: 16px 18px; }
    .hero h2 { font-size: 19px; }
    .hero-stats { width: 100%; justify-content: space-between; gap: 8px; padding: 9px 14px; font-size: 12px; }

    .section { overflow-x: visible; }
    .list-head { display: none; }
    .cards .card { min-width: 0; grid-template-columns: 1fr 1fr; gap: 12px 14px; padding: 16px; }
    .card-head { grid-column: 1 / -1; }
    .metric .label { display: block; margin-bottom: 2px; }
    .metric.apy { display: block; }
    .metric.apy .spark { margin-left: 8px; }
    .deposit-btn { grid-column: 1 / -1; width: 100%; justify-self: stretch; }

    .perps-grid { grid-template-columns: 1fr; }
    .chart-wrap { grid-column: auto; }
    .grid2, .grid2[style] { grid-template-columns: 1fr !important; }
    .growth-grid { grid-template-columns: repeat(2, 1fr); }
    .tiles { grid-template-columns: repeat(2, 1fr); }
    .tile .value { font-size: 19px; }
    .vhead-l h2 { font-size: 18px; }
    .rail { position: static; }
    .code-box { font-size: 14px; flex-wrap: wrap; }
    .pairbar { gap: 14px; padding: 12px 16px; }
    .toasts { bottom: calc(84px + env(safe-area-inset-bottom)); }
  }

  /* ---------- OG lime buttons + separator lines ---------- */
  .deposit-btn {
    display: inline-flex; align-items: center; justify-content: center; text-align: center;
    background: rgba(215, 251, 95, 0.12); color: var(--lime);
    box-shadow: inset 0 0 0 1px rgba(215, 251, 95, 0.25);
  }
  .deposit-btn:hover {
    background: linear-gradient(180deg, #e4ff78, #cdf254); color: #0a1a12;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45), 0 6px 20px rgba(215, 251, 95, 0.22);
  }
  .deposit-btn::after { content: none; }
  .ghost-btn { background: rgba(215, 251, 95, 0.12); color: var(--lime); box-shadow: inset 0 0 0 1px rgba(215, 251, 95, 0.22); }
  .ghost-btn:hover { background: linear-gradient(180deg, #e4ff78, #cdf254); color: #0a1a12; }
  .cta {
    background: linear-gradient(180deg, #e0fb6d, #cbf04f); color: #0a1a12;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 0 4px 16px rgba(215, 251, 95, 0.20);
  }
  .cta:hover { background: linear-gradient(180deg, #eaff85, #d6f95f); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.55), 0 6px 20px rgba(215, 251, 95, 0.30); }
  .cta.sell { background: linear-gradient(180deg, #e0605d, #c04a47); color: #fff; box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 4px 16px rgba(224, 96, 93, 0.25); }
  .cta.sell:hover { background: linear-gradient(180deg, #e8706d, #cb5350); }
  .connect-btn {
    background: linear-gradient(180deg, #e0fb6d, #cbf04f); color: #0a1a12; border: none; font-weight: 600;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 0 4px 16px rgba(215, 251, 95, 0.20);
  }
  .connect-btn:hover { background: linear-gradient(180deg, #eaff85, #d6f95f); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.55), 0 6px 20px rgba(215, 251, 95, 0.30); }
  .connect-btn.addr {
    background: rgba(215, 251, 95, 0.12); color: var(--lime);
    box-shadow: inset 0 0 0 1px rgba(215, 251, 95, 0.28);
  }
  .connect-btn.addr:hover { background: rgba(215, 251, 95, 0.18); }

  /* HyperEVM chain pill in lime */
  .chain-btn {
    background: rgba(215, 251, 95, 0.12); border-color: rgba(215, 251, 95, 0.28);
    color: var(--lime); font-weight: 600;
  }
  .chain-btn:hover { background: rgba(215, 251, 95, 0.18); border-color: rgba(215, 251, 95, 0.4); }
  .chain-btn .chev { opacity: 0.8; }
  .chain-btn .cicon svg circle { fill: #d7fb5f; }
  .chain-btn .cicon svg path { fill: #0a1a12; }

  .panel .kv { padding: 7px 2px; }
  .panel .kv + .kv { border-top: 1px solid rgba(255, 255, 255, 0.055); }
  .growth-grid { border-top: 1px solid rgba(255, 255, 255, 0.055); padding-top: 14px; }
  @media (max-width: 760px) {
    .cards .card .row { grid-column: 1 / -1; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 10px; }
    .cards .card .deposit-btn { margin-top: 2px; }
  }
"""
open(os.path.join(OUT, "assets", "style.css"), "a").write(EXTRA2_CSS)

KHYPE_ICON_S = '<span class="coin" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 541 541"><circle cx="270.5" cy="270.5" r="262.5" fill="#131313" stroke="#35ABD9" stroke-width="16"/><path fill="#6EE4FF" d="M436.07 269.312c.302 27.204-5.387 53.199-16.564 78.035-15.96 35.366-54.223 64.283-89.165 33.502-28.496-25.089-33.783-76.021-76.476-83.477-56.49-6.851-57.849 58.69-94.754 66.096-41.133 8.363-54.777-60.857-54.173-92.293s8.962-75.617 44.708-75.617c41.134 0 43.903 62.317 96.113 58.942 51.706-3.526 52.612-68.363 86.395-96.122 29.151-23.98 63.437-6.398 80.605 22.469 15.91 26.701 22.909 58.036 23.26 88.465z"/></svg></span>'

def spark_tile(pts, w=64, h=22, color="#d7fb5f"):
    line = " ".join("%d,%d" % p for p in pts)
    last = pts[-1]
    return ('<svg class="spark" width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true">'
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="%d" cy="%d" r="2" fill="%s"/></svg>') % (w, h, w, h, line, color, last[0], last[1], color)

def area_chart_axes():
    pts = [(70,168),(124,163),(178,152),(232,155),(286,138),(340,128),(394,111),(448,101),(502,80),(556,73),(610,54),(664,41),(718,26)]
    line = " ".join("%d,%d" % p for p in pts)
    fill = "70,190 " + line + " 718,190"
    grid = ""
    for i, lab in enumerate(["$8M", "$6M", "$4M", "$2M"]):
        y = 20 + i * 48
        grid += '<line x1="70" y1="%d" x2="718" y2="%d" stroke="rgba(255,255,255,0.05)"/>' % (y, y)
        grid += '<text class="axis" x="10" y="%d">%s</text>' % (y + 3, lab)
    xlab = ""
    for x, lab in [(70, "Apr"), (240, "May"), (410, "Jun"), (580, "Jul")]:
        xlab += '<text class="axis" x="%d" y="207">%s</text>' % (x, lab)
    return ('<svg viewBox="0 0 730 212" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="ag2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(215,251,95,0.30)"/><stop offset="1" stop-color="rgba(215,251,95,0)"/></linearGradient></defs>'
            + grid + xlab +
            '<polygon points="' + fill + '" fill="url(#ag2)"/>'
            '<polyline points="' + line + '" fill="none" stroke="#d7fb5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="718" cy="26" r="3.5" fill="#d7fb5f"/></svg>')

def volume_bars():
    random.seed(21)
    vals = [random.uniform(0.35, 1.0) for _ in range(12)]
    vals[-1] = 1.0
    bars = ""
    for i, v in enumerate(vals):
        x = 70 + i * 54
        bh = int(150 * v)
        col = "#d7fb5f" if i == len(vals) - 1 else "rgba(98,217,139,0.55)"
        bars += '<rect x="%d" y="%d" width="34" height="%d" rx="4" fill="%s"/>' % (x, 178 - bh, bh, col)
    grid = ""
    for i, lab in enumerate(["$3M", "$2M", "$1M"]):
        y = 40 + i * 46
        grid += '<line x1="70" y1="%d" x2="718" y2="%d" stroke="rgba(255,255,255,0.05)"/><text class="axis" x="10" y="%d">%s</text>' % (y, y, y + 3, lab)
    xlab = '<text class="axis" x="70" y="200">May</text><text class="axis" x="340" y="200">Jun</text><text class="axis" x="610" y="200">Jul</text>'
    return '<svg viewBox="0 0 730 205" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">' + grid + xlab + bars + '</svg>'

def drawdown_chart():
    pts = [(20,60),(80,52),(140,68),(200,58),(260,84),(320,72),(380,96),(440,88),(500,70),(560,78),(620,62),(680,55)]
    line = " ".join("%d,%d" % p for p in pts)
    return ('<svg viewBox="0 0 700 140" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="20" y="100" width="660" height="26" rx="4" fill="rgba(242,113,110,0.10)"/>'
            '<line x1="20" y1="100" x2="680" y2="100" stroke="rgba(242,113,110,0.6)" stroke-width="1" stroke-dasharray="5 4"/>'
            '<text class="axis" x="24" y="118" fill="rgba(242,113,110,0.8)">protection floor  (-5%)</text>'
            '<polyline points="' + line + '" fill="none" stroke="#62d98b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="680" cy="55" r="3.5" fill="#62d98b"/></svg>')

def net_flows():
    random.seed(11)
    vals = [random.uniform(-0.55, 1.0) for _ in range(12)]
    vals[-1] = 0.85
    zero_y = 100
    bars = ""
    for i, v in enumerate(vals):
        x = 70 + i * 54
        bh = max(4, abs(v) * 66)
        if v >= 0:
            col = "#d7fb5f" if i == len(vals) - 1 else "rgba(98,217,139,0.6)"
            bars += '<rect x="%d" y="%.1f" width="34" height="%.1f" rx="4" fill="%s"/>' % (x, zero_y - bh, bh, col)
        else:
            bars += '<rect x="%d" y="%d" width="34" height="%.1f" rx="4" fill="rgba(242,113,110,0.55)"/>' % (x, zero_y, bh)
    grid = ""
    for yy, lab in [(34, "+$1M"), (100, "$0"), (166, "-$1M")]:
        grid += '<line x1="70" y1="%d" x2="718" y2="%d" stroke="rgba(255,255,255,0.06)"/><text class="axis" x="10" y="%d">%s</text>' % (yy, yy, yy + 3, lab)
    xlab = '<text class="axis" x="70" y="196">May</text><text class="axis" x="340" y="196">Jun</text><text class="axis" x="610" y="196">Jul</text>'
    return '<svg viewBox="0 0 730 200" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">' + grid + xlab + bars + '</svg>'

COUNTER_JS = '''    <script>
    (function () {
      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      document.querySelectorAll("[data-count]").forEach(function (el) {
        var v = parseFloat(el.dataset.count);
        var step = parseFloat(el.dataset.step || "0.1");
        setInterval(function () {
          v += Math.random() * step;
          el.textContent = "+$" + v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }, 1800);
      });
    })();
    </script>
'''

ANALYTICS = '''    <div class="tiles">
      <div class="tile"><div class="label">Total value locked</div><div class="value">$7.86M<span class="delta up">+4.2% 7d</span></div>''' + spark_tile([(0,18),(9,16),(18,17),(27,13),(36,12),(45,9),(54,7),(63,4)]) + '''</div>
      <div class="tile"><div class="label">24h volume</div><div class="value">$1.92M<span class="delta up">+12.8%</span></div>''' + spark_tile([(0,14),(9,16),(18,10),(27,13),(36,8),(45,11),(54,6),(63,4)]) + '''</div>
      <div class="tile"><div class="label">Best APY</div><div class="value lime">8.42%</div><div class="sub">HIP-3 haUSDC Vault</div></div>
      <div class="tile"><div class="label">Depositors</div><div class="value">1,241<span class="delta up">+38 this week</span></div></div>
      <div class="tile"><div class="label">Protocol fees (30d)</div><div class="value">$28.4K<span class="delta up">+9.1%</span></div></div>
      <div class="tile"><div class="label">Avg. deposit</div><div class="value">$6.3K</div><div class="sub">median $940</div></div>
    </div>
    <div class="grid2" style="margin-bottom:14px">
      <div class="panel">
        <h2>TVL — last 90 days</h2>
        <p class="muted" style="margin:0 0 12px">Protocol-wide, all vaults.</p>
        ''' + area_chart_axes() + '''
      </div>
      <div class="panel">
        <h2>Weekly volume</h2>
        <p class="muted" style="margin:0 0 12px">Deposits, withdrawals and routed swaps.</p>
        ''' + volume_bars() + '''
      </div>
    </div>
    <div class="grid2" style="margin-bottom:14px">
      <div class="panel">
        <h2>Net flows — weekly</h2>
        <p class="muted" style="margin:0 0 12px">Deposits minus withdrawals.</p>
        ''' + net_flows() + '''
      </div>
      <div class="panel">
        <h2>Protocol fees — all time</h2>
        <p class="muted" style="margin:2px 0 0">Performance fees plus builder-code revenue.</p>
        <div class="bignum" data-count="153204.77" data-step="0.35">+$153,204.77</div>
        <div style="margin-top:12px">
          <div class="kv"><span>Performance fees (10% on yield)</span><b>$132.9K</b></div>
          <div class="kv"><span>Builder-code fees (perps + spot)</span><b>$20.3K</b></div>
          <div class="kv"><span>Fee switch to HAR stakers</span><b>Active — 50%</b></div>
        </div>
      </div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>TVL by vault</h2>
        <p class="muted" style="margin:0 0 6px">Share of protocol deposits.</p>
        <div class="hbar-row">''' + KHYPE_ICON_S + '''<span>HyperEVM $KHYPE</span><span class="hbar-track"><i style="width:100%"></i></span><span class="val">$2.90M</span><span class="pct">49.9%</span></div>
        <div class="hbar-row">''' + HYPE_ICON + '''<span>HyperEVM $HYPE</span><span class="hbar-track"><i style="width:69%"></i></span><span class="val">$1.99M</span><span class="pct">34.3%</span></div>
        <div class="hbar-row">''' + USDC_ICON + '''<span>USDC — $HYPE Delta Neutral</span><span class="hbar-track"><i style="width:21%"></i></span><span class="val">$606.5K</span><span class="pct">10.4%</span></div>
        <div class="hbar-row">''' + USDC_ICON + '''<span>HIP-3 haUSDC</span><span class="hbar-track"><i style="width:11%"></i></span><span class="val">$314.3K</span><span class="pct">5.4%</span></div>
      </div>
      <div class="panel">
        <h2>Vault performance</h2>
        <p class="muted" style="margin:0 0 6px">Net APY, trailing.</p>
        <table class="gtable">
          <thead><tr><th>Vault</th><th class="r">Net APY</th><th class="r">7d avg</th><th class="r">30d avg</th><th class="r">TVL Δ 7d</th></tr></thead>
          <tbody>
            <tr><td>HIP-3 haUSDC</td><td class="r" style="color:var(--lime)">8.42%</td><td class="r">8.19%</td><td class="r">7.86%</td><td class="r" style="color:#62d98b">+6.1%</td></tr>
            <tr><td>USDC — $HYPE Delta Neutral</td><td class="r" style="color:var(--lime)">7.46%</td><td class="r">7.61%</td><td class="r">7.02%</td><td class="r" style="color:#62d98b">+2.4%</td></tr>
            <tr><td>HyperEVM $KHYPE</td><td class="r" style="color:var(--lime)">3.84%</td><td class="r">3.79%</td><td class="r">3.91%</td><td class="r" style="color:#62d98b">+3.8%</td></tr>
            <tr><td>HyperEVM $HYPE</td><td class="r" style="color:var(--lime)">3.80%</td><td class="r">3.84%</td><td class="r">3.72%</td><td class="r" style="color:#f2716e">-1.2%</td></tr>
          </tbody>
        </table>
      </div>
    </div>
''' + COUNTER_JS

PORTFOLIO = '''    <div class="tiles">
      <div class="tile"><div class="label">Total balance</div><div class="value">$0.00</div><div class="sub">Across vaults, spot and perps</div></div>
      <div class="tile"><div class="label">Deposited</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Unclaimed rewards</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Points</div><div class="value">0</div><div class="sub">Season 1</div></div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>Allocation</h2>
        <p class="muted" style="margin:0 0 10px">How your balance is deployed.</p>
        <svg viewBox="0 0 160 160" style="width:150px;height:150px;display:block;margin:16px auto" aria-hidden="true">
          <circle cx="80" cy="80" r="62" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="18"/>
          <text x="80" y="76" text-anchor="middle" font-size="17" font-weight="600" fill="rgba(244,247,243,0.72)" font-family="Poppins, sans-serif">$0.00</text>
          <text x="80" y="94" text-anchor="middle" font-size="10" fill="rgba(244,247,243,0.36)" font-family="Poppins, sans-serif">no positions yet</text>
        </svg>
        <div class="legend">
          <span><span class="sw" style="background:#d7fb5f"></span>Vaults</span>
          <span><span class="sw" style="background:#62d98b"></span>Spot</span>
          <span><span class="sw" style="background:#50D2C1"></span>Perps margin</span>
          <span><span class="sw" style="background:rgba(255,255,255,0.25)"></span>Idle</span>
        </div>
      </div>
      <div class="panel">
        <h2>Positions</h2>
        <p class="muted" style="margin:0 0 6px">Vault deposits and open balances.</p>
        <table class="gtable">
          <thead><tr><th>Position</th><th class="r">Balance</th><th class="r">Net APY</th><th class="r">PnL</th></tr></thead>
          <tbody>
            <tr><td style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td></tr>
            <tr><td style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td><td class="r" style="color:var(--text-3)">—</td></tr>
          </tbody>
        </table>
        <div class="empty-state" style="padding:26px 20px 8px">
          Connect your wallet to see deposits, PnL and rewards.
          <div><button class="connect-btn" style="margin-top:14px">Connect wallet</button></div>
        </div>
      </div>
    </div>
'''

STAKE = '''    <div class="tiles">
      <div class="tile"><div class="label">Staking APR</div><div class="value lime">2.31%</div>''' + spark_tile([(0,12),(9,13),(18,10),(27,11),(36,9),(45,10),(54,7),(63,8)]) + '''</div>
      <div class="tile"><div class="label">Total staked</div><div class="value">381,204 HYPE</div><div class="sub">$16.4M</div></div>
      <div class="tile"><div class="label">Unbonding period</div><div class="value">7 days</div></div>
      <div class="tile"><div class="label">Your stake</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>Validators</h2>
        <p class="muted" style="margin:0 0 6px">Delegate HYPE and earn network staking rewards.</p>
        <table class="gtable">
          <thead><tr><th>Validator</th><th class="r">APR</th><th class="r">Commission</th><th class="r">Total staked</th><th class="r"></th></tr></thead>
          <tbody>
            <tr><td><span class="avatar">H</span>Harmonix Validator</td><td class="r" style="color:#62d98b">2.31%</td><td class="r">4%</td><td class="r">204,118</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
            <tr><td><span class="avatar">F</span>Hyper Foundation 1</td><td class="r" style="color:#62d98b">2.28%</td><td class="r">5%</td><td class="r">122,551</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
            <tr><td><span class="avatar">N</span>Nansen x HypurrCollective</td><td class="r" style="color:#62d98b">2.24%</td><td class="r">5%</td><td class="r">54,535</td><td class="r"><button class="ghost-btn">Stake</button></td></tr>
          </tbody>
        </table>
      </div>
      <div class="panel">
        <h2>How staking works</h2>
        <div class="steps" style="margin-top:10px;grid-template-columns:1fr">
          <div class="step"><b><span class="n">1</span>Delegate</b>Choose a validator and stake any amount of HYPE.</div>
          <div class="step"><b><span class="n">2</span>Earn</b>Rewards accrue every epoch and auto-compound.</div>
          <div class="step"><b><span class="n">3</span>Unstake</b>Withdraw any time — funds unlock after the 7-day unbonding period.</div>
        </div>
        <div style="margin-top:14px">
          <div class="kv"><span>Reward frequency</span><b>Every epoch (~90 min)</b></div>
          <div class="kv"><span>Auto-compounding</span><b>Yes</b></div>
          <div class="kv"><span>Points boost</span><b>1.2x while staked</b></div>
        </div>
      </div>
    </div>
'''

STAKE_HAR = '''    <div class="tiles">
      <div class="tile"><div class="label">HAR price</div><div class="value">$0.042<span class="delta up">+3.1%</span></div></div>
      <div class="tile"><div class="label">HAR staked</div><div class="value">18.4M</div><div class="sub">34% of supply</div></div>
      <div class="tile"><div class="label">Average lock</div><div class="value">5.2 mo</div></div>
      <div class="tile"><div class="label">Your stake</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
    </div>
    <div class="grid2" style="grid-template-columns: 2fr 1fr">
      <div class="panel">
        <h2>Choose a lock</h2>
        <p class="muted" style="margin:0 0 12px">Longer locks earn bigger point multipliers and a larger revenue share.</p>
        <div class="steps" style="margin-top:0">
          <div class="step tier"><div class="dur">1 month</div><div class="mult">1.0x</div><div class="est">Est. 8% APR - revenue share</div><button class="ghost-btn">Select</button></div>
          <div class="step tier" style="border-color:rgba(215,251,95,0.35)"><div class="dur">3 months</div><div class="mult">1.5x</div><div class="est">Est. 14% APR - revenue share</div><button class="ghost-btn">Select</button></div>
          <div class="step tier"><div class="dur">12 months</div><div class="mult">3.0x</div><div class="est">Est. 26% APR - revenue share</div><button class="ghost-btn">Select</button></div>
        </div>
        <button class="cta" style="max-width:280px">Connect wallet to stake</button>
      </div>
      <div class="panel">
        <h2>Why stake HAR</h2>
        <div class="steps" style="margin-top:10px;grid-template-columns:1fr">
          <div class="step"><b>Revenue share</b>A cut of protocol fees, paid in USDC.</div>
          <div class="step"><b>Points multiplier</b>Boosts every point you earn across Harmonix.</div>
          <div class="step"><b>Governance</b>Vote on new vaults and parameters.</div>
        </div>
      </div>
    </div>
'''

PROTECTION = '''    <div class="tiles">
      <div class="tile"><div class="label">Net APY</div><div class="value lime">5.20%</div>''' + spark_tile([(0,14),(9,12),(18,13),(27,10),(36,11),(45,8),(54,9),(63,7)]) + '''</div>
      <div class="tile"><div class="label">TVL</div><div class="value">$1.24M</div></div>
      <div class="tile"><div class="label">Protection floor</div><div class="value">-5%</div><div class="sub">max drawdown target</div></div>
      <div class="tile"><div class="label">Hedge cost</div><div class="value">0.9%</div><div class="sub">annualized</div></div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>HYPE Protection Vault</h2>
        <p class="muted" style="margin:0 0 12px">Vault performance vs. the protection floor, last 60 days.</p>
        ''' + drawdown_chart() + '''
        <button class="ghost-btn" style="margin-top:14px">Deposit</button>
      </div>
      <div class="panel">
        <h2>How it works</h2>
        <div class="steps" style="margin-top:10px;grid-template-columns:1fr">
          <div class="step"><b><span class="n">1</span>Deposit HYPE</b>Your spot HYPE keeps full upside exposure.</div>
          <div class="step"><b><span class="n">2</span>Automatic hedge</b>The vault buys downside protection with perps when volatility spikes.</div>
          <div class="step"><b><span class="n">3</span>Bounded drawdown</b>Losses are capped near the floor while funding and covered strategies pay the hedge.</div>
        </div>
        <div style="margin-top:12px">
          <div class="kv"><span>Withdrawals</span><b>Daily, no lock</b></div>
          <div class="kv"><span>Performance fee</span><b>10% on yield</b></div>
        </div>
      </div>
    </div>
'''

REFERRAL = '''    <div class="tiles">
      <div class="tile"><div class="label">Friends invited</div><div class="value">0</div></div>
      <div class="tile"><div class="label">Referral earnings</div><div class="value">$0.00</div></div>
      <div class="tile"><div class="label">Your share</div><div class="value lime">10%</div><div class="sub">of referred fees, forever</div></div>
      <div class="tile"><div class="label">Friend bonus</div><div class="value">1.1x</div><div class="sub">points boost for them</div></div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>Your referral link</h2>
        <p class="muted" style="margin:0 0 14px">Share your code — you earn a share of your friends' fees, they get a points boost.</p>
        <div class="code-box"><span>harmonix.fi/r/••••••</span><button class="ghost-btn">Connect to reveal</button></div>
        <div class="steps">
          <div class="step"><b><span class="n">1</span>Connect</b>Link your wallet to generate a personal code.</div>
          <div class="step"><b><span class="n">2</span>Share</b>Send your link to friends and communities.</div>
          <div class="step"><b><span class="n">3</span>Earn</b>Collect a share of their fees, forever.</div>
        </div>
      </div>
      <div class="panel">
        <h2>Top referrers</h2>
        <p class="muted" style="margin:0 0 6px">This season.</p>
        <table class="gtable">
          <thead><tr><th>Rank</th><th>Address</th><th class="r">Invited</th><th class="r">Earned</th></tr></thead>
          <tbody>
            <tr><td>1</td><td class="mono">0x4be2…a913</td><td class="r">148</td><td class="r">$12,410</td></tr>
            <tr><td>2</td><td class="mono">0x90cc…17f4</td><td class="r">96</td><td class="r">$8,205</td></tr>
            <tr><td>3</td><td class="mono">0x2d81…6b0a</td><td class="r">71</td><td class="r">$5,988</td></tr>
            <tr><td>4</td><td class="mono">0xf00d…3c55</td><td class="r">44</td><td class="r">$3,102</td></tr>
            <tr><td>5</td><td class="mono">0x81ee…920b</td><td class="r">37</td><td class="r">$2,671</td></tr>
          </tbody>
        </table>
      </div>
    </div>
'''

POINTS = '''    <div class="tiles">
      <div class="tile"><div class="label">Your points</div><div class="value">—</div><div class="sub">Connect wallet</div></div>
      <div class="tile">
        <div class="label">Season 1</div><div class="value">74 days left</div>
        <div class="progress" aria-hidden="true"><i style="width:38%"></i></div>
      </div>
      <div class="tile"><div class="label">Points distributed</div><div class="value">12.6M</div><div class="sub">across 1,241 wallets</div></div>
      <div class="tile"><div class="label">Your boost</div><div class="value">1.0x</div><div class="sub">stake HAR to raise it</div></div>
    </div>
    <div class="grid2">
      <div class="panel">
        <h2>Leaderboard</h2>
        <p class="muted" style="margin:0 0 6px">Season 1 — top wallets.</p>
        <table class="gtable">
          <thead><tr><th>Rank</th><th>Address</th><th class="r">Boost</th><th class="r">Points</th></tr></thead>
          <tbody>
            <tr><td>1</td><td class="mono">0x7f3a…9c21</td><td class="r">3.0x</td><td class="r">842,110</td></tr>
            <tr><td>2</td><td class="mono">0x1bd4…08ee</td><td class="r">1.5x</td><td class="r">611,489</td></tr>
            <tr><td>3</td><td class="mono">0xc02f…44a7</td><td class="r">3.0x</td><td class="r">590,732</td></tr>
            <tr><td>4</td><td class="mono">0x98e1…d3b0</td><td class="r">1.0x</td><td class="r">402,175</td></tr>
            <tr><td>5</td><td class="mono">0x33aa…71c9</td><td class="r">1.5x</td><td class="r">387,960</td></tr>
            <tr class="you-row"><td>—</td><td>You</td><td class="r">1.0x</td><td class="r">Connect wallet</td></tr>
          </tbody>
        </table>
      </div>
      <div class="panel">
        <h2>How to earn</h2>
        <div class="steps" style="margin-top:10px;grid-template-columns:1fr">
          <div class="step"><b>Deposit in vaults</b>1 point per $1 per day, boosted by HAR staking.</div>
          <div class="step"><b>Trade perps &amp; spot</b>Points on volume routed through the Harmonix builder code.</div>
          <div class="step"><b>Refer friends</b>Earn 10% of your referrals' points.</div>
        </div>
        <div style="margin-top:12px">
          <div class="kv"><span>1 month HAR lock</span><b>1.0x</b></div>
          <div class="kv"><span>3 month HAR lock</span><b>1.5x</b></div>
          <div class="kv"><span>12 month HAR lock</span><b>3.0x</b></div>
        </div>
      </div>
    </div>
'''

# ---------- 4c. vault detail pages + clickable rows ----------
def vault_apy_chart(apy):
    random.seed(int(apy * 100))
    pts = []
    x, y = 60, 128
    for i in range(13):
        pts.append((x, int(max(34, min(158, y)))))
        x += 51
        y += random.uniform(-15, 9)
    line = " ".join("%d,%d" % p for p in pts)
    fill = "60,176 " + line + " %d,176" % pts[-1][0]
    labels = ""
    for i, frac in enumerate([1.15, 1.0, 0.85, 0.7]):
        yy = 34 + i * 41
        labels += '<line x1="60" y1="%d" x2="700" y2="%d" stroke="rgba(255,255,255,0.05)"/><text class="axis" x="8" y="%d">%.1f%%</text>' % (yy, yy, yy + 3, apy * frac)
    bench = " ".join("%d,%d" % (p[0], min(160, p[1] + 26 + (i % 3) * 3)) for i, p in enumerate(pts))
    return ('<svg viewBox="0 0 730 185" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="vg' + str(int(apy*100)) + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(215,251,95,0.28)"/><stop offset="1" stop-color="rgba(215,251,95,0)"/></linearGradient></defs>'
            + labels +
            '<polygon points="' + fill + '" fill="url(#vg' + str(int(apy*100)) + ')"/>'
            '<polyline points="' + bench + '" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="1.5" stroke-dasharray="5 4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<polyline points="' + line + '" fill="none" stroke="#d7fb5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="%d" cy="%d" r="3.5" fill="#d7fb5f"/></svg>' % pts[-1])

VAULTS = [
    dict(slug="vault-hausdc.html", px="1", earned_full="18412.66", earned_disp="18,412.66", step="0.05", icon=USDC_ICON, name="HIP-3 haUSDC Vault", apy=8.42, tvl="$314.3K", sub="",
         asset="USDC", cap="$5.0M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span><span class="plus">+3</span>',
         desc="Multi-asset stablecoin vault optimized across HyperEVM, HyperCore, and HIP3 markets. Earn from delta-neutral strategies, lending yield, and future HIP3 potential rewards.",
         profile="Balanced", earned="$18.4K", g1="$61", g7="$412", g30="$1.7K", vid="0x3f8a…9d21", deployed="Jun 2026",
         allocs=[("Delta-neutral basis (HyperCore)", "52%", "$163.4K", "9.8%"),
                 ("Stablecoin lending (HyperEVM)", "33%", "$103.7K", "6.4%"),
                 ("HIP-3 market-making, hedged", "15%", "$47.2K", "8.9%")]),
    dict(slug="vault-delta-neutral.html", px="1", earned_full="31204.18", earned_disp="31,204.18", step="0.09", icon=USDC_ICON, name="USDC — $HYPE Delta Neutral Vault", apy=7.46, tvl="$606.51K", sub="",
         asset="USDC", cap="$2.5M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span>',
         desc="Convert half of your deposit into HyperLiquid and purchase $HYPE, while a 1x short HYPE-USD position hedges your exposure and earns funding fees. Net delta zero; auto-rebalances when funding flips.",
         profile="Balanced", earned="$31.2K", g1="$124", g7="$861", g30="$3.6K", vid="0x81c2…44e0", deployed="Feb 2026",
         allocs=[("Spot HYPE long", "50%", "$303.2K", "—"),
                 ("1x HYPE-USD short (funding)", "50%", "$303.3K", "14.9%")]),
    dict(slug="vault-khype.html", px="43.6", earned_full="84903.42", earned_disp="84,903.42", step="0.24", icon=KHYPE_ICON_S, name="HyperEVM $KHYPE Vault", apy=3.84, tvl="$2.9M", sub="47,539.37 KHYPE",
         asset="KHYPE", cap="$6.0M", rewards='<span class="ricon"><svg aria-hidden="true"><use href="#tok-valantis"/></svg></span><span class="plus">+1</span>',
         desc="Deposit your KHYPE to earn optimized yield across market-neutral strategies, dynamically allocated across leading HyperEVM protocols. Valantis points accrue to depositors.",
         profile="Conservative", earned="$84.9K", g1="$305", g7="$2.1K", g30="$9.2K", vid="0xc4d9…b7a3", deployed="Mar 2026",
         allocs=[("HyperEVM lending markets", "58%", "$1.68M", "4.1%"),
                 ("Delta-neutral overlay", "27%", "$783K", "3.4%"),
                 ("Liquid reserve", "15%", "$435K", "—")]),
    dict(slug="vault-hype.html", px="42.9", earned_full="56310.77", earned_disp="56,310.77", step="0.16", icon=HYPE_ICON, name="HyperEVM $HYPE Vault", apy=3.80, tvl="$1.99M", sub="33,231.78 HYPE",
         asset="HYPE", cap="$5.0M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span><span class="plus">+1</span>',
         desc="Deposit your HYPE to earn optimized yield across market-neutral strategies, dynamically allocated across leading HyperEVM protocols. No directional risk.",
         profile="Conservative", earned="$56.3K", g1="$207", g7="$1.5K", g30="$6.1K", vid="0x9ab1…02cf", deployed="Mar 2026",
         allocs=[("HyperEVM protocol allocation", "62%", "$1.23M", "4.0%"),
                 ("Market-neutral positions", "23%", "$458K", "3.6%"),
                 ("Liquid reserve", "15%", "$299K", "—")]),
]

def vault_content(v):
    sub_html = ('<div class="sub">%s</div>' % v["sub"]) if v["sub"] else ""
    alloc_rows = "".join(
        '<tr><td>%s</td><td class="r">%s</td><td class="r">%s</td><td class="r" style="color:var(--lime)">%s</td></tr>'
        % a for a in v["allocs"])
    return '''    <p style="margin:0 0 12px"><a href="index.html" class="backlink">Yield Markets</a><span style="color:var(--text-3);font-size:13px"> / ''' + v["name"] + '''</span></p>
    <div class="vhead">
      <div class="vhead-l">
        ''' + v["icon"] + '''
        <div>
          <h2>''' + v["name"] + '''</h2>
          <div class="chip-row">
            <span class="chip-sm">Profile <b>''' + v["profile"] + '''</b></span>
            <span class="chip-sm">Vault token <b>''' + v["asset"] + '''</b></span>
            <span class="chip-sm">Manager <b>Harmonix</b></span>
          </div>
        </div>
      </div>
      <span class="live">LIVE</span>
    </div>
    <div class="vtabs"><button class="active">Vault overview</button><button>My position</button></div>
    <div class="tiles">
      <div class="tile"><div class="label">TVL</div><div class="value">''' + v["tvl"] + '''</div>''' + sub_html + '''</div>
      <div class="tile"><div class="label">Capacity</div><div class="value">''' + v["cap"] + '''</div></div>
      <div class="tile"><div class="label">Net APY</div><div class="value lime">''' + ('%.2f%%' % v["apy"]) + '''</div></div>
      <div class="tile"><div class="label">Net APY (90d avg)</div><div class="value">''' + ('%.2f%%' % (v["apy"] * 0.93)) + '''</div></div>
      <div class="tile"><div class="label">Rewards</div><div class="value" style="display:flex;align-items:center;gap:6px">''' + v["rewards"] + '''</div></div>
    </div>
    <div class="grid2" style="grid-template-columns: 1.7fr 1fr; align-items: start;">
      <div>
        <div class="panel" style="margin-bottom:14px">
          <h2>Strategy overview</h2>
          <p class="muted" style="margin:6px 0 0">''' + v["desc"] + '''</p>
        </div>
        <div class="panel" style="margin-bottom:14px">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
            <h2 style="margin:0">Net APY</h2>
            <div class="tf" style="margin:0"><button>7D</button><button class="active">30D</button><button>3M</button></div>
          </div>
          <div class="legend" style="margin:10px 0 8px">
            <span><span class="legend-dot" style="background:#d7fb5f"></span>Net APY</span>
            <span><span class="legend-dot" style="background:rgba(255,255,255,0.35)"></span>Benchmark (HyperEVM lending)</span>
          </div>
          ''' + vault_apy_chart(v["apy"]) + '''
          <p class="chart-cap">Trailing net APY after fees. Rewards valued at market on accrual.</p>
        </div>
        <div class="panel" style="margin-bottom:14px">
          <h2>Interest generated</h2>
          <p class="muted" style="margin:2px 0 0">Total yield paid to depositors in this vault.</p>
          <div class="bignum" data-count="''' + v["earned_full"] + '''" data-step="''' + v["step"] + '''">+$''' + v["earned_disp"] + '''</div>
          <div class="growth-grid">
            <div class="g"><div class="n">''' + v["g1"] + '''</div><div class="l">1D growth</div></div>
            <div class="g"><div class="n">''' + v["g7"] + '''</div><div class="l">7D growth</div></div>
            <div class="g"><div class="n">''' + v["g30"] + '''</div><div class="l">30D growth</div></div>
            <div class="g"><div class="n">''' + v["earned"] + '''</div><div class="l">All time</div></div>
          </div>
        </div>
        <div class="panel">
          <h2>Allocation breakdown</h2>
          <p class="muted" style="margin:0 0 6px">Where deposits are deployed right now.</p>
          <table class="gtable">
            <thead><tr><th>Strategy</th><th class="r">Allocation</th><th class="r">Deployed</th><th class="r">APY</th></tr></thead>
            <tbody>''' + alloc_rows + '''</tbody>
          </table>
        </div>
      </div>
      <div class="rail">
        <div class="panel" style="margin-bottom:14px">
          <h2>You deposit</h2>
          <div class="field" style="margin-top:8px">
            <div class="fbox"><input class="finput" id="dep-in" inputmode="decimal" placeholder="0.00" data-apy="''' + str(v["apy"]) + '''" data-asset="''' + v["asset"] + '''" data-px="''' + v["px"] + '''" aria-label="Deposit amount"><span class="unit">''' + v["asset"] + '''</span></div>
          </div>
          <div class="wallet-line"><span>Wallet: <span data-walletbal="''' + v["asset"] + '''">0</span></span><span class="halfmax"><button class="ghost-btn" data-frac="0.5" style="padding:4px 10px;font-size:11px;border-radius:7px">Half</button><button class="ghost-btn" data-frac="1" style="padding:4px 10px;font-size:11px;border-radius:7px">Max</button></span></div>
          <div class="trade-rows">
            <div class="kv"><span>~ value</span><b id="dep-val">$0.00</b></div>
            <div class="kv"><span>Est. yearly earnings</span><b id="dep-earn">—</b></div>
          </div>
          <button class="cta" id="dep-cta">Connect wallet</button>
          <div class="kv" style="margin-top:10px"><span>Transaction settings</span><b>0.5% slippage</b></div>
        </div>
        <div class="panel" style="margin-bottom:14px">
          <h2>Vault info</h2>
          <div style="margin-top:8px">
            <div class="kv"><span>Token</span><b>''' + v["asset"] + '''</b></div>
            <div class="kv"><span>Vault profile</span><b>''' + v["profile"] + '''</b></div>
            <div class="kv"><span>Net APY</span><b style="color:var(--lime)">''' + ('%.2f%%' % v["apy"]) + '''</b></div>
            <div class="kv"><span>Vault ID</span><b class="mono">''' + v["vid"] + '''</b></div>
            <div class="kv"><span>Network</span><b>HyperEVM</b></div>
            <div class="kv"><span>Manager</span><b>Harmonix</b></div>
            <div class="kv"><span>Deployed</span><b>''' + v["deployed"] + '''</b></div>
            <div class="kv"><span>Management fee</span><b>0.00%</b></div>
            <div class="kv"><span>Performance fee</span><b>10.00%</b></div>
            <div class="kv"><span>Withdrawals</span><b>Daily, no lock</b></div>
          </div>
        </div>
        <div class="panel">
          <h2>Harmonix</h2>
          <p class="muted" style="margin:6px 0 10px">Harmonix builds risk-managed yield strategies on Hyperliquid — delta-neutral by default, transparent on-chain, audited by Verichains, Zenith and Shieldify.</p>
          <a class="backlink" href="analytics.html">Learn more</a>
        </div>
      </div>
    </div>
''' + COUNTER_JS

# make home rows clickable
home_main = home_main.replace('href="https://christophorusan.github.io/harmonix-glass/', 'href="')
_parts = home_main.split('<article class="card">')
if len(_parts) == 5:
    _rebuilt = _parts[0]
    for _i, _part in enumerate(_parts[1:]):
        _part = _part.replace('</article>', '</a>', 1)
        _part = _part.replace('<button class="deposit-btn">Deposit</button>', '<span class="deposit-btn" role="button">Deposit</span>', 1)
        _rebuilt += '<a class="card" href="' + VAULTS[_i]["slug"] + '">' + _part
    home_main = _rebuilt
else:
    assert 'a class="card" href="vault-' in home_main, "vault rows neither articles nor anchors"

# ---------- 5. home page: reuse existing main, strip its inline topbar & swap in shared ----------
home_content = home_main[len('<main class="main">'):]
home_content = home_content[:home_content.rindex('</main>')]
# replace its topbar with the standard one (already identical) — keep as is.
idx_html = make_shell("Home", "Yield Markets") + '<main class="main">' + home_content + '</main>\n' + SHELL_TAIL
idx_html = mark_mnav(idx_html, "Home")
open(os.path.join(OUT, "index.html"), "w").write(idx_html)
print("wrote index.html", len(idx_html))

page("perps.html", "Perps", "Perps", PERPS)
page("swap.html", "Swap", "Swap", SWAP)
page("stake.html", "Stake", "Stake", STAKE)
page("protection.html", "Protection Vault", "Protection Vault", PROTECTION)
page("stake-har.html", "Stake HAR", "Stake HAR", STAKE_HAR)
page("portfolio.html", "Portfolio", "Portfolio", PORTFOLIO)
page("analytics.html", "Analytics", "Analytics", ANALYTICS)
page("referral.html", "Referral Program", "Referral Program", REFERRAL)
page("points.html", "Points", "Points", POINTS)
for v in VAULTS:
    page(v["slug"], "Home", v["name"], vault_content(v))
print("done")


LIGHT_CSS = """
html[data-theme="light"] {
  /* ---------- OG light theme (exact app.harmonix.fi default) ---------- */
  & {
    --text-0: #11181c;
    --text-1: rgba(24, 49, 50, 0.78);
    --text-2: #71717a;
    --text-3: #a1a1aa;
    --glass-border: #e5e7eb;
    --glass-border-hover: #c9cec3;
  }
  body { background: #f2f5ee; color: #11181c; }
  body::before {
    background:
      radial-gradient(1200px 800px at 62% 28%, rgba(226, 246, 161, 0.38), transparent 60%),
      radial-gradient(900px 700px at 22% 78%, rgba(7, 39, 35, 0.07), transparent 70%),
      linear-gradient(160deg, #f8faf4 0%, #edf1e7 48%, #f4f6f0 100%);
  }
  .sidebar { color: #f8faf8; }
  .sidebar .assets-card .value { color: #ffffff; }
  .mn { color: rgba(248, 250, 248, 0.6); }
  .mn.active { color: #e2f6a1; }
  body::after { opacity: 0.02; }
  .topbar h1 { color: #11181c; }

  .banner { background: linear-gradient(90deg, rgba(242, 250, 217, 0.75), rgba(227, 243, 198, 0.75)); border-color: rgba(24, 49, 50, 0.08); color: #3f4a46; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); }
  .banner strong { color: #11181c; }
  .banner .dot { background: #77a11c; box-shadow: none; }

  .card, .panel, .tile, .tabs, .sort, .chain-btn, .pairbar {
    background: rgba(255, 255, 255, 0.58); border-color: rgba(24, 49, 50, 0.10); color: #11181c;
    box-shadow: 0 8px 24px rgba(16, 24, 40, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(18px) saturate(1.1); -webkit-backdrop-filter: blur(18px) saturate(1.1);
  }
  .card:hover { background: rgba(255, 255, 255, 0.75); border-color: rgba(24, 49, 50, 0.18); box-shadow: 0 12px 30px rgba(16, 24, 40, 0.10), inset 0 1px 0 rgba(255, 255, 255, 0.85); }
  .list-head { color: #71717a; }
  .card-head h3, .metric .value, .tile .value, .row .v, .kv b, .pstat .v { color: #183132; }
  .metric .label, .tile .label, .pstat .label, .flabel { color: #71717a; }
  .metric .sub, .tile .sub { color: #a1a1aa; }
  .metric.apy .value, .tile .value.lime, .pstat .v.lime { color: #059212; }
  .pstat .v.up { color: #059212; }
  .delta.up { color: #059212; } .delta.down { color: #dc2626; }
  .gtable th { color: #71717a; }
  .gtable td { border-color: #eef0eb; color: #3f4a46; }
  .gtable td:first-child { color: #183132; }
  .panel h2 { color: #11181c; }
  .panel .muted { color: #71717a; }
  .panel .kv { color: #71717a; }
  .panel .kv + .kv, .growth-grid, .divider, .spread { border-color: #eef0eb; }
  .you-row td { color: #4d7c0f !important; }

  /* dark-green hero + chart cards, like the OG section cards */
  .hero, .chart-panel, .panel:has(.axis) { background: rgba(7, 39, 35, 0.88); border-color: rgba(255, 255, 255, 0.08); color: #f8faf8; box-shadow: 0 16px 40px rgba(7, 39, 35, 0.28); backdrop-filter: blur(18px) saturate(1.1); -webkit-backdrop-filter: blur(18px) saturate(1.1); }
  .hero h2, .chart-panel h2, .panel:has(.axis) h2 { color: #ffffff; }
  .hero p, .chart-panel .muted, .panel:has(.axis) .muted { color: rgba(248, 250, 248, 0.6); }
  .panel:has(.axis) .kv, .chart-panel .kv { color: rgba(248, 250, 248, 0.6); }
  .panel:has(.axis) .kv b, .chart-panel .kv b { color: #f8faf8; }
  .panel:has(.axis) .kv + .kv, .chart-panel .kv + .kv { border-color: rgba(255, 255, 255, 0.08); }
  .chart-cap { color: #a1a1aa; }
  .chart-panel .chart-cap, .panel:has(.axis) .chart-cap { color: rgba(248, 250, 248, 0.45); }
  .panel:has(.axis) .legend, .chart-panel .legend { color: rgba(248, 250, 248, 0.75); }
  .legend { color: #3f4a46; }
  .hero-stats { background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.12); color: rgba(248, 250, 248, 0.8); }
  .hero-stats b { color: #ffffff; }
  .hero-stats .apy { color: #e2f6a1; }
  .hero .live { color: #e2f6a1; border-color: rgba(226, 246, 161, 0.45); }
  .hero .live::before { background: #e2f6a1; }
  .live { color: #059212; border-color: rgba(5, 146, 18, 0.4); }
  .live::before { background: #059212; box-shadow: none; }

  /* accents on white */
  .card .spark polyline, .tile .spark polyline { stroke: #059212; }
  .card .spark circle, .tile .spark circle { fill: #059212; }
  .px-up { color: #059212 !important; }
  .px-down { color: #dc2626 !important; }
  .growth-grid .g .n, .bignum { color: #059212; }
  .hbar-track { background: #eef0eb; }
  .hbar-track i { background: linear-gradient(90deg, rgba(5, 146, 18, 0.35), #059212); }
  .hbar-row + .hbar-row { border-color: #eef0eb; }
  .hbar-row .val { color: #183132; }
  .hbar-row .pct { color: #71717a; }

  /* OG buttons: dark teal pills on light */
  .deposit-btn { background: #183132; color: #ffffff; box-shadow: none; }
  .deposit-btn:hover { background: #1c3b3c; color: #ffffff; box-shadow: 0 6px 16px rgba(24, 49, 50, 0.25); }
  .cta { background: #183132; color: #ffffff; box-shadow: none; }
  .cta:hover { background: #1c3b3c; box-shadow: 0 6px 16px rgba(24, 49, 50, 0.25); }
  .cta.sell { background: #dc2626; color: #fff; }
  .cta.sell:hover { background: #e04545; }
  .connect-btn { background: #183132; color: #ffffff; box-shadow: none; }
  .connect-btn:hover { background: #1c3b3c; }
  .connect-btn.addr { background: #f4f5f1; color: #183132; box-shadow: inset 0 0 0 1px #d8dcd0; }
  .connect-btn.addr:hover { background: #eef0e9; }
  .ghost-btn { background: #f4f5f1; color: #183132; box-shadow: inset 0 0 0 1px #d8dcd0; }
  .ghost-btn:hover { background: #183132; color: #ffffff; }
  .chain-btn { color: #183132; font-weight: 600; }
  .chain-btn:hover { background: #f6f7f3; border-color: #d6dad2; }
  .chain-btn .cicon svg circle { fill: #072723; }
  .chain-btn .cicon svg path { fill: #50D2C1; }

  /* segments, tabs, inputs on white */
  .seg { background: rgba(24, 49, 50, 0.05); border-color: rgba(24, 49, 50, 0.08); }
  .seg button { color: #71717a; }
  .seg button.active { background: #183132; color: #ffffff; }
  .seg.buysell button.buy.active { background: #059212; color: #fff; }
  .seg.buysell button.sell.active { background: #dc2626; color: #fff; }
  .tf button { color: #71717a; }
  .tf button.active { background: rgba(5, 146, 18, 0.10); color: #059212; }
  .chart-panel .tf button, .panel:has(.axis) .tf button { color: rgba(248, 250, 248, 0.55); }
  .chart-panel .tf button.active, .panel:has(.axis) .tf button.active { background: rgba(226, 246, 161, 0.16); color: #e2f6a1; }
  .ptabs button, .vtabs button { color: #71717a; }
  .ptabs button.active, .vtabs button.active { color: #11181c; border-bottom-color: #059212; }
  .ptabs, .vtabs { border-color: #eef0eb; }
  .fbox { background: rgba(24, 49, 50, 0.045); border-color: rgba(24, 49, 50, 0.09); color: #183132; }
  .finput { color: #183132; }
  .finput::placeholder { color: #a1a1aa; }
  .halfmax button { background: #f4f5f1; border-color: #d8dcd0; color: #183132; }
  .wallet-line { color: #a1a1aa; }
  .ob-head { color: #71717a; }
  .ob-row { color: #3f4a46; }
  .spread { color: #71717a; }
  .empty { background: #fafbf7; border-color: #d8dcd0; color: #a1a1aa; }
  .empty-state { color: #71717a; }
  .empty-state .big { color: #11181c; }
  .step, .swap-box, .code-box { background: rgba(24, 49, 50, 0.045); border-color: rgba(24, 49, 50, 0.09); color: #3f4a46; }
  .step b { color: #11181c; }
  .step .n { color: #4d7c0f; }
  .chip-sm { background: #f4f5f1; border-color: #e5e7eb; color: #71717a; }
  .chip-sm b { color: #183132; }
  .backlink { color: #71717a; }
  .backlink:hover { color: #11181c; }
  .token-pill { background: #f4f5f1; border-color: #e5e7eb; color: #183132; }
  .avatar { background: #f4f5f1; border-color: #e5e7eb; color: #3f4a46; }
  .row .v .chip { background: rgba(5, 146, 18, 0.08); border-color: rgba(5, 146, 18, 0.3); color: #059212; }
  .row .v .plus { color: #71717a; }
  .panel:not(:has(.axis)) svg text { fill: #71717a; }
  .progress { background: #eef0eb; border-color: #e5e7eb; }
  .progress i { background: linear-gradient(90deg, rgba(5, 146, 18, 0.4), #059212); }

  /* sidebar stays OG dark */
  .sidebar { background: rgba(10, 26, 23, 0.90); border: 1px solid rgba(255, 255, 255, 0.06); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); }
  .assets-card { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.09); }

  @media (max-width: 760px) {
    .cards .card .row { border-color: #eef0eb; }
  }
}
"""
open(os.path.join(OUT, "assets", "style.css"), "a").write(LIGHT_CSS)

# theme toggle button styling (works in both themes via tokens)
THEME_BTN_CSS = """
  .theme-btn {
    width: 40px; height: 40px; border-radius: 999px; cursor: pointer;
    display: inline-grid; place-items: center;
    background: var(--glass); border: 1px solid var(--glass-border); color: var(--text-1);
    transition: color 0.15s, border-color 0.15s, background 0.15s;
  }
  .theme-btn:hover { color: var(--text-0); border-color: var(--glass-border-hover); }
  .theme-btn:focus-visible { outline: 2px solid #e2f6a1; outline-offset: 2px; }
  html[data-theme="light"] .theme-btn { background: rgba(255, 255, 255, 0.6); border-color: rgba(24, 49, 50, 0.10); color: #71717a; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); }
  html[data-theme="light"] .theme-btn:hover { color: #11181c; border-color: #c9cec3; }
  .mhead .theme-btn { width: 34px; height: 34px; }
"""
open(os.path.join(OUT, "assets", "style.css"), "a").write(THEME_BTN_CSS)

# ---------- final palette pass: exact OG accent across all generated files ----------
PALETTE = [
    ("#d7fb5f", "#e2f6a1"), ("#D7FB5F", "#E2F6A1"),
    ("rgba(215, 251, 95", "rgba(226, 246, 161"), ("rgba(215,251,95", "rgba(226,246,161"),
    ("#e0fb6d", "#ecf9c0"), ("#cbf04f", "#dcf291"),
    ("#eaff85", "#f2fcd4"), ("#d6f95f", "#e5f6a8"),
    ("#e4ff78", "#eef9c6"), ("#cdf254", "#ddf295"),
    ("#0a1a12", "#183132"),
]
def apply_palette(txt):
    for a, b in PALETTE:
        txt = txt.replace(a, b)
    return txt

import glob
_js_src = apply_palette(open("app.js").read())
open(os.path.join(OUT, "assets", "app.js"), "w").write(_js_src)
for _f in glob.glob(os.path.join(OUT, "*.html")) + [os.path.join(OUT, "assets", "style.css")]:
    _t = open(_f).read()
    open(_f, "w").write(apply_palette(_t))
print("palette pass done")
