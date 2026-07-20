# OG-mirror analytics page (mirrors app.harmonix.fi/dashboards, numbers as of 2026-07-19)

def combo_chart(seed, ylab, bar_col="rgba(98,217,139,0.55)", line_col="#e2f6a1"):
    random.seed(seed)
    bars = ""
    cum = []
    total, y0 = 0, 176
    vals = [random.uniform(0.25, 1.0) for _ in range(12)]
    for i, v in enumerate(vals):
        x = 70 + i * 54
        bh = int(120 * v)
        bars += '<rect x="%d" y="%d" width="34" height="%d" rx="3" fill="%s"/>' % (x, y0 - bh, bh, bar_col)
        total += v
        cum.append((x + 17, y0 - 6 - int(total / 12.0 * 130)))
    line = " ".join("%d,%d" % p for p in cum)
    grid = ""
    for i, lab in enumerate(ylab):
        yy = 36 + i * 46
        grid += '<line x1="70" y1="%d" x2="718" y2="%d" stroke="rgba(255,255,255,0.06)"/><text class="axis" x="8" y="%d">%s</text>' % (yy, yy, yy + 3, lab)
    xlab = '<text class="axis" x="70" y="198">May</text><text class="axis" x="340" y="198">Jun</text><text class="axis" x="610" y="198">Jul</text>'
    end = '<circle cx="%d" cy="%d" r="3.5" fill="%s"/>' % (cum[-1][0], cum[-1][1], line_col)
    return ('<svg viewBox="0 0 730 204" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">' + grid + xlab + bars +
            '<polyline points="' + line + '" fill="none" stroke="' + line_col + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' + end + '</svg>')


def tvl_donut():
    segs = [("HyperEVM $KHYPE Vault", 49.0, "#e2f6a1"), ("HyperEVM $HYPE Vault", 33.9, "#50D2C1"),
            ("USDC — $HYPE Delta Neutral", 10.2, "#5EA9FF"), ("HIP-3 haUSDC Vault", 5.8, "#f1f1eb"),
            ("KelpDao — USDC Delta Neutral", 1.1, "#a1a1aa")]
    C = 2 * 3.14159 * 62
    off = 0.0
    arcs = ""
    for name, pct, col in segs:
        ln = C * pct / 100.0
        arcs += '<circle cx="80" cy="80" r="62" fill="none" stroke="%s" stroke-width="17" stroke-dasharray="%.1f %.1f" stroke-dashoffset="%.1f" transform="rotate(-90 80 80)"/>' % (col, max(ln - 2, 1), C - max(ln - 2, 1), -off)
        off += ln
    legend = "".join('<span><span class="legend-dot" style="background:%s"></span>%s <b style="font-weight:600">%.1f%%</b></span>' % (c, n, p) for n, p, c in segs)
    return ('<div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap">'
            '<svg viewBox="0 0 160 160" style="width:150px;height:150px;flex:none">' + arcs +
            '<text x="80" y="76" text-anchor="middle" font-size="15" font-weight="600" fill="currentColor" font-family="Poppins, sans-serif">$5.93M</text>'
            '<text x="80" y="94" text-anchor="middle" font-size="9" fill="#a1a1aa" font-family="Poppins, sans-serif">Total TVL</text></svg>'
            '<div class="legend" style="flex-direction:column;align-items:flex-start;gap:8px;display:flex">' + legend + '</div></div>')


def vrow(name, href, tvl, apy, pps):
    btn = ('<a class="ghost-btn" style="text-decoration:none" href="%s">View</a>' % href) if href else '<button class="ghost-btn">View</button>'
    return ('<tr><td>%s</td><td class="r">%s</td><td class="r" style="color:var(--lime)">%s</td><td class="r">0</td><td class="r">%s</td><td class="r">%s</td></tr>'
            % (name, tvl, apy, pps, btn))


_TILES = (
    '<div class="tiles">'
    '<div class="tile"><div class="label">Deposit 7D</div><div class="value">$31.63</div></div>'
    '<div class="tile"><div class="label">Deposit 30D</div><div class="value">$16.55K</div></div>'
    '<div class="tile"><div class="label">New depositors 7D</div><div class="value">11</div></div>'
    '<div class="tile"><div class="label">New depositors 30D</div><div class="value">60</div></div>'
    '<div class="tile"><div class="label">Yield 7D</div><div class="value" style="color:#62d98b">$172.56</div></div>'
    '<div class="tile"><div class="label">Yield 30D</div><div class="value" style="color:#62d98b">$328.71</div></div>'
    '<div class="tile"><div class="label">Total Value Locked</div><div class="value">$5,931,894</div></div>'
    '<div class="tile"><div class="label">Total Staked</div><div class="value">33,104.18 HYPE</div><div class="sub">≈ $2,005,129.58</div></div>'
    '</div>'
)

_LEG_W = '<span><span class="legend-dot" style="background:rgba(98,217,139,0.8)"></span>%s</span><span><span class="legend-dot" style="background:#e2f6a1"></span>%s</span>'

ANALYTICS = ('    ' + _TILES + '''
    <div class="grid2" style="margin-bottom:14px">
      <div class="panel">
        <h2>TVL Compositions</h2>
        <p class="muted" style="margin:0 0 14px">Share of protocol deposits by vault.</p>
        ''' + tvl_donut() + '''
      </div>
      <div class="panel">
        <h2>TVL</h2>
        <div class="legend" style="margin:6px 0 10px">''' + (_LEG_W % ("Weekly TVL", "Cumulative TVL")) + '''</div>
        ''' + combo_chart(31, ["$25.5M", "$17M", "$8.5M", "$0"]) + '''
      </div>
    </div>
    <div class="grid2" style="margin-bottom:14px">
      <div class="panel">
        <h2>Depositors</h2>
        <div class="legend" style="margin:6px 0 10px">''' + (_LEG_W % ("New depositors", "Cumulative depositors")) + '''</div>
        ''' + combo_chart(47, ["14K", "9K", "4K", "0"]) + '''
      </div>
      <div class="panel">
        <h2>Delta Neutral Yield</h2>
        <div class="legend" style="margin:6px 0 10px">''' + (_LEG_W % ("Weekly yield", "Cumulative yield")) + '''</div>
        ''' + combo_chart(63, ["$450K", "$300K", "$150K", "$0"]) + '''
      </div>
    </div>
    <div class="panel">
      <h2>Vaults</h2>
      <p class="muted" style="margin:0 0 6px">All Harmonix vaults, live stats.</p>
      <table class="gtable">
        <thead><tr><th>Vault</th><th class="r">TVL</th><th class="r">APY</th><th class="r">Risk factor</th><th class="r">Price / share</th><th class="r"></th></tr></thead>
        <tbody>
          ''' + vrow("HyperEVM $KHYPE Vault", "vault-khype.html", "47,550.22 KHYPE", "3.84%", "—")
              + vrow("Hyperliquid — USDC — $HYPE Delta Neutral Vault", "vault-delta-neutral.html", "$606,626", "7.27%", "$1.1674")
              + vrow("HyperEVM $HYPE Vault", "vault-hype.html", "33,231.22 HYPE", "3.8%", "—")
              + vrow("HIP-3 haUSDC Vault", "vault-hausdc.html", "$340,922", "8.52%", "$1.0155")
              + vrow("KelpDao — USDC — Delta Neutral Vault", None, "$21,387", "0.06%", "$1.1479") + '''
        </tbody>
      </table>
    </div>
''') + COUNTER_JS
