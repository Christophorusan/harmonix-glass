/* Harmonix glass mockup — demo interaction layer. No real wallet, no real orders. */
(function () {
  "use strict";

  var DEMO_ADDR = "0x7Fa9…3Cd2";
  var BAL = { USDC: 5240.18, HYPE: 118.4, KHYPE: 312.6 };
  try {
    var saved = JSON.parse(localStorage.getItem("hmx_bal") || "null");
    if (saved) BAL = saved;
  } catch (e) {}

  /* real wallet (EIP-1193) with demo fallback */
  var realAddr = null;
  var HYPEREVM = {
    chainId: "0x3e7",
    chainName: "HyperEVM",
    nativeCurrency: { name: "HYPE", symbol: "HYPE", decimals: 18 },
    rpcUrls: ["https://rpc.hyperliquid.xyz/evm"],
    blockExplorerUrls: ["https://hyperevmscan.io"]
  };
  function short(a) { return a.slice(0, 6) + "…" + a.slice(-4); }
  function ADDR() { return realAddr ? short(realAddr) : DEMO_ADDR; }

  function switchToHyperEVM(eth) {
    return eth.request({ method: "wallet_switchEthereumChain", params: [{ chainId: HYPEREVM.chainId }] })
      .catch(function (e) {
        if (e && (e.code === 4902 || /unrecognized|not.*added/i.test(e.message || ""))) {
          return eth.request({ method: "wallet_addEthereumChain", params: [HYPEREVM] });
        }
        throw e;
      });
  }

  function fetchNativeBal(eth) {
    eth.request({ method: "eth_getBalance", params: [realAddr, "latest"] })
      .then(function (hex) {
        BAL.HYPE = parseInt(hex, 16) / 1e18;
        refreshWallet();
      })
      .catch(function () {});
  }

  function connectInjected(eth) {
    return eth.request({ method: "eth_requestAccounts" }).then(function (accs) {
      if (!accs || !accs.length) throw new Error("no accounts");
      realAddr = accs[0];
      localStorage.setItem("hmx_w", "1");
      localStorage.setItem("hmx_mode", "injected");
      toast("Connected " + short(realAddr));
      switchToHyperEVM(eth).then(function () { fetchNativeBal(eth); }).catch(function () { fetchNativeBal(eth); });
      refreshWallet();
    });
  }

  function restoreInjected() {
    var eth = window.ethereum;
    if (!eth || localStorage.getItem("hmx_mode") !== "injected") return;
    eth.request({ method: "eth_accounts" }).then(function (accs) {
      if (accs && accs.length) {
        realAddr = accs[0];
        fetchNativeBal(eth);
      } else {
        localStorage.removeItem("hmx_w");
        localStorage.removeItem("hmx_mode");
      }
      refreshWallet();
    }).catch(function () {});
    if (eth.on && !eth._hmxBound) {
      eth._hmxBound = true;
      eth.on("accountsChanged", function (accs) {
        if (accs && accs.length) { realAddr = accs[0]; fetchNativeBal(eth); toast("Account changed — " + short(realAddr)); }
        else { realAddr = null; localStorage.removeItem("hmx_w"); localStorage.removeItem("hmx_mode"); toast("Wallet disconnected"); }
        refreshWallet();
      });
      eth.on("chainChanged", function () { if (realAddr) fetchNativeBal(eth); });
    }
  }

  function on() { return localStorage.getItem("hmx_w") === "1"; }
  function saveBal() { try { localStorage.setItem("hmx_bal", JSON.stringify(BAL)); } catch (e) {} }
  function fmt(n, d) {
    if (d === undefined) d = 2;
    return n.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function num(el) { return parseFloat((el && el.value || "").replace(/,/g, "")) || 0; }
  function set(id, txt) { var el = document.getElementById(id); if (el) el.textContent = txt; }

  /* ---------- toasts ---------- */
  var toastBox = null;
  function toast(msg) {
    if (!toastBox) {
      toastBox = document.createElement("div");
      toastBox.className = "toasts";
      document.body.appendChild(toastBox);
    }
    var t = document.createElement("div");
    t.className = "toast";
    t.textContent = msg;
    toastBox.appendChild(t);
    requestAnimationFrame(function () { t.classList.add("show"); });
    setTimeout(function () {
      t.classList.remove("show");
      setTimeout(function () { t.remove(); }, 300);
    }, 2800);
  }

  /* ---------- wallet ---------- */
  function refreshWallet() {
    var isOn = on();
    document.querySelectorAll(".connect-btn").forEach(function (b) {
      b.textContent = isOn ? ADDR() : (b.closest(".mhead") ? "Connect" : "Connect wallet");
      b.classList.toggle("addr", isOn);
      b.title = isOn ? "Click to disconnect" : (window.ethereum ? "Connect wallet" : "Connect demo wallet");
    });
    document.querySelectorAll("[data-bal]").forEach(function (el) {
      var a = el.dataset.bal;
      el.textContent = (isOn ? fmt(BAL[a] || 0) : "0.00") + " " + a;
    });
    document.querySelectorAll("[data-balv]").forEach(function (el) {
      el.textContent = isOn ? fmt(BAL[el.dataset.balv] || 0) : "0.00";
    });
    document.querySelectorAll("[data-walletbal]").forEach(function (el) {
      el.textContent = isOn ? fmt(BAL[el.dataset.walletbal] || 0) : "0";
    });
    var note = document.getElementById("acct-note");
    if (note && !note.dataset.filled) note.textContent = isOn ? "No open positions yet." : "Connect wallet to view your account";
    updateTradeCta();
    updateSwapCta();
    updateDepCta();
  }

  function toggleWallet() {
    if (on()) {
      realAddr = null;
      localStorage.removeItem("hmx_w");
      localStorage.removeItem("hmx_mode");
      toast("Wallet disconnected");
      refreshWallet();
      return;
    }
    if (window.ethereum) {
      connectInjected(window.ethereum).catch(function (e) {
        if (e && e.code === 4001) { toast("Connection rejected"); return; }
        localStorage.setItem("hmx_w", "1");
        localStorage.setItem("hmx_mode", "demo");
        toast("Wallet unavailable — demo wallet connected");
        refreshWallet();
      });
    } else {
      localStorage.setItem("hmx_w", "1");
      localStorage.setItem("hmx_mode", "demo");
      toast("No wallet extension found — demo wallet connected");
      refreshWallet();
    }
  }

  /* ---------- perps ---------- */
  var tp = document.getElementById("trade-panel");
  var PX = tp ? parseFloat(tp.dataset.price) : 0;
  var lev = 20, side = "long", mode = "market";
  var LEVS = [5, 10, 20, 50];

  function updateTradeCta() {
    var c = document.getElementById("trade-cta");
    if (!c) return;
    var s = num(document.getElementById("size-in"));
    if (!on()) { c.textContent = "Connect wallet to trade"; c.classList.remove("sell"); return; }
    var verb = side === "long" ? "Buy / Long" : "Sell / Short";
    c.textContent = s ? verb + " " + fmt(s / PX, 2) + " HYPE" : verb + " HYPE";
    c.classList.toggle("sell", side === "short");
  }

  function updTrade() {
    var s = num(document.getElementById("size-in"));
    set("ov", s ? "$" + fmt(s) : "N/A");
    set("mr", s ? "$" + fmt(s / lev) : "N/A");
    var liq = side === "long" ? PX * (1 - 0.95 / lev) : PX * (1 + 0.95 / lev);
    set("lq", s ? fmt(liq) : "N/A");
    updateTradeCta();
  }

  if (tp) {
    var sizeIn = document.getElementById("size-in");
    if (sizeIn) sizeIn.addEventListener("input", updTrade);

    tp.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.id === "lev-btn") {
        lev = LEVS[(LEVS.indexOf(lev) + 1) % LEVS.length];
        b.textContent = lev + "x";
        b.classList.add("active");
        toast("Leverage set to " + lev + "x (demo)");
        updTrade();
        return;
      }
      if (b.dataset.side) { side = b.dataset.side; updTrade(); }
      if (b.dataset.mode) {
        mode = b.dataset.mode;
        var lf = document.getElementById("limit-field");
        if (lf) lf.hidden = mode !== "limit";
        if (mode === "pro") toast("Pro mode — demo only");
      }
      if (b.id === "trade-cta") {
        if (!on()) { toggleWallet(); return; }
        var s = num(sizeIn);
        if (!s) { toast("Enter a size first"); return; }
        if (s > (BAL.USDC || 0)) { toast("Insufficient USDC (demo balance " + fmt(BAL.USDC) + ")"); return; }
        var qty = s / PX;
        placePosition(side, qty, s);
        toast((side === "long" ? "Long" : "Short") + " " + fmt(qty, 2) + " HYPE @ " + fmt(PX) + " — demo order filled");
        sizeIn.value = "";
        updTrade();
      }
    });
  }

  function placePosition(side, qty, notional) {
    var note = document.getElementById("acct-note");
    if (!note) return;
    note.dataset.filled = "1";
    note.classList.remove("empty-state");
    note.innerHTML = "";
    var tbl = document.createElement("table");
    tbl.className = "gtable";
    tbl.innerHTML =
      "<thead><tr><th>Position</th><th class='r'>Size</th><th class='r'>Entry</th><th class='r'>Leverage</th><th class='r'>PnL</th></tr></thead>" +
      "<tbody><tr><td>" + (side === "long" ? "Long" : "Short") + " HYPE-USD</td>" +
      "<td class='r'>" + fmt(qty, 2) + " HYPE</td>" +
      "<td class='r'>" + fmt(PX) + "</td>" +
      "<td class='r'>" + lev + "x</td>" +
      "<td class='r' style='color:#62d98b'>+$0.00</td></tr></tbody>";
    note.appendChild(tbl);
    var tabs = document.querySelectorAll(".positions-panel .ptabs button");
    tabs.forEach(function (t) { t.classList.toggle("active", /Positions/.test(t.textContent)); });
  }

  /* ---------- spot swap ---------- */
  var sp = document.getElementById("swap-panel");
  var RATE = sp ? parseFloat(sp.dataset.rate) : 0;
  var dir = "buy"; // buy: USDC -> HYPE

  function updateSwapCta() {
    var c = document.getElementById("swap-cta");
    if (!c) return;
    c.textContent = on() ? (dir === "buy" ? "Buy HYPE" : "Sell HYPE") : "Connect wallet to swap";
    c.classList.toggle("sell", dir === "sell");
  }

  function updSwap() {
    var payIn = document.getElementById("pay-in");
    var rcvIn = document.getElementById("rcv-in");
    if (!payIn || !rcvIn) return;
    var v = num(payIn);
    rcvIn.value = v ? fmt(dir === "buy" ? v / RATE : v * RATE) : "";
  }

  if (sp) {
    var payIn = document.getElementById("pay-in");
    if (payIn) payIn.addEventListener("input", updSwap);
    sp.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.dir) {
        dir = b.dataset.dir;
        set("pay-unit", dir === "buy" ? "USDC" : "HYPE");
        set("rcv-unit", dir === "buy" ? "HYPE" : "USDC");
        var pi = document.getElementById("pay-in");
        if (pi) pi.value = "";
        var ri = document.getElementById("rcv-in");
        if (ri) ri.value = "";
        updateSwapCta();
      }
      if (b.id === "swap-cta") {
        if (!on()) { toggleWallet(); return; }
        var v = num(document.getElementById("pay-in"));
        if (!v) { toast("Enter an amount first"); return; }
        var payA = dir === "buy" ? "USDC" : "HYPE";
        var rcvA = dir === "buy" ? "HYPE" : "USDC";
        if (v > (BAL[payA] || 0)) { toast("Insufficient " + payA + " (demo balance " + fmt(BAL[payA]) + ")"); return; }
        var out = dir === "buy" ? v / RATE : v * RATE;
        BAL[payA] -= v;
        BAL[rcvA] = (BAL[rcvA] || 0) + out;
        saveBal();
        toast("Swapped " + fmt(v) + " " + payA + " → " + fmt(out) + " " + rcvA + " (demo)");
        document.getElementById("pay-in").value = "";
        document.getElementById("rcv-in").value = "";
        refreshWallet();
      }
    });
  }

  /* ---------- vault deposit ---------- */
  var depIn = document.getElementById("dep-in");

  function updateDepCta() {
    var c = document.getElementById("dep-cta");
    if (!c) return;
    c.textContent = on() ? "Deposit" : "Connect wallet";
  }

  function updDep() {
    if (!depIn) return;
    var v = num(depIn);
    var apy = parseFloat(depIn.dataset.apy) || 0;
    var px = parseFloat(depIn.dataset.px) || 1;
    set("dep-val", "$" + fmt(v * px));
    set("dep-earn", v ? "~$" + fmt(v * px * apy / 100) + " / yr" : "—");
  }

  if (depIn) {
    depIn.addEventListener("input", updDep);
    document.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.frac) {
        if (!on()) { toast("Connect a wallet first"); return; }
        var asset = depIn.dataset.asset;
        depIn.value = fmt((BAL[asset] || 0) * parseFloat(b.dataset.frac), 2).replace(/,/g, "");
        updDep();
      }
      if (b.id === "dep-cta") {
        if (!on()) { toggleWallet(); return; }
        var v = num(depIn);
        var asset = depIn.dataset.asset;
        if (!v) { toast("Enter an amount first"); return; }
        if (v > (BAL[asset] || 0)) { toast("Insufficient " + asset + " (demo balance " + fmt(BAL[asset]) + ")"); return; }
        BAL[asset] -= v;
        saveBal();
        toast("Deposited " + fmt(v) + " " + asset + " (demo)");
        depIn.value = "";
        updDep();
        refreshWallet();
      }
    });
  }

  /* ---------- charts: timeframe redraw ---------- */
  function lcg(seed) {
    var s = seed >>> 0;
    return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }
  function drawCandles(svg, seed) {
    var W = 760, H = 300, N = 46, cw = W / N;
    var rnd = lcg(seed);
    var lo = 42.0, hi = 46.5, price = 44.0;
    function ym(p) { return H - (p - lo) / (hi - lo) * H; }
    var out = [];
    for (var gy = 1; gy < 6; gy++) {
      var y = H * gy / 6;
      out.push('<line x1="0" y1="' + y.toFixed(1) + '" x2="' + W + '" y2="' + y.toFixed(1) + '" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>');
    }
    for (var i = 0; i < N; i++) {
      var o = price;
      var c = Math.max(lo + 0.2, Math.min(hi - 0.2, price + (rnd() - 0.47) * 1.15));
      var top = Math.max(o, c) + rnd() * 0.3 + 0.05;
      var bot = Math.min(o, c) - rnd() * 0.3 - 0.05;
      var col = c >= o ? "#4fc776" : "#e0605d";
      var x = i * cw + cw * 0.5;
      out.push('<line x1="' + x.toFixed(1) + '" y1="' + ym(top).toFixed(1) + '" x2="' + x.toFixed(1) + '" y2="' + ym(bot).toFixed(1) + '" stroke="' + col + '" stroke-width="1"/>');
      var y1 = ym(Math.max(o, c)), y2 = ym(Math.min(o, c));
      out.push('<rect x="' + (i * cw + cw * 0.18).toFixed(1) + '" y="' + y1.toFixed(1) + '" width="' + (cw * 0.64).toFixed(1) + '" height="' + Math.max(2, y2 - y1).toFixed(1) + '" rx="1" fill="' + col + '"/>');
      price = c;
    }
    var ly = ym(price);
    out.push('<line x1="0" y1="' + ly.toFixed(1) + '" x2="' + W + '" y2="' + ly.toFixed(1) + '" stroke="rgba(215,251,95,0.5)" stroke-width="1" stroke-dasharray="4 4"/>');
    out.push('<rect x="' + (W - 56) + '" y="' + (ly - 9).toFixed(1) + '" width="52" height="18" rx="4" fill="#2c4a1f"/>');
    out.push('<text x="' + (W - 52) + '" y="' + (ly + 4).toFixed(1) + '" font-size="11" fill="#d7fb5f" font-family="Poppins, sans-serif">' + price.toFixed(2) + "</text>");
    svg.innerHTML = out.join("");
  }
  var TF_SEEDS = { "1m": 3, "5m": 13, "15m": 19, "1h": 7, "4h": 23, "1d": 31 };
  document.querySelectorAll(".tf button[data-tf]").forEach(function (b) {
    b.addEventListener("click", function () {
      var svg = b.closest(".panel").querySelector("svg.candles");
      if (svg) drawCandles(svg, TF_SEEDS[b.dataset.tf] || 7);
    });
  });

  /* ---------- order book / recent trades tabs ---------- */
  function buildTrades(host, base) {
    var rnd = lcg(97);
    var rows = ['<div class="ob-head"><span>Price</span><span>Size</span><span>Time</span></div>'];
    var t = new Date();
    for (var i = 0; i < 13; i++) {
      var up = rnd() > 0.45;
      var p = base + (rnd() - 0.5) * 0.4;
      var sz = 40 + rnd() * 900;
      t = new Date(t.getTime() - (20 + rnd() * 90) * 1000);
      var hh = ("0" + t.getHours()).slice(-2) + ":" + ("0" + t.getMinutes()).slice(-2) + ":" + ("0" + t.getSeconds()).slice(-2);
      rows.push('<div class="ob-row ' + (up ? "bid" : "ask") + '"><span>' + p.toFixed(2) + "</span><span>" + sz.toFixed(1) + "</span><span>" + hh + "</span></div>");
    }
    host.innerHTML = rows.join("");
  }
  document.querySelectorAll("[data-obtab]").forEach(function (b) {
    b.addEventListener("click", function () {
      var panel = b.closest(".panel");
      var book = panel.querySelector(".ob-wrap");
      var trades = panel.querySelector(".tr-wrap");
      if (!book || !trades) return;
      var showTrades = b.dataset.obtab === "trades";
      book.hidden = showTrades;
      trades.hidden = !showTrades;
      if (showTrades && !trades.dataset.built) {
        buildTrades(trades, PX || RATE || 43);
        trades.dataset.built = "1";
      }
    });
  });

  /* ---------- global click handling ---------- */
  document.addEventListener("click", function (e) {
    var cb = e.target.closest(".connect-btn");
    if (cb) { e.preventDefault(); toggleWallet(); return; }

    var seg = e.target.closest(".seg, .tf, .ptabs, .vtabs, .tabs");
    var btn = e.target.closest("button");
    if (seg && btn && seg.contains(btn) && btn.id !== "lev-btn") {
      seg.querySelectorAll("button").forEach(function (x) { x.classList.remove("active"); });
      btn.classList.add("active");
      if (btn.closest(".vtabs") && /My position/.test(btn.textContent)) {
        toast(on() ? "No position in this vault yet (demo)" : "Connect a wallet to see your position");
      }
    }

    var ghost = e.target.closest(".ghost-btn");
    if (ghost && !ghost.dataset.frac) {
      toast(on() ? "Demo mockup — action simulated" : "Connect a wallet first");
    }
  });

  restoreInjected();
  refreshWallet();
})();
