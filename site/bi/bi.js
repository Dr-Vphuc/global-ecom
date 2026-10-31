/* Dashboard BI — global-ecom.
 *
 * Dữ liệu: data/world.json (danh mục + chuỗi theo nước) và data/c/<ISO3>.json
 * (tải khi chọn nước), do src/build_bi.py dựng. Giá trị tính bằng nghìn USD.
 *
 * Trạng thái: bộ lọc chung (nước, năm) nằm trên #hash để gửi link được; mỗi thẻ
 * giữ bộ lọc riêng của nó và chỉ thẻ đó vẽ lại khi bộ lọc riêng đổi.
 *
 * Màu: màu sắc chỉ dùng cho NGÀNH (style guide §3.1). Mọi thứ khác là mực và xám.
 */
(function () {
  "use strict";

  var INK = "#15171c", INK2 = "#393e48", MUTED = "#5a606c", GREY = "#b4b0a6",
      GRID = "#ebe8e1", RULE = "#d9d6cd", DOWN = "#8c3b2e";
  var FONT = '"Be Vietnam Pro", "Segoe UI", Arial, sans-serif';
  var ASEAN = ["BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM"];
  var CFG = { displaylogo: false, responsive: true, displayModeBar: "hover",
              modeBarButtons: [["toImage"]],
              toImageButtonOptions: { format: "png", scale: 2 } };

  var W = null, C = {}, S = { iso: "VNM", y: null };
  var nuoc = {}, nganh = {}, hs2Ng = [], sumX = [], sumWp = [], hang = [];

  /* ---------------------------------------------------------- định dạng */

  var nfCache = {};
  function f(v, d) {
    d = d || 0;
    if (!nfCache[d]) nfCache[d] = new Intl.NumberFormat("vi-VN",
      { minimumFractionDigits: d, maximumFractionDigits: d });
    return nfCache[d].format(v);
  }
  // k: nghìn USD → [số, đơn vị]
  function usdP(k) {
    var a = Math.abs(k);
    if (a >= 1e9) return [f(k / 1e9, 2), "nghìn tỷ USD"];
    if (a >= 1e6) return [f(k / 1e6, 1), "tỷ USD"];
    if (a >= 1e3) return [f(k / 1e3, 1), "triệu USD"];
    return [f(k, 0), "nghìn USD"];
  }
  function usd(k) { var p = usdP(k); return p[0] + " " + p[1]; }
  function pct(v, d) { return f(v, d === undefined ? 1 : d) + "%"; }
  function sum(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i] || 0; return s; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function mix(hex, t) {          // pha màu ngành với trắng, t ∈ [0,1)
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    function c(v) { return Math.round(v + (255 - v) * t); }
    return "rgb(" + c(r) + "," + c(g) + "," + c(b) + ")";
  }

  function merge(a, b) {
    var o = {}, k;
    for (k in a) o[k] = a[k];
    for (k in b) {
      o[k] = (b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) &&
              a[k] && typeof a[k] === "object") ? merge(a[k], b[k]) : b[k];
    }
    return o;
  }
  function L(x) {
    return merge({
      font: { family: FONT, size: 12, color: INK2 }, separators: ",.",
      margin: { l: 56, r: 16, t: 14, b: 36 }, paper_bgcolor: "#fff", plot_bgcolor: "#fff",
      showlegend: false, hovermode: "closest",
      hoverlabel: { font: { family: FONT, size: 12, color: "#fff" }, bgcolor: INK, bordercolor: INK },
      xaxis: { gridcolor: GRID, linecolor: RULE, zeroline: false, tickfont: { size: 11 } },
      yaxis: { gridcolor: GRID, linecolor: RULE, zeroline: false, tickfont: { size: 11 } }
    }, x || {});
  }
  function yearLine(y) {
    return { type: "line", xref: "x", yref: "paper", x0: y, x1: y, y0: 0, y1: 1,
             line: { color: MUTED, width: 1, dash: "dot" } };
  }
  function draw(card, traces, layout) {
    Plotly.react(card.querySelector(".plot"), traces, L(layout), CFG);
  }

  /* ---------------------------------------------------------- dữ liệu */

  function idx() { return W.nam.indexOf(S.y); }
  function cs(iso) { return W.cs[iso]; }

  function prep() {
    W.nuoc.forEach(function (n) { nuoc[n.iso] = n; });
    W.nganh.forEach(function (g) { nganh[g.id] = g; });
    hs2Ng = W.hs2.map(function (h) { return h.ng; });
    W.nam.forEach(function (_, i) {
      var s = 0, r = [];
      Object.keys(W.cs).forEach(function (iso) {
        var x = W.cs[iso].x[i];
        if (x > 0) { s += x; r.push([iso, x]); }
      });
      sumX[i] = s;
      r.sort(function (a, b) { return b[1] - a[1]; });
      var h = {};
      r.forEach(function (p, k) { h[p[0]] = k + 1; });
      hang[i] = { h: h, n: r.length, ds: r };
      sumWp[i] = sum(W.wp[i]);
    });
  }

  function rca(c, i, j) {
    var xc = sum(c.p[i]), xp = W.wp[i][j];
    if (!xc || !xp || !sumWp[i]) return null;
    return (c.p[i][j] / xc) / (xp / sumWp[i]);
  }

  function load(iso) {
    if (C[iso]) return Promise.resolve(C[iso]);
    return fetch("data/c/" + iso + ".json").then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (d) {
      d.sp = d.p.map(sum);
      C[iso] = d;
      return d;
    });
  }

  /* ---------------------------------------------------------- KPI */

  function spark(arr, i, invert) {
    var v = arr.map(function (x) { return x === null || x === undefined ? NaN : x; });
    var ok = v.filter(function (x) { return !isNaN(x); });
    if (ok.length < 2) return "";
    var lo = Math.min.apply(null, ok), hi = Math.max.apply(null, ok), rg = (hi - lo) || 1;
    var n = v.length, pts = [], dot = "";
    v.forEach(function (x, k) {
      if (isNaN(x)) return;
      var t = (x - lo) / rg, px = 2 + k / (n - 1) * 116, py = 2 + (invert ? t : 1 - t) * 24;
      pts.push(px.toFixed(1) + "," + py.toFixed(1));
      if (k === i) dot = '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="2.6"/>';
    });
    return '<svg class="spark" viewBox="0 0 120 28" preserveAspectRatio="none" aria-hidden="true">' +
      '<polyline points="' + pts.join(" ") + '"/>' + dot + "</svg>";
  }

  function delta(now, prev, kind) {
    // kind: "pct" (% thay đổi), "pp" (điểm %), "abs" (USD), "rank" (bậc, nhỏ là tốt), "n"
    if (prev === null || prev === undefined || now === null || now === undefined) return "&nbsp;";
    var d, txt, up;
    if (kind === "pct") { if (!prev) return "&nbsp;"; d = (now - prev) / Math.abs(prev) * 100; txt = pct(Math.abs(d)); }
    else if (kind === "pp" || kind === "pp1") {
      d = now - prev; txt = f(Math.abs(d), kind === "pp" ? 3 : 1) + " đ.%";
    }
    else if (kind === "abs") { d = now - prev; txt = usd(Math.abs(d)); }
    else if (kind === "rank") { d = prev - now; txt = f(Math.abs(d)) + " bậc"; }
    else { d = now - prev; txt = f(Math.abs(d)); }
    var nam = '<span class="kpi__vs">/ ' + (S.y - 1) + "</span>";
    if (d === 0) return "= " + nam;
    up = d > 0;
    return '<b class="' + (up ? "up" : "down") + '">' + (up ? "▲ " : "▼ ") + txt + "</b> " + nam;
  }

  function kpis() {
    var i = idx(), c = cs(S.iso), d = C[S.iso], el = document.getElementById("kpis");
    var nRca = W.nam.map(function (_, k) {
      if (!d.sp[k]) return null;
      var n = 0;
      for (var j = 0; j < W.hs2.length; j++) { var r = rca(d, k, j); if (r !== null && r >= 1) n++; }
      return n;
    });
    var cc = c.x.map(function (x, k) { return x - c.m[k]; });
    var tp = c.x.map(function (x, k) { return sumX[k] ? x / sumX[k] * 100 : null; });
    var hx = W.nam.map(function (_, k) { return hang[k].h[S.iso] || null; });
    // Tỷ trọng ba thị trường lớn nhất. Không dùng chỉ số đa dạng (diversity) của
    // Atlas: năm 2004 nó gần gấp đôi ở MỌI nước rồi rơi lại — lỗi dữ liệu (A20).
    var top3 = W.nam.map(function (_, k) {
      var v = d.x.map(function (r) { return r[k]; }).sort(function (a, b) { return b - a; });
      var tot = sum(v) + d.xk[k];
      return tot ? (v[0] + v[1] + v[2]) / tot * 100 : null;
    });
    var p = function (a) { return i > 0 ? a[i - 1] : null; };
    var items = [
      ["Xuất khẩu", usdP(c.x[i]), delta(c.x[i], p(c.x), "pct"), c.x],
      ["Nhập khẩu", usdP(c.m[i]), delta(c.m[i], p(c.m), "pct"), c.m],
      ["Cán cân thương mại", (function () { var u = usdP(cc[i]); if (cc[i] > 0) u[0] = "+" + u[0]; return u; })(),
        delta(cc[i], p(cc), "abs"), cc],
      ["Thị phần xuất khẩu", [tp[i] === null ? "—" : f(tp[i], 3), "%"], delta(tp[i], p(tp), "pp"), tp],
      ["Hạng xuất khẩu", [hx[i] ? f(hx[i]) : "—", "/" + hang[i].n], delta(hx[i], p(hx), "rank"), hx, true],
      ["Hạng ECI", [c.er[i] ? f(c.er[i]) : "—", c.en[i] ? "/" + c.en[i] : ""], delta(c.er[i], p(c.er), "rank"), c.er, true],
      ["Nhóm HS2 có RCA ≥ 1", [nRca[i] === null ? "—" : f(nRca[i]), "/" + W.hs2.length], delta(nRca[i], p(nRca), "n"), nRca],
      ["Top 3 thị trường", [top3[i] === null ? "—" : f(top3[i], 1), "%"], delta(top3[i], p(top3), "pp1"), top3]
    ];
    el.innerHTML = items.map(function (it) {
      return '<li class="kpi"><p class="kpi__label" title="' + esc(it[0]) + '">' + esc(it[0]) + "</p>" +
        '<p class="kpi__value">' + esc(it[1][0]) + '<span class="kpi__unit">' + esc(it[1][1]) + "</span></p>" +
        '<p class="kpi__delta">' + it[2] + "</p>" + spark(it[3], i, it[4]) + "</li>";
    }).join("");
  }

  /* ---------------------------------------------------------- thẻ */

  var CARDS = {};

  function card(id, render) {
    var el = document.getElementById(id), st = {};
    el.querySelectorAll(".seg").forEach(function (g) {
      st[g.dataset.key] = g.querySelector('[aria-pressed="true"]').dataset.v;
      g.addEventListener("click", function (ev) {
        var b = ev.target.closest("button");
        if (!b) return;
        g.querySelectorAll("button").forEach(function (x) {
          x.setAttribute("aria-pressed", x === b ? "true" : "false");
        });
        st[g.dataset.key] = b.dataset.v;
        go();
      });
    });
    el.querySelectorAll("select[data-key], input[data-key]").forEach(function (s) {
      s.addEventListener(s.tagName === "INPUT" ? "input" : "change", function () {
        st[s.dataset.key] = s.value;
        go();
      });
    });
    function go() { if (C[S.iso]) render(el, st); }
    CARDS[id] = { el: el, st: st, go: go };
    return el;
  }
  function setOptions(sel, opts, keep) {
    var cur = keep !== undefined ? keep : sel.value;
    sel.innerHTML = opts.map(function (o) {
      return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + "</option>";
    }).join("");
    if (opts.some(function (o) { return String(o[0]) === String(cur); })) sel.value = cur;
    return sel.value;
  }
  function nganhOpts() {
    return [["all", "Tất cả ngành"]].concat(W.nganh.map(function (g) { return [g.id, g.ten]; }));
  }

  /* A. Kim ngạch theo năm */
  function rKimNgach(el, st) {
    var c = cs(S.iso), a = W.nam.indexOf(+st.tu), b = W.nam.indexOf(+st.den);
    if (a > b) { var t = a; a = b; b = t; }
    var ys = W.nam.slice(a, b + 1), tr;
    if (st.chi === "cc") {
      var v = ys.map(function (_, k) { return (c.x[a + k] - c.m[a + k]) / 1e6; });
      tr = [{ type: "bar", x: ys, y: v, marker: { color: v.map(function (x) { return x >= 0 ? INK : GREY; }) },
              hovertemplate: "%{x}: %{y:,.1f} tỷ USD<extra>Cán cân</extra>" }];
    } else {
      tr = [
        { type: "scatter", mode: "lines", name: "Xuất khẩu", x: ys,
          y: ys.map(function (_, k) { return c.x[a + k] / 1e6; }), line: { color: INK, width: 2.4 },
          hovertemplate: "%{y:,.1f} tỷ USD" },
        { type: "scatter", mode: "lines", name: "Nhập khẩu", x: ys,
          y: ys.map(function (_, k) { return c.m[a + k] / 1e6; }), line: { color: GREY, width: 2.4 },
          hovertemplate: "%{y:,.1f} tỷ USD" }
      ];
    }
    draw(el, tr, {
      hovermode: "x unified", showlegend: st.chi !== "cc",
      legend: { orientation: "h", x: 0, y: 1.1, font: { size: 12 } },
      margin: { t: st.chi === "cc" ? 14 : 34 },
      xaxis: { dtick: ys.length > 15 ? 5 : 1, range: [ys[0] - 0.5, ys[ys.length - 1] + 0.5] },
      yaxis: { title: { text: "tỷ USD", font: { size: 11 } }, zeroline: st.chi === "cc", zerolinecolor: RULE },
      shapes: S.y >= ys[0] && S.y <= ys[ys.length - 1] ? [yearLine(S.y)] : []
    });
  }

  /* B. Cơ cấu ngành theo năm */
  function rNganh(el, st) {
    var d = C[S.iso], tr = [];
    if (st.nganh === "all") {
      W.nganh.forEach(function (g) {
        var y = W.nam.map(function (_, i) {
          var s = 0;
          for (var j = 0; j < hs2Ng.length; j++) if (hs2Ng[j] === g.id) s += d.p[i][j];
          return s / 1e6;
        });
        tr.push({ type: "scatter", mode: "lines", stackgroup: "a", groupnorm: st.kieu === "tt" ? "percent" : "",
                  name: g.ten, x: W.nam, y: y, line: { width: 0.5, color: "#fff" }, fillcolor: g.mau,
                  hovertemplate: st.kieu === "tt" ? "%{y:,.1f}%<extra>" + esc(g.ten) + "</extra>"
                                                  : "%{y:,.2f} tỷ USD<extra>" + esc(g.ten) + "</extra>" });
      });
    } else {
      var gid = +st.nganh, g = nganh[gid], i = idx();
      var js = [];
      for (var j = 0; j < hs2Ng.length; j++) if (hs2Ng[j] === gid) js.push(j);
      js.sort(function (p, q) { return d.p[i][q] - d.p[i][p]; });
      var top = js.slice(0, 7), rest = js.slice(7);
      top.forEach(function (j, k) {
        var h = W.hs2[j];
        tr.push({ type: "scatter", mode: "lines", stackgroup: "a", groupnorm: st.kieu === "tt" ? "percent" : "",
                  name: h.ma + " " + h.ten, x: W.nam, y: W.nam.map(function (_, t) { return d.p[t][j] / 1e6; }),
                  line: { width: 0.5, color: "#fff" }, fillcolor: mix(g.mau, k * 0.11),
                  hovertemplate: (st.kieu === "tt" ? "%{y:,.1f}%" : "%{y:,.2f} tỷ USD") +
                    "<extra>" + esc(h.ma + " " + h.ten) + "</extra>" });
      });
      if (rest.length) {
        tr.push({ type: "scatter", mode: "lines", stackgroup: "a", groupnorm: st.kieu === "tt" ? "percent" : "",
                  name: "Nhóm khác", x: W.nam, y: W.nam.map(function (_, t) {
                    var s = 0; rest.forEach(function (j) { s += d.p[t][j]; }); return s / 1e6; }),
                  line: { width: 0.5, color: "#fff" }, fillcolor: "#dcd9d0",
                  hovertemplate: (st.kieu === "tt" ? "%{y:,.1f}%" : "%{y:,.2f} tỷ USD") + "<extra>Nhóm khác</extra>" });
      }
    }
    draw(el, tr, {
      showlegend: true, hovermode: "x unified",
      legend: { orientation: "h", x: 0, y: -0.14, yanchor: "top", font: { size: 10.5 },
                traceorder: "normal", itemwidth: 30 },
      margin: { r: 12, b: 96 },
      xaxis: { dtick: 5 },
      yaxis: { title: { text: st.kieu === "tt" ? "%" : "tỷ USD", font: { size: 11 } },
               range: st.kieu === "tt" ? [0, 100] : null },
      shapes: [yearLine(S.y)]
    });
  }

  /* C. Đối tác */
  function rDoiTac(el, st) {
    var d = C[S.iso], i = idx(), arr = st.chieu === "x" ? d.x : d.m;
    var tot = sum(arr.map(function (r) { return r[i]; })) + (st.chieu === "x" ? d.xk : d.mk)[i];
    var rows = d.dt.map(function (iso, k) { return [iso, arr[k][i]]; }).filter(function (r) {
      return r[1] > 0 && (st.kv === "all" || (nuoc[r[0]] && nuoc[r[0]].kv === st.kv));
    });
    rows.sort(function (a, b) { return b[1] - a[1]; });
    rows = rows.slice(0, +st.top);
    var name = rows.map(function (r) { return nuoc[r[0]] ? nuoc[r[0]].ten : r[0]; });
    draw(el, [{
      type: "bar", orientation: "h", y: name, x: rows.map(function (r) { return r[1] / 1e6; }),
      marker: { color: INK },
      text: rows.map(function (r) { return usd(r[1]) + " · " + pct(tot ? r[1] / tot * 100 : 0); }),
      textposition: "outside", cliponaxis: false, textfont: { size: 11, color: INK2 },
      hovertemplate: "%{y}<br>%{text}<extra></extra>"
    }], {
      margin: { l: 120, r: 120, t: 8, b: 30 }, bargap: 0.25,
      yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", tickfont: { size: 11 }, automargin: true },
      xaxis: { title: { text: "tỷ USD", font: { size: 11 } } }
    });
  }

  /* D. Khu vực */
  function rKhuVuc(el, st) {
    var d = C[S.iso], i = idx(), kv = d.kv[st.chieu] || {};
    function shares(t) {
      var tot = 0, o = [];
      Object.keys(kv).forEach(function (k) { tot += kv[k][t]; });
      Object.keys(kv).forEach(function (k) { o.push([k, tot ? kv[k][t] / tot * 100 : 0]); });
      return o;
    }
    var now = shares(i).sort(function (a, b) { return b[1] - a[1]; });
    var keep = now.filter(function (r) { return r[1] >= 1; }).slice(0, 10).map(function (r) { return r[0]; });
    function rows(t) {
      var o = {}, khac = 0;
      shares(t).forEach(function (r) { if (keep.indexOf(r[0]) >= 0) o[r[0]] = r[1]; else khac += r[1]; });
      return keep.map(function (k) { return o[k] || 0; }).concat([khac]);
    }
    var lab = keep.concat(["Khu vực khác"]);
    var cur = rows(i);
    var tr = [{ type: "bar", orientation: "h", y: lab, x: cur, name: String(S.y),
                marker: { color: INK }, text: cur.map(function (v) { return pct(v); }),
                textposition: "outside", cliponaxis: false, textfont: { size: 10.5, color: INK2 },
                hovertemplate: "%{y}: %{x:,.1f}%<extra>" + S.y + "</extra>" }];
    var so = st.so && st.so !== "0" ? +st.so : null;
    if (so && so !== S.y) {
      tr.push({ type: "bar", orientation: "h", y: lab, x: rows(W.nam.indexOf(so)), name: String(so),
                marker: { color: GREY }, hovertemplate: "%{y}: %{x:,.1f}%<extra>" + so + "</extra>" });
    }
    draw(el, tr, {
      barmode: "group", bargap: 0.25, showlegend: tr.length > 1,
      legend: { orientation: "h", x: 0, y: 1.08 },
      margin: { l: 120, r: 44, t: tr.length > 1 ? 30 : 8, b: 30 },
      yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true },
      xaxis: { ticksuffix: "%" }
    });
  }

  /* E. Nhóm hàng HS2 */
  function rMatHang(el, st) {
    var d = C[S.iso], i = idx(), tot = d.sp[i], rows = [];
    for (var j = 0; j < W.hs2.length; j++) {
      if (st.nganh !== "all" && hs2Ng[j] !== +st.nganh) continue;
      var v = d.p[i][j], pv = i > 0 ? d.p[i - 1][j] : 0;
      if (v <= 0) continue;
      var g = pv > 0 ? (v - pv) / pv * 100 : null;
      if (st.xep === "tg" && (g === null || v < 10000)) continue;   // ≥ 10 triệu USD
      rows.push({ j: j, v: v, g: g });
    }
    rows.sort(st.xep === "tg" ? function (a, b) { return b.g - a.g; } : function (a, b) { return b.v - a.v; });
    rows = rows.slice(0, +st.top);
    var lab = rows.map(function (r) { var h = W.hs2[r.j]; return h.ma + " " + h.ten; });
    var x = rows.map(function (r) { return st.xep === "tg" ? r.g : r.v / 1e6; });
    draw(el, [{
      type: "bar", orientation: "h", y: lab, x: x,
      marker: { color: rows.map(function (r) { return nganh[hs2Ng[r.j]].mau; }),
                line: { color: "rgba(0,0,0,0.15)", width: 0.5 } },
      text: rows.map(function (r) {
        return st.xep === "tg" ? (r.g >= 0 ? "+" : "−") + pct(Math.abs(r.g)) + " · " + usd(r.v)
                               : usd(r.v) + " · " + pct(tot ? r.v / tot * 100 : 0);
      }),
      textposition: "outside", cliponaxis: false, textfont: { size: 11, color: INK2 },
      hovertemplate: "%{y}<br>%{text}<extra></extra>"
    }], {
      margin: { l: 210, r: 150, t: 8, b: 30 }, bargap: 0.25,
      yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 11 } },
      xaxis: st.xep === "tg" ? { ticksuffix: "%", zeroline: true, zerolinecolor: RULE }
                             : { title: { text: "tỷ USD", font: { size: 11 } } }
    });
  }

  /* F. RCA × PCI */
  function rRca(el, st) {
    var d = C[S.iso], i = idx(), pts = [];
    for (var j = 0; j < W.hs2.length; j++) {
      if (st.nganh !== "all" && hs2Ng[j] !== +st.nganh) continue;
      var v = d.p[i][j], r = rca(d, i, j), p = W.pci[i][j];
      if (v < +st.san || !r || p === null) continue;
      pts.push({ j: j, v: v, r: r, p: p });
    }
    var vmax = Math.max.apply(null, pts.map(function (q) { return q.v; }).concat([1]));
    var tick = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100];
    draw(el, [{
      type: "scatter", mode: "markers", x: pts.map(function (q) { return q.r; }),
      y: pts.map(function (q) { return q.p; }),
      marker: { size: pts.map(function (q) { return 6 + 34 * Math.sqrt(q.v / vmax); }),
                color: pts.map(function (q) { return nganh[hs2Ng[q.j]].mau; }),
                line: { color: "rgba(0,0,0,0.35)", width: 0.6 }, opacity: 0.9 },
      customdata: pts.map(function (q) {
        var h = W.hs2[q.j];
        return [h.ma + " " + h.ten, f(q.r, 2), f(q.p, 2), usd(q.v)];
      }),
      hovertemplate: "<b>%{customdata[0]}</b><br>RCA %{customdata[1]} · PCI %{customdata[2]}<br>%{customdata[3]}<extra></extra>"
    }], {
      margin: { l: 48, r: 16, t: 10, b: 42 },
      xaxis: { type: "log", title: { text: "RCA (thang log)", font: { size: 11 } },
               tickmode: "array", tickvals: tick, ticktext: tick.map(function (t) { return f(t, t < 1 ? 2 : 0); }) },
      yaxis: { title: { text: "PCI", font: { size: 11 } } },
      shapes: [
        { type: "line", xref: "x", yref: "paper", x0: 1, x1: 1, y0: 0, y1: 1, line: { color: MUTED, width: 1, dash: "dash" } },
        { type: "line", xref: "paper", yref: "y", x0: 0, x1: 1, y0: 0, y1: 0, line: { color: MUTED, width: 1, dash: "dash" } }
      ]
    });
  }

  /* F2. Phần giá trị ở lại trong nước (OECD TiVA). Chỉ Việt Nam, nên không đổi
   * theo bộ lọc quốc gia; theo bộ lọc năm tới 2022, năm TiVA dừng. */
  var dvaNarrow = null;
  function gap2(s) {              // gập tên ngành thành hai dòng, ở chỗ trắng gần giữa nhất
    var mid = s.length / 2, best = -1, i;
    for (i = s.indexOf(" "); i >= 0; i = s.indexOf(" ", i + 1)) {
      if (best < 0 || Math.abs(i - mid) < Math.abs(best - mid)) best = i;
    }
    return best < 0 || s.length <= 16 ? s : s.slice(0, best) + "<br>" + s.slice(best + 1);
  }
  function rDva(el, st) {
    var D = W.dva, foot = el.querySelector("#dva-foot");
    if (!D) { foot.textContent = "Không có dữ liệu TiVA."; return; }
    var k = D.nam.indexOf(S.y), cuoi = D.nam[D.nam.length - 1];
    if (k < 0) k = D.nam.length - 1;
    var rows = [];
    D.ng.forEach(function (id, j) {
      if (D.v[k][j] === null) return;
      rows.push({ id: id, ten: nganh[id].ten, v: D.v[k][j], lo: D.lo[k][j], hi: D.hi[k][j],
                  pci: D.pci[k][j], tt: D.tt[k][j] });
    });
    // Xếp theo PCI giảm dần: ngành khó nhất ở trên cùng (B30).
    rows.sort(function (a, b) { return (b.pci === null ? -9 : b.pci) - (a.pci === null ? -9 : a.pci); });
    // Khổ hẹp: hai cột chữ bên phải không còn chỗ, nên số đặt ngay cuối thanh và
    // bỏ cột PCI (vẫn còn trong hover và trong thứ tự xếp).
    var narrow = el.querySelector(".plot").clientWidth < 600;
    dvaNarrow = narrow;
    var ten = rows.map(function (r) { return narrow ? gap2(r.ten) : r.ten; });
    var rb = D.rb[k];
    var ann = [
      { xref: "x", x: rb, xanchor: "center", yref: "paper", y: 1, yanchor: "bottom",
        text: "Bình quân cả rổ " + pct(rb), showarrow: false, font: { size: 11, color: MUTED } }
    ];
    if (!narrow) {
      ann.push({ xref: "paper", x: 1, xanchor: "left", xshift: 10, yref: "paper", y: 1, yanchor: "bottom",
                 text: "Trong nước", showarrow: false, font: { size: 11, color: MUTED } });
      ann.push({ xref: "paper", x: 1, xanchor: "left", xshift: 76, yref: "paper", y: 1, yanchor: "bottom",
                 text: "PCI", showarrow: false, font: { size: 11, color: MUTED } });
    }
    rows.forEach(function (r, i) {
      if (narrow) {
        ann.push({ xref: "x", x: r.hi, xanchor: "left", xshift: 5, yref: "y", y: ten[i],
                   text: pct(r.v), showarrow: false, font: { size: 11, color: INK } });
        return;
      }
      ann.push({ xref: "paper", x: 1, xanchor: "left", xshift: 10, yref: "y", y: ten[i],
                 text: pct(r.v), showarrow: false, font: { size: 12, color: INK } });
      ann.push({ xref: "paper", x: 1, xanchor: "left", xshift: 76, yref: "y", y: ten[i],
                 text: n2(r.pci, 2, true), showarrow: false, font: { size: 12, color: MUTED } });
    });
    draw(el, [{
      type: "bar", orientation: "h", x: rows.map(function (r) { return r.v; }), y: ten,
      marker: { color: rows.map(function (r) { return nganh[r.id].mau; }),
                line: { color: "#fff", width: 1 } },
      error_x: { type: "data", symmetric: false, color: INK2, thickness: 1, width: 3,
                 array: rows.map(function (r) { return Math.max(0, r.hi - r.v); }),
                 arrayminus: rows.map(function (r) { return Math.max(0, r.v - r.lo); }) },
      customdata: rows.map(function (r) {
        return [r.ten, pct(r.v), f(r.lo, 1), pct(r.hi), n2(r.pci, 2, true), pct(r.tt)];
      }),
      hovertemplate: "<b>%{customdata[0]}</b><br>Giữ lại trong nước: %{customdata[1]}" +
        "<br>Khoảng theo hai cách ghép: %{customdata[2]}–%{customdata[3]}" +
        "<br>PCI %{customdata[4]} · %{customdata[5]} xuất khẩu ghép được<extra></extra>"
    }], {
      margin: narrow ? { l: 112, r: 44, t: 34, b: 36 } : { l: 190, r: 130, t: 34, b: 36 },
      bargap: 0.35, annotations: ann,
      xaxis: { range: [0, 100], fixedrange: true, tickmode: "array", tickvals: [0, 25, 50, 75, 100],
               ticktext: [0, 25, 50, 75, 100].map(function (t) { return f(t, 0) + "%"; }) },
      yaxis: { autorange: "reversed", fixedrange: true, ticks: "", gridcolor: "#fff" },
      shapes: [{ type: "line", xref: "x", yref: "paper", x0: rb, x1: rb, y0: 0, y1: 1,
                 line: { color: MUTED, width: 1, dash: "dash" } }]
    });
    foot.textContent = "Năm TiVA: " + D.nam[k] +
      (S.y > cuoi ? " (TiVA dừng ở " + cuoi + "; bộ lọc năm là " + S.y + ")" : "") +
      " · luôn là Việt Nam, không đổi theo bộ lọc quốc gia · chưa tính ngành Khác (" +
      pct(D.khac[k]) + " xuất khẩu: HS97, HS99 không ghép được) · vạch mảnh là khoảng giữa hai cách ghép HS2 sang ISIC · thanh xếp theo PCI giảm dần";
  }

  /* G. So sánh quốc gia */
  function rSoSanh(el, st) {
    var i = idx(), ds;
    if (st.nhom === "asean") ds = ASEAN.slice();
    else if (st.nhom === "kv") {
      var kv = nuoc[S.iso].kv;
      ds = W.co.filter(function (iso) { return nuoc[iso].kv === kv; });
    } else ds = hang[i].ds.slice(0, 10).map(function (r) { return r[0]; });
    if (ds.indexOf(S.iso) < 0) ds.push(S.iso);
    ds = ds.filter(function (iso) { return W.cs[iso]; });
    function val(iso, t) {
      var c = W.cs[iso];
      if (st.cs === "x") return c.x[t] ? c.x[t] / 1e6 : null;
      if (st.cs === "m") return c.m[t] ? c.m[t] / 1e6 : null;
      if (st.cs === "tp") return sumX[t] && c.x[t] ? c.x[t] / sumX[t] * 100 : null;
      if (st.cs === "er") return c.er[t];
      return c.eci[t];
    }
    var unit = { x: " tỷ USD", m: " tỷ USD", tp: "%", er: "", eci: "" }[st.cs];
    var fmt = { x: ",.1f", m: ",.1f", tp: ",.3f", er: ",.0f", eci: ",.2f" }[st.cs];
    var ordered = ds.filter(function (iso) { return iso !== S.iso; }).concat([S.iso]);
    var ends = [];
    var tr = ordered.map(function (iso) {
      var me = iso === S.iso, y = W.nam.map(function (_, t) { return val(iso, t); });
      var last = -1;
      for (var t = y.length - 1; t >= 0; t--) if (y[t] !== null && y[t] !== undefined) { last = t; break; }
      if (last >= 0) ends.push({ iso: iso, me: me, x: W.nam[last], y: y[last] });
      return { type: "scatter", mode: "lines", name: nuoc[iso].ten, x: W.nam, y: y, connectgaps: false,
               line: { color: me ? INK : GREY, width: me ? 3 : 1.4 },
               hovertemplate: "%{x}: %{y:" + fmt + "}" + unit + "<extra>" + esc(nuoc[iso].ten) + "</extra>" };
    });
    // Nhãn cuối dòng: nước đang chọn trước, rồi các nước còn lại từ trên xuống;
    // bỏ nhãn nào cách nhãn đã đặt dưới 6% chiều cao trục (tên vẫn có khi rê chuột).
    var ys = ends.map(function (e) { return e.y; });
    var span = (Math.max.apply(null, ys) - Math.min.apply(null, ys)) || 1, placed = [], ann = [];
    ends.sort(function (a, b) {
      if (a.me !== b.me) return a.me ? -1 : 1;
      return st.cs === "er" ? a.y - b.y : b.y - a.y;
    }).forEach(function (e) {
      if (!e.me && placed.some(function (p) { return Math.abs(p - e.y) < span * 0.06; })) return;
      placed.push(e.y);
      ann.push({ x: e.x, y: e.y, xanchor: "left", text: " " + esc(nuoc[e.iso].ten), showarrow: false,
                 font: { size: e.me ? 12 : 10.5, color: e.me ? INK : MUTED } });
    });
    draw(el, tr, {
      margin: { l: 56, r: 130, t: 12, b: 32 }, xaxis: { dtick: 5 },
      yaxis: { autorange: st.cs === "er" ? "reversed" : true,
               title: { text: { x: "tỷ USD", m: "tỷ USD", tp: "% thế giới", er: "hạng (1 = cao nhất)", eci: "ECI" }[st.cs],
                        font: { size: 11 } } },
      annotations: ann, shapes: [yearLine(S.y)]
    });
  }

  /* H. Bảng HS2 */
  var sortKey = "gt", sortDir = -1;
  function tblRows(st) {
    var d = C[S.iso], i = idx(), tot = d.sp[i], q = (st.q || "").trim().toLowerCase(), rows = [];
    for (var j = 0; j < W.hs2.length; j++) {
      var h = W.hs2[j], v = d.p[i][j];
      if (v <= 0) continue;
      if (st.nganh && st.nganh !== "all" && h.ng !== +st.nganh) continue;
      if (q && (h.ma + " " + h.ten).toLowerCase().indexOf(q) < 0) continue;
      var pv = i > 0 ? d.p[i - 1][j] : 0;
      rows.push({ ma: h.ma, ten: h.ten, ng: nganh[h.ng].ten, mau: nganh[h.ng].mau, gt: v / 1e3,
                  tt: tot ? v / tot * 100 : 0, tg: pv > 0 ? (v - pv) / pv * 100 : null,
                  rca: rca(d, i, j), pci: W.pci[i][j] });
    }
    rows.sort(function (a, b) {
      var x = a[sortKey], y = b[sortKey];
      if (x === null) return 1;
      if (y === null) return -1;
      return (typeof x === "string" ? x.localeCompare(y, "vi") : x - y) * sortDir;
    });
    return rows;
  }
  function n2(v, d, sign) {
    if (v === null || v === undefined) return "—";
    return (sign && v > 0 ? "+" : "") + f(v, d);
  }
  function rBang(el, st) {
    var rows = tblRows(st);
    el.querySelector("tbody").innerHTML = rows.map(function (r) {
      return "<tr><td>" + esc(r.ma) + '</td><td class="ten">' + esc(r.ten) + "</td>" +
        '<td><span class="sw" style="background:' + r.mau + '"></span>' + esc(r.ng) + "</td>" +
        '<td class="num">' + n2(r.gt, 1) + '</td><td class="num">' + n2(r.tt, 2) + "%</td>" +
        '<td class="num">' + (r.tg === null ? "—" : n2(r.tg, 1, true) + "%") + "</td>" +
        '<td class="num">' + n2(r.rca, 2) + '</td><td class="num">' + n2(r.pci, 2) + "</td></tr>";
    }).join("");
    var tot = rows.reduce(function (s, r) { return s + r.gt; }, 0);
    document.getElementById("tbl-foot").textContent =
      f(rows.length) + " nhóm hàng · " + usd(tot * 1e3) + " · " + nuoc[S.iso].ten + " · " + S.y;
    el.querySelectorAll("th[data-sort]").forEach(function (th) {
      if (th.dataset.sort === sortKey) th.setAttribute("aria-sort", sortDir < 0 ? "descending" : "ascending");
      else th.removeAttribute("aria-sort");
    });
  }
  function csv(st) {
    var rows = tblRows(st), sep = ";";
    var head = ["Mã HS2", "Nhóm hàng", "Ngành", "Kim ngạch (triệu USD)", "Tỷ trọng (%)",
                "So năm trước (%)", "RCA", "PCI"];
    var q = function (s) { return '"' + String(s).replace(/"/g, '""') + '"'; };
    var lines = [head.map(q).join(sep)].concat(rows.map(function (r) {
      return [q(r.ma), q(r.ten), q(r.ng), n2(r.gt, 1), n2(r.tt, 2), r.tg === null ? "" : n2(r.tg, 1),
              n2(r.rca, 3), n2(r.pci, 3)].join(sep);
    }));
    var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "hs2_" + S.iso + "_" + S.y + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  /* ---------------------------------------------------------- dựng & nối */

  function setup() {
    var fn = document.getElementById("f-nuoc"), fy = document.getElementById("f-nam");
    var groups = {};
    W.co.forEach(function (iso) { var n = nuoc[iso]; (groups[n.kv] = groups[n.kv] || []).push(n); });
    fn.innerHTML = Object.keys(groups).sort(function (a, b) { return a.localeCompare(b, "vi"); })
      .map(function (k) {
        return '<optgroup label="' + esc(k) + '">' + groups[k].sort(function (a, b) {
          return a.ten.localeCompare(b.ten, "vi");
        }).map(function (n) { return '<option value="' + n.iso + '">' + esc(n.ten) + "</option>"; }).join("") +
        "</optgroup>";
      }).join("");
    setOptions(fy, W.nam.slice().reverse().map(function (y) { return [y, y]; }));

    card("c-kimngach", rKimNgach);
    card("c-khuvuc", rKhuVuc);
    card("c-nganh", rNganh);
    card("c-doitac", rDoiTac);
    card("c-mathang", rMatHang);
    card("c-rca", rRca);
    card("c-dva", rDva);
    card("c-sosanh", rSoSanh);
    var bang = card("c-bang", rBang);

    var years = W.nam.map(function (y) { return [y, y]; });
    var k = CARDS["c-kimngach"];
    k.st.tu = setOptions(k.el.querySelector('[data-key="tu"]'), years, W.nam[0]);
    k.st.den = setOptions(k.el.querySelector('[data-key="den"]'), years, W.nam[W.nam.length - 1]);
    var kv = CARDS["c-khuvuc"];
    kv.st.so = setOptions(kv.el.querySelector('[data-key="so"]'),
      [["0", "Không so sánh"]].concat(W.nam.slice().reverse().map(function (y) { return [y, y]; })), "0");
    ["c-nganh", "c-mathang", "c-rca", "c-bang"].forEach(function (id) {
      CARDS[id].st.nganh = setOptions(CARDS[id].el.querySelector('[data-key="nganh"]'), nganhOpts(), "all");
    });
    Object.keys(CARDS).forEach(function (id) {
      CARDS[id].el.querySelectorAll("select[data-key]").forEach(function (s) {
        if (CARDS[id].st[s.dataset.key] === undefined) CARDS[id].st[s.dataset.key] = s.value;
      });
    });

    bang.querySelectorAll("th[data-sort]").forEach(function (th) {
      th.tabIndex = 0;
      function act() {
        var key = th.dataset.sort;
        if (key === sortKey) sortDir = -sortDir;
        else { sortKey = key; sortDir = (key === "ma" || key === "ten" || key === "ng") ? 1 : -1; }
        CARDS["c-bang"].go();
      }
      th.addEventListener("click", act);
      th.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); act(); }
      });
    });
    bang.querySelector('[data-act="csv"]').addEventListener("click", function () { csv(CARDS["c-bang"].st); });

    var rt = null;                // vẽ lại thẻ giá trị ở lại khi đổi giữa khổ rộng và hẹp
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        var p = CARDS["c-dva"].el.querySelector(".plot");
        if ((p.clientWidth < 600) !== dvaNarrow) CARDS["c-dva"].go();
      }, 150);
    });

    fn.addEventListener("change", function () { change(fn.value, S.y); });
    fy.addEventListener("change", function () { change(S.iso, +fy.value); });
    document.getElementById("f-nam-lui").addEventListener("click", function () { change(S.iso, S.y - 1); });
    document.getElementById("f-nam-toi").addEventListener("click", function () { change(S.iso, S.y + 1); });
    window.addEventListener("hashchange", function () { var h = readHash(); change(h[0], h[1]); });
  }

  function readHash() {
    var m = /^#([A-Z]{3})-(\d{4})$/.exec(location.hash);
    var iso = m && W.co.indexOf(m[1]) >= 0 ? m[1] : S.iso;
    var y = m && W.nam.indexOf(+m[2]) >= 0 ? +m[2] : (S.y || W.nam[W.nam.length - 1]);
    return [iso, y];
  }

  var busy = 0;
  function change(iso, y) {
    if (W.nam.indexOf(y) < 0) return;
    var ticket = ++busy, status = document.getElementById("status");
    status.textContent = C[iso] ? "" : "Đang tải dữ liệu " + nuoc[iso].ten + "…";
    load(iso).then(function () {
      if (ticket !== busy) return;
      S.iso = iso; S.y = y;
      document.getElementById("f-nuoc").value = iso;
      document.getElementById("f-nam").value = String(y);
      document.getElementById("f-nam-lui").disabled = y <= W.nam[0];
      document.getElementById("f-nam-toi").disabled = y >= W.nam[W.nam.length - 1];
      var h = "#" + iso + "-" + y;
      if (location.hash !== h && history.replaceState) history.replaceState(null, "", h);
      var d = C[iso], dt = CARDS["c-doitac"];
      var kvs = [];
      d.dt.forEach(function (p) { var n = nuoc[p]; if (n && kvs.indexOf(n.kv) < 0) kvs.push(n.kv); });
      kvs.sort(function (a, b) { return a.localeCompare(b, "vi"); });
      dt.st.kv = setOptions(dt.el.querySelector('[data-key="kv"]'),
        [["all", "Tất cả"]].concat(kvs.map(function (k) { return [k, k]; })), dt.st.kv || "all");
      status.textContent = "";
      document.getElementById("noi-dung").setAttribute("aria-busy", "false");
      kpis();
      Object.keys(CARDS).forEach(function (id) { CARDS[id].go(); });
    }).catch(function (e) {
      status.textContent = "Không tải được dữ liệu " + iso + " (" + e.message + ").";
    });
  }

  function start() {
    fetch("data/world.json").then(function (r) { return r.json(); }).then(function (w) {
      W = w;
      prep();
      setup();
      var h = readHash();
      change(h[0], h[1]);
    }).catch(function (e) {
      document.getElementById("status").textContent = "Không tải được dữ liệu (" + e.message + ").";
    });
  }

  if (window.Plotly) start();
  else window.addEventListener("load", start);
})();
