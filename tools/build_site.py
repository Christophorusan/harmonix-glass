#!/usr/bin/env python3
"""Generate the multi-page Harmonix glass mockup site from the single-file source."""
import re, random, os

SRC = "harmonix-earn-glass.html"
OUT = "harmonix-glass-deploy"

src = open(SRC).read()

# ---------- 1. split source ----------
style_m = re.search(r"<style>(.*?)</style>", src, re.S)
base_css = style_m.group(1)

main_start = src.index('<main class="main">')
shell_head = src[:main_start]              # meta, title, sprite svg, <div class="app">, sidebar, up to main
shell_head = shell_head.replace(style_m.group(0), '<link rel="stylesheet" href="assets/style.css">')

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
_new_bg = """      radial-gradient(140% 140% at 50% 42%, transparent 52%, rgba(2, 9, 5, 0.62) 100%),
      radial-gradient(1150px 820px at 64% 36%, rgba(86, 168, 116, 0.50), transparent 60%),
      radial-gradient(760px 560px at 22% 76%, rgba(40, 96, 64, 0.34), transparent 70%),
      radial-gradient(1700px 1150px at 50% 46%, rgba(22, 56, 38, 0.55), transparent 82%),
      linear-gradient(155deg, #0b1a12 0%, #143726 36%, #0e2a1a 62%, #05100a 100%);"""
if _old_bg in base_css:
    base_css = base_css.replace(_old_bg, _new_bg)
else:
    assert "rgba(86, 168, 116, 0.50)" in base_css, "backdrop missing entirely"

# ---------- 2. nav hrefs + active state ----------
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
        <button class="chain-btn" aria-haspopup="listbox" aria-label="Switch network, current: HyperEVM">
          <span class="cicon" aria-hidden="true"><svg viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="11" fill="#072723"/><path d="M18.9666 10.8871C18.9812 12.1981 18.7068 13.4507 18.1679 14.6475C17.3984 16.3517 15.5534 17.7452 13.8685 16.2619C12.4945 15.0529 12.2396 12.5986 10.181 12.2393C7.45717 11.9092 7.39163 15.0675 5.61217 15.4244C3.62879 15.8274 2.9709 12.4918 3.00004 10.9769C3.02917 9.46209 3.43215 7.33305 5.15578 7.33305C7.13915 7.33305 7.27267 10.336 9.79014 10.1734C12.2833 10.0035 12.327 6.87908 13.9559 5.54146C15.3615 4.3859 17.0148 5.23315 17.8426 6.62418C18.6097 7.91083 18.9472 9.42082 18.9641 10.8871H18.9666Z" fill="#50D2C1"/></svg></span>
          HyperEVM
          <svg class="chev" width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <button class="connect-btn">Connect wallet</button>
      </div>
    </div>
'''

def page(fname, active, title, content):
    html = make_shell(active, title)
    html += '<main class="main">\n' + TOPBAR.format(title=title) + content + '\n  </main>\n' + SHELL_TAIL
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
        <div class="tf"><button>1m</button><button>5m</button><button>15m</button><button class="active">1h</button><button>4h</button><button>1d</button></div>
        ''' + CANDLES + '''
        <p class="chart-cap">1h candles. Mark price ticks live with momentum colouring.</p>
      </div>

      <div class="panel">
        <div class="ptabs" style="margin:-6px -6px 10px"><button class="active">Order book</button><button>Recent trades</button></div>
        <div class="ob-head"><span>Price</span><span>Size</span><span>Total</span></div>
        ''' + orderbook(LAST) + '''
      </div>

      <div class="panel">
        <div class="seg"><button class="active">Cross</button><button>20x</button><button>One-way</button></div>
        <div class="seg" style="margin-top:8px"><button class="active">Market</button><button>Limit</button><button>Pro</button></div>
        <div class="seg buysell"><button class="buy active">Buy / Long</button><button class="sell">Sell / Short</button></div>
        <div class="trade-rows">
          <div class="kv"><span>Available to trade</span><b>0.00 USDC</b></div>
          <div class="kv"><span>Current position</span><b>0.00 HYPE</b></div>
        </div>
        <div class="field">
          <div class="flabel">Size</div>
          <div class="fbox">0.00 <span class="unit">USDC</span></div>
        </div>
        <button class="cta">Connect wallet to trade</button>
        <div class="trade-rows">
          <div class="kv"><span>Liquidation price</span><b>N/A</b></div>
          <div class="kv"><span>Order value</span><b>N/A</b></div>
          <div class="kv"><span>Margin required</span><b>N/A</b></div>
          <div class="kv"><span>Slippage</span><b>Est. 0.10% / Max 3%</b></div>
          <div class="kv"><span>Fees</span><b>0.0350% / 0.0150%</b></div>
        </div>
      </div>

      <div class="panel positions-panel">
        <div class="ptabs"><button class="active">Balances</button><button>Positions</button><button>Open orders</button><button>TWAP</button><button>Trade history</button><button>Funding history</button></div>
        <div class="empty-state">Connect wallet to view your account</div>
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
        <div class="tf"><button>1m</button><button>5m</button><button>15m</button><button class="active">1h</button><button>4h</button><button>1d</button></div>
        ''' + CANDLES2 + '''
        <p class="chart-cap">1h candles, HYPE/USDC spot. Last price ticks live.</p>
      </div>

      <div class="panel">
        <div class="ptabs" style="margin:-6px -6px 10px"><button class="active">Order book</button><button>Recent trades</button></div>
        <div class="ob-head"><span>Price</span><span>Size</span><span>Total</span></div>
        ''' + orderbook(LAST2) + '''
      </div>

      <div class="panel">
        <div class="seg"><button class="active">Market</button><button>Limit</button><button>TWAP</button></div>
        <div class="seg buysell"><button class="buy active">Buy HYPE</button><button class="sell">Sell HYPE</button></div>
        <div class="trade-rows">
          <div class="kv"><span>Available USDC</span><b>0.00</b></div>
          <div class="kv"><span>Available HYPE</span><b>0.00</b></div>
        </div>
        <div class="field">
          <div class="flabel">You pay</div>
          <div class="fbox">0.00 <span class="unit">USDC</span></div>
        </div>
        <div class="swap-arrow" style="margin-top:8px"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 3v10m0 0 4-4m-4 4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="field" style="margin-top:2px">
          <div class="flabel">You receive</div>
          <div class="fbox">0.00 <span class="unit">HYPE</span></div>
        </div>
        <button class="cta">Connect wallet to swap</button>
        <div class="trade-rows">
          <div class="kv"><span>Rate</span><b>1 HYPE = ''' + ('%.2f' % LAST2) + ''' USDC</b></div>
          <div class="kv"><span>Max slippage</span><b>0.50%</b></div>
          <div class="kv"><span>Fees</span><b>0.0400% + builder 0.0100%</b></div>
        </div>
      </div>

      <div class="panel positions-panel">
        <div class="ptabs"><button class="active">Balances</button><button>Open orders</button><button>Trade history</button></div>
        <div class="empty-state">Connect wallet to view your account</div>
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

  /* quiet chart captions */
  .chart-cap { margin: 8px 2px 0; font-size: 11.5px; color: var(--text-3); }
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

ANALYTICS = '''    <div class="tiles">
      <div class="tile"><div class="label">Total value locked</div><div class="value">$7.86M<span class="delta up">+4.2% 7d</span></div>''' + spark_tile([(0,18),(9,16),(18,17),(27,13),(36,12),(45,9),(54,7),(63,4)]) + '''</div>
      <div class="tile"><div class="label">24h volume</div><div class="value">$1.92M<span class="delta up">+12.8%</span></div>''' + spark_tile([(0,14),(9,16),(18,10),(27,13),(36,8),(45,11),(54,6),(63,4)]) + '''</div>
      <div class="tile"><div class="label">Best APY</div><div class="value lime">8.42%</div><div class="sub">HIP-3 haUSDC Vault</div></div>
      <div class="tile"><div class="label">Depositors</div><div class="value">1,241<span class="delta up">+38 this week</span></div></div>
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
    <div class="grid2">
      <div class="panel">
        <h2>TVL by vault</h2>
        <p class="muted" style="margin:0 0 6px">Share of protocol deposits.</p>
        <div class="hbar-row">''' + KHYPE_ICON_S + '''<span>HyperEVM $KHYPE</span><span class="hbar-track"><i style="width:100%"></i></span><span class="val">$2.90M</span><span class="pct">49.9%</span></div>
        <div class="hbar-row">''' + HYPE_ICON + '''<span>HyperEVM $HYPE</span><span class="hbar-track"><i style="width:69%"></i></span><span class="val">$1.99M</span><span class="pct">34.3%</span></div>
        <div class="hbar-row">''' + HYPE_ICON + '''<span>USDC — $HYPE Delta Neutral</span><span class="hbar-track"><i style="width:21%"></i></span><span class="val">$606.5K</span><span class="pct">10.4%</span></div>
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
'''

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
    return ('<svg viewBox="0 0 730 185" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="vg' + str(int(apy*100)) + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(215,251,95,0.28)"/><stop offset="1" stop-color="rgba(215,251,95,0)"/></linearGradient></defs>'
            + labels +
            '<polygon points="' + fill + '" fill="url(#vg' + str(int(apy*100)) + ')"/>'
            '<polyline points="' + line + '" fill="none" stroke="#d7fb5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="%d" cy="%d" r="3.5" fill="#d7fb5f"/></svg>' % pts[-1])

VAULTS = [
    dict(slug="vault-hausdc.html", icon=USDC_ICON, name="HIP-3 haUSDC Vault", apy=8.42, tvl="$314.3K", sub="",
         asset="USDC", cap="$5.0M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span><span class="plus">+3</span>',
         desc="Multi-asset stablecoin vault optimized across HyperEVM, HyperCore, and HIP3 markets. Earn from delta-neutral strategies, lending yield, and future HIP3 potential rewards.",
         strat=["Delta-neutral basis positions on HyperCore perps", "Stablecoin lending across HyperEVM money markets", "HIP-3 market-making inventory, hedged"]),
    dict(slug="vault-delta-neutral.html", icon=USDC_ICON, name="USDC — $HYPE Delta Neutral Vault", apy=7.46, tvl="$606.51K", sub="",
         asset="USDC", cap="$2.5M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span>',
         desc="Convert half of your deposit into HyperLiquid and purchase $HYPE, while a 1x short HYPE-USD position hedges your exposure and earns funding fees.",
         strat=["Spot HYPE long, 1x perp short — net delta zero", "Collects funding while hedged", "Auto-rebalances when funding flips"]),
    dict(slug="vault-khype.html", icon=KHYPE_ICON_S, name="HyperEVM $KHYPE Vault", apy=3.84, tvl="$2.9M", sub="47,539.37 KHYPE",
         asset="KHYPE", cap="$6.0M", rewards='<span class="ricon"><svg aria-hidden="true"><use href="#tok-valantis"/></svg></span><span class="plus">+1</span>',
         desc="Deposit your KHYPE to earn optimized yield across market-neutral strategies, dynamically allocated across leading HyperEVM protocols.",
         strat=["Spot KHYPE deployed across HyperEVM lending markets", "Delta-neutral overlay on staking yield", "Valantis points accrue to depositors"]),
    dict(slug="vault-hype.html", icon=HYPE_ICON, name="HyperEVM $HYPE Vault", apy=3.80, tvl="$1.99M", sub="33,231.78 HYPE",
         asset="HYPE", cap="$5.0M", rewards='<span class="ricon" style="background:#071916"><svg aria-hidden="true"><use href="#tok-glow"/></svg></span><span class="plus">+1</span>',
         desc="Deposit your HYPE to earn optimized yield across market-neutral strategies, dynamically allocated across leading HyperEVM protocols.",
         strat=["Spot HYPE allocated across HyperEVM protocols", "Market-neutral positioning, no directional risk", "Rewards stream in the Harmonix token"]),
]

def vault_content(v):
    strat_html = "".join('<div class="step"><b><span class="n">%d</span>%s</b></div>' % (i + 1, s) for i, s in enumerate(v["strat"]))
    sub_html = ('<div class="sub">%s</div>' % v["sub"]) if v["sub"] else ""
    return '''    <p style="margin:0 0 14px"><a href="index.html" class="backlink">&larr; Yield Markets</a></p>
    <div class="hero" style="padding:20px 26px">
      <div class="vault-hero-head">
        ''' + v["icon"] + '''
        <div><h2>''' + v["name"] + '''</h2><p>''' + v["desc"] + '''</p></div>
      </div>
      <span class="live">LIVE</span>
    </div>
    <div class="tiles">
      <div class="tile"><div class="label">Net APY</div><div class="value lime">''' + ('%.2f%%' % v["apy"]) + '''</div>''' + spark_tile([(0,15),(9,13),(18,14),(27,11),(36,12),(45,9),(54,8),(63,5)]) + '''</div>
      <div class="tile"><div class="label">TVL</div><div class="value">''' + v["tvl"] + '''</div>''' + sub_html + '''</div>
      <div class="tile"><div class="label">Capacity</div><div class="value">''' + v["cap"] + '''</div></div>
      <div class="tile"><div class="label">Rewards</div><div class="value" style="display:flex;align-items:center;gap:6px">''' + v["rewards"] + '''</div></div>
    </div>
    <div class="grid2">
      <div>
        <div class="panel" style="margin-bottom:14px">
          <h2>Net APY — last 90 days</h2>
          <p class="muted" style="margin:0 0 12px">After fees, including rewards.</p>
          ''' + vault_apy_chart(v["apy"]) + '''
          <p class="chart-cap">Trailing net APY. Rewards valued at market on accrual.</p>
        </div>
        <div class="panel">
          <h2>Strategy</h2>
          <div class="steps" style="margin-top:10px;grid-template-columns:1fr">''' + strat_html + '''</div>
        </div>
      </div>
      <div>
        <div class="panel" style="margin-bottom:14px">
          <h2>Deposit</h2>
          <div class="field">
            <div class="flabel">You deposit</div>
            <div class="fbox">0.00 <span class="unit">''' + v["asset"] + '''</span></div>
          </div>
          <div class="trade-rows">
            <div class="kv"><span>Est. yearly earnings</span><b>—</b></div>
            <div class="kv"><span>Your balance</span><b>—</b></div>
          </div>
          <button class="cta">Connect wallet to deposit</button>
        </div>
        <div class="panel">
          <h2>Details</h2>
          <div style="margin-top:8px">
            <div class="kv"><span>Network</span><b>HyperEVM</b></div>
            <div class="kv"><span>Asset</span><b>''' + v["asset"] + '''</b></div>
            <div class="kv"><span>Withdrawals</span><b>Daily, no lock</b></div>
            <div class="kv"><span>Performance fee</span><b>10% on yield</b></div>
            <div class="kv"><span>Management fee</span><b>None</b></div>
            <div class="kv"><span>Manager</span><b>Harmonix</b></div>
            <div class="kv"><span>Contract</span><b class="mono">0x3f8a…9d21</b></div>
          </div>
        </div>
      </div>
    </div>
'''

# make home rows clickable
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
