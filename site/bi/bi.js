/* Dashboard BI — global-ecom.
 *
 * Dữ liệu: data/world.json (danh mục + chuỗi theo nước) và data/c/<ISO3>.json
 * (tải khi chọn nước), do src/build_bi.py dựng. Giá trị tính bằng nghìn USD.
 *
 * Ba trang dùng chung một khuôn (xem bi.css): ba thẻ KPI, ô bên trái, ô xu hướng,
 * ô phân rã, bảng. Thẻ KPI đang chọn là CHỈ SỐ của cả trang: bản đồ, biểu đồ và
 * bảng đều đổi theo nó. Ô bên trái là bộ lọc trực quan (châu lục và đối tác ·
 * ngành · nhóm nước); bấm vào đó hoặc vào một dòng bảng là lọc cả trang.
 *
 * Toàn bộ trạng thái nằm trong S và được ghi lên #hash, để gửi link là mở đúng
 * góc nhìn. Mọi con số trên trang đều tính lại từ dữ liệu, không viết sẵn.
 *
 * Màu: màu sắc chỉ dùng cho NGÀNH (style guide §3.1). Mọi thứ khác là mực và xám;
 * riêng thâm hụt / giảm dùng --down.
 */
(function () {
  "use strict";

  var INK = "#15171c", INK2 = "#393e48", MUTED = "#5a606c", GREY = "#b4b0a6",
      LIGHT = "#d9d6cd", SOFT = "#8b909a", GRID = "#ebe8e1", RULE = "#d9d6cd",
      DOWN = "#8c3b2e", LAND = "#f1efea";
  var FONT = '"Be Vietnam Pro", "Segoe UI", Arial, sans-serif';
  var ASEAN = ["BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM"];
  var CHAU = ["Châu Á", "Châu Âu", "Châu Mỹ", "Châu Phi", "Châu Đại Dương"];
  // Khung nhìn bản đồ cho từng châu lục: [kinh độ], [vĩ độ]
  var KHUNG = {
    "all": [[-180, 180], [-56, 80]],
    "Châu Á": [[25, 150], [-12, 58]], "Châu Âu": [[-25, 45], [34, 71]],
    "Châu Mỹ": [[-170, -30], [-56, 72]], "Châu Phi": [[-20, 55], [-36, 38]],
    "Châu Đại Dương": [[110, 180], [-48, 2]]
  };
  var CFG = { displaylogo: false, responsive: true, displayModeBar: false, scrollZoom: false };

  var W = null, C = {};
  var S = { pg: "tq", iso: "VNM", y: null, so: "auto",
            m: { tq: "x", mh: "v", ss: "hx" },
            ca: "all", dt: null, ng: "all", hs: null, nhom: "asean", q: "", sort: {} };
  var nuoc = {}, nganh = {}, hs2Ng = [], sumX = [], sumWp = [], hang = [], kvCa = {};

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
  function sgn(s, v) { return v > 0 ? "+" + s : s; }
  function pct(v, d) { return f(v, d === undefined ? 1 : d) + "%"; }
  function sum(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i] || 0; return s; }
  function ok(v) { return v !== null && v !== undefined && !isNaN(v); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function mix(hex, t) {          // pha màu với trắng, t ∈ [0,1)
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    function c(v) { return Math.round(v + (255 - v) * t); }
    return "rgb(" + c(r) + "," + c(g) + "," + c(b) + ")";
  }
  function ten(iso) { return nuoc[iso] ? nuoc[iso].ten : iso; }
  function $(id) { return document.getElementById(id); }

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
      font: { family: FONT, size: 11.5, color: INK2 }, separators: ",.",
      margin: { l: 50, r: 12, t: 8, b: 28 }, paper_bgcolor: "#fff", plot_bgcolor: "#fff",
      showlegend: false, hovermode: "closest", dragmode: false,
      hoverlabel: { font: { family: FONT, size: 12, color: "#fff" }, bgcolor: INK, bordercolor: INK },
      xaxis: { gridcolor: GRID, linecolor: RULE, zeroline: false, tickfont: { size: 10.5 }, fixedrange: true },
      yaxis: { gridcolor: GRID, linecolor: RULE, zeroline: false, tickfont: { size: 10.5 }, fixedrange: true }
    }, x || {});
  }
  function yearLine(y, dash) {
    return { type: "line", xref: "x", yref: "paper", x0: y, x1: y, y0: 0, y1: 1,
             line: { color: dash ? SOFT : MUTED, width: 1, dash: dash ? "dot" : "solid" } };
  }

  var CLICK = {}, sized = false;
  function draw(id, traces, layout, onClick) {
    var el = $(id);
    CLICK[id] = onClick || null;
    el.style.cursor = "";
    return Plotly.react(el, traces, L(layout), CFG).then(function () {
      if (!el._bound) {
        el._bound = true;
        el.on("plotly_click", function (ev) {
          if (CLICK[id] && ev && ev.points && ev.points[0]) CLICK[id](ev.points[0]);
        });
      }
    });
  }
  function resizeAll() {
    ["g-side", "g-trend", "g-break"].forEach(function (id) {
      var el = $(id);
      if (el && el.data) Plotly.Plots.resize(el);
    });
  }

  /* ---------------------------------------------------------- dữ liệu */

  function idx() { return W.nam.indexOf(S.y); }
  function soY() {
    var y = S.so === "auto" ? S.y - 1 : +S.so;
    return y !== S.y && W.nam.indexOf(y) >= 0 ? y : null;
  }
  function soI() { var y = soY(); return y === null ? -1 : W.nam.indexOf(y); }
  function cs(iso) { return W.cs[iso]; }
  function D() { return C[S.iso]; }

  function prep() {
    W.nuoc.forEach(function (n) { nuoc[n.iso] = n; kvCa[n.kv] = n.ca; });
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
    var xc = c.sp[i], xp = W.wp[i][j];
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

  function spark(arr, i, j, invert) {
    var v = arr.map(function (x) { return ok(x) ? x : NaN; });
    var good = v.filter(function (x) { return !isNaN(x); });
    if (good.length < 2) return "";
    var lo = Math.min.apply(null, good), hi = Math.max.apply(null, good), rg = (hi - lo) || 1;
    var n = v.length, pts = [], dots = "";
    v.forEach(function (x, k) {
      if (isNaN(x)) return;
      var t = (x - lo) / rg, px = 2 + k / (n - 1) * 116, py = 3 + (invert ? t : 1 - t) * 28;
      pts.push(px.toFixed(1) + "," + py.toFixed(1));
      if (k === j) dots += '<circle class="so" cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="2.6"/>';
      if (k === i) dots += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="2.8"/>';
    });
    return '<svg class="spark" viewBox="0 0 120 34" preserveAspectRatio="none" aria-hidden="true">' +
      '<polyline points="' + pts.join(" ") + '"/>' + dots + "</svg>";
  }

  // kind: "pct" (% thay đổi), "pp" (điểm %), "abs" (USD), "rank" (bậc, nhỏ là tốt), "n", "d2"
  function delta(now, prev, kind) {
    var y = soY();
    if (y === null || !ok(prev) || !ok(now)) return "&nbsp;";
    var d, txt;
    if (kind === "pct") { if (!prev) return "&nbsp;"; d = (now - prev) / Math.abs(prev) * 100; txt = pct(Math.abs(d)); }
    else if (kind === "pp") { d = now - prev; txt = f(Math.abs(d), 3) + " điểm %"; }
    else if (kind === "abs") { d = now - prev; txt = usd(Math.abs(d)); }
    else if (kind === "rank") { d = prev - now; txt = f(Math.abs(d)) + " bậc"; }
    else if (kind === "d2") { d = now - prev; txt = f(Math.abs(d), 2); }
    else if (kind === "pp1") { d = now - prev; txt = f(Math.abs(d), 1) + " điểm %"; }
    else { d = now - prev; txt = f(Math.abs(d)); }
    var vs = " so với " + y;
    if (Math.abs(d) < 1e-9) return "không đổi" + vs;
    return '<b class="' + (d > 0 ? "up" : "down") + '">' + (d > 0 ? "▲ " : "▼ ") + txt + "</b>" + vs;
  }

  function renderKpis(items) {
    var i = idx(), j = soI(), el = $("kpis"), cur = S.m[S.pg];
    el.dataset.n = items.length;
    el.innerHTML = items.map(function (it) {
      var v = it.now !== undefined ? it.now : it.s[i];
      var val = it.val(v);
      var dl = it.dnote ? esc(it.dnote) : delta(v, j >= 0 ? it.s[j] : null, it.kind);
      return '<div class="kpi" role="button" tabindex="0" data-m="' + it.id + '" aria-pressed="' +
        (it.id === cur) + '"><p class="kpi__label" title="' + esc(it.label) + '">' + esc(it.label) + "</p>" +
        '<span class="q" tabindex="0" data-tip="' + esc(it.tip) + '" aria-label="' + esc(it.tip) + '">?</span>' +
        '<p class="kpi__value">' + esc(val[0]) + '<span class="kpi__unit">' + esc(val[1]) + "</span></p>" +
        '<p class="kpi__delta">' + dl + "</p>" +
        spark(it.s, i, j, it.invert) + "</div>";
    }).join("");
  }

  /* ---------------------------------------------------------- bảng chung */

  // spec: { title, unit, cols:[{k,label,num,v(r),f(r),cls(r),bar}], rows, foot(rows)->r|null,
  //         def:{k,dir}, sel(r)->bool, row(r)->key|null, onRow(key), noun }
  var TB = null;
  function sortOf() { return S.sort[S.pg] || TB.def; }
  function renderTable(spec) {
    TB = spec;
    var so = sortOf(), col = null;
    spec.cols.forEach(function (c) { if (c.k === so.k) col = c; });
    if (!col) { so = spec.def; spec.cols.forEach(function (c) { if (c.k === so.k) col = c; }); }
    var q = S.q.trim().toLowerCase();
    var rows = spec.rows.filter(function (r) { return !q || r._s.toLowerCase().indexOf(q) >= 0; });
    rows.sort(function (a, b) {
      if (a._last !== b._last) return a._last ? 1 : -1;     // dòng gộp luôn nằm cuối
      var x = col.v(a), y = col.v(b);
      var nx = !ok(x) && typeof x !== "string", ny = !ok(y) && typeof y !== "string";
      if (nx || ny) return nx === ny ? 0 : nx ? 1 : -1;     // ô trống luôn nằm cuối
      return (typeof x === "string" ? x.localeCompare(y, "vi") : x - y) * so.dir;
    });
    var max = {};
    spec.cols.forEach(function (c) {
      if (!c.bar) return;
      max[c.k] = Math.max.apply(null, rows.map(function (r) { var v = c.v(r); return ok(v) ? Math.abs(v) : 0; }).concat([1e-12]));
    });
    $("t-table").textContent = spec.title;
    var t = $("tbl");
    t.querySelector("thead").innerHTML = "<tr>" + spec.cols.map(function (c) {
      var s = c.k === so.k ? ' aria-sort="' + (so.dir < 0 ? "descending" : "ascending") + '"' : "";
      return '<th scope="col" tabindex="0" data-k="' + c.k + '"' + (c.num ? ' class="num"' : "") + s + ">" + esc(c.label) + "</th>";
    }).join("") + "</tr>";
    function cell(c, r) {
      var v = c.f(r), cls = c.cls ? c.cls(r) : "";
      if (c.bar) {
        var w = ok(c.v(r)) ? Math.abs(c.v(r)) / max[c.k] : 0;
        return '<td class="num bar' + (cls ? " " + cls : "") + '"><i style="width:calc((100% - 16px)*' +
          w.toFixed(4) + ')"></i><span>' + esc(v) + "</span></td>";
      }
      return "<td" + ((c.num || cls) ? ' class="' + (c.num ? "num" : "") + (cls ? " " + cls : "") + '"' : "") + ">" + c.html(r, v) + "</td>";
    }
    spec.cols.forEach(function (c) { if (!c.html) c.html = function (r, v) { return esc(v); }; });
    t.querySelector("tbody").innerHTML = rows.map(function (r) {
      var key = spec.row ? spec.row(r) : null;
      return "<tr" + (key ? ' data-k="' + esc(key) + '"' : "") + (spec.sel && spec.sel(r) ? ' aria-selected="true"' : "") + ">" +
        spec.cols.map(function (c) { return cell(c, r); }).join("") + "</tr>";
    }).join("");
    var ft = spec.foot ? spec.foot(rows) : null;
    t.querySelector("tfoot").innerHTML = ft ? "<tr>" + spec.cols.map(function (c) {
      var v = ft[c.k];
      return "<td" + (c.num ? ' class="num"' : "") + ">" + esc(v === undefined ? "" : v) + "</td>";
    }).join("") + "</tr>" : "";
    $("tbl-foot").textContent = f(rows.length) + " / " + f(spec.rows.length) + " " + spec.noun;
    TB.shown = rows;
    var s = t.querySelector('tbody tr[aria-selected="true"]');
    if (s && s.scrollIntoView) s.scrollIntoView({ block: "nearest" });
  }
  function csv() {
    if (!TB) return;
    var sep = ";", q = function (s) { return '"' + String(s).replace(/"/g, '""') + '"'; };
    var lines = [TB.cols.map(function (c) { return q(c.label); }).join(sep)].concat(TB.shown.map(function (r) {
      return TB.cols.map(function (c) { return q(c.f(r)); }).join(sep);
    }));
    var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = S.pg + "_" + S.iso + "_" + S.y + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  function seg(items, cur, on) {
    var el = $("seg-side");
    el.innerHTML = items.map(function (it) {
      return '<button type="button" data-v="' + esc(it[0]) + '" aria-pressed="' + (String(it[0]) === String(cur)) + '">' +
        esc(it[1]) + "</button>";
    }).join("");
    el.onclick = function (ev) { var b = ev.target.closest("button"); if (b) on(b.dataset.v); };
  }
  function chip(text, clear) {
    var el = $("chip");
    if (!text) { el.hidden = true; el.onclick = null; return; }
    el.hidden = false;
    el.textContent = text + "  ✕";
    el.setAttribute("aria-label", "Bỏ lọc " + text);
    el.onclick = clear;
  }

  /* ========================================================== TRANG 1: TỔNG QUAN */

  var TQ = {
    title: "Tổng quan",
    help: "Bấm một thẻ chỉ số để đổi chỉ số cho bản đồ, biểu đồ và bảng. Bấm một châu lục, một nước trên bản đồ hoặc một dòng trong bảng để xem riêng thương mại với đối tác đó.",
    // chuỗi theo năm trong phạm vi đang lọc (cả thế giới · một châu lục · một đối tác)
    series: function (m) {
      var d = D(), c = cs(S.iso), x, mm;
      if (S.dt) {
        var k = d.dt.indexOf(S.dt);
        x = d.x[k]; mm = d.m[k];
      } else if (S.ca !== "all") {
        x = W.nam.map(function (_, t) { var s = 0; for (var r in d.kv.x) if (kvCa[r] === S.ca) s += d.kv.x[r][t]; return s; });
        mm = W.nam.map(function (_, t) { var s = 0; for (var r in d.kv.m) if (kvCa[r] === S.ca) s += d.kv.m[r][t]; return s; });
      } else { x = c.x; mm = c.m; }
      if (m === "x") return x;
      if (m === "m") return mm;
      return x.map(function (v, t) { return v - mm[t]; });
    },
    scope: function () { return S.dt ? ten(S.dt) : S.ca !== "all" ? S.ca : null; },
    kpis: function () {
      var sc = TQ.scope(), n = ten(S.iso);
      return [
        { id: "x", label: "Xuất khẩu" + (sc ? " sang " + sc : ""), kind: "pct", s: TQ.series("x"),
          val: function (v) { return usdP(v); },
          tip: "Giá trị hàng hóa " + n + " bán ra nước ngoài trong năm, USD danh nghĩa." },
        { id: "m", label: "Nhập khẩu" + (sc ? " từ " + sc : ""), kind: "pct", s: TQ.series("m"),
          val: function (v) { return usdP(v); },
          tip: "Giá trị hàng hóa " + n + " mua từ nước ngoài trong năm." },
        { id: "cc", label: "Cán cân" + (sc ? " với " + sc : " thương mại"), kind: "abs", s: TQ.series("cc"),
          val: function (v) { var u = usdP(v); u[0] = sgn(u[0], v); return u; },
          tip: "Xuất khẩu trừ nhập khẩu. Dương là thặng dư (bán nhiều hơn mua), âm là thâm hụt." }
      ];
    },
    rows: function (i) {
      var d = D();
      return d.dt.map(function (iso, k) {
        return { iso: iso, ten: ten(iso), kv: nuoc[iso] ? nuoc[iso].kv : "", ca: nuoc[iso] ? nuoc[iso].ca : "",
                 x: d.x[k][i], m: d.m[k][i], cc: d.x[k][i] - d.m[k][i] };
      });
    },
    side: function () {
      var m = S.m.tq, i = idx(), d = D();
      $("t-side").textContent = { x: "Thị trường xuất khẩu", m: "Nguồn nhập khẩu", cc: "Cán cân theo đối tác" }[m] + " · " + S.y;
      seg([["all", "Toàn cầu"]].concat(CHAU.map(function (c) { return [c, c.replace("Châu ", "")]; })), S.ca, function (v) {
        S.ca = v;
        if (S.dt && nuoc[S.dt] && v !== "all" && nuoc[S.dt].ca !== v) S.dt = null;
        render();
      });
      var rows = TQ.rows(i).filter(function (r) { return m === "cc" ? r.x || r.m : r[m] > 0; });
      var inn = rows.filter(function (r) { return S.ca === "all" || r.ca === S.ca; });
      var out = rows.filter(function (r) { return !(S.ca === "all" || r.ca === S.ca); });
      var tot = (m === "m" ? cs(S.iso).m : cs(S.iso).x)[i];
      var tr = [], cd = function (r) {
        var p = tot ? " (" + pct((m === "m" ? r.m : r.x) / tot * 100) + ")" : "";
        return m === "cc" ? [r.ten, "Cán cân: " + sgn(usd(r.cc), r.cc), "Xuất " + usd(r.x) + " · nhập " + usd(r.m)]
                          : [r.ten, (m === "x" ? "Xuất khẩu: " : "Nhập khẩu: ") + usd(r[m]) + p, ""];
      };
      var lw = function (arr) { return arr.map(function (r) { return r.iso === S.dt ? 2.4 : 0.5; }); };
      var lc = function (arr) { return arr.map(function (r) { return r.iso === S.dt ? INK : "#fff"; }); };
      var tick, cbar;
      if (m === "cc") {
        var lim = Math.max.apply(null, inn.map(function (r) { return Math.abs(r.cc) / 1e6; }).concat([0.001]));
        tr.push({ type: "choropleth", locationmode: "ISO-3", locations: inn.map(function (r) { return r.iso; }),
          z: inn.map(function (r) { return r.cc / 1e6; }), zmin: -lim, zmax: lim, zmid: 0,
          colorscale: [[0, DOWN], [0.5, "#f4f2ec"], [1, INK]],
          marker: { line: { color: lc(inn), width: lw(inn) } }, customdata: inn.map(cd),
          hovertemplate: "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>%{customdata[2]}<extra></extra>",
          colorbar: { thickness: 8, len: 0.5, x: 1, y: 0.5, outlinewidth: 0, ticksuffix: " tỷ", tickfont: { size: 10 } } });
      } else {
        var vals = inn.map(function (r) { return r[m]; }).filter(function (v) { return v > 0; });
        var lo = Math.floor(Math.log10(Math.max(Math.min.apply(null, vals.concat([1e9])), 1)));
        var hi = Math.ceil(Math.log10(Math.max.apply(null, vals.concat([10]))));
        tick = []; for (var e = lo; e <= hi; e++) tick.push(e);
        cbar = { thickness: 8, len: 0.5, x: 1, y: 0.5, outlinewidth: 0, tickfont: { size: 10 },
                 tickmode: "array", tickvals: tick, ticktext: tick.map(function (e) {
                   var u = Math.pow(10, e); // nghìn USD
                   return u >= 1e9 ? f(u / 1e9) + " nghìn tỷ" : u >= 1e6 ? f(u / 1e6) + " tỷ" : u >= 1e3 ? f(u / 1e3) + " triệu" : f(u) + " nghìn";
                 }) };
        tr.push({ type: "choropleth", locationmode: "ISO-3", locations: inn.map(function (r) { return r.iso; }),
          z: inn.map(function (r) { return Math.log10(Math.max(r[m], 1)); }), zmin: lo, zmax: hi,
          colorscale: [[0, "#e4e2dc"], [0.5, SOFT], [1, INK]],
          marker: { line: { color: lc(inn), width: lw(inn) } }, customdata: inn.map(cd),
          hovertemplate: "<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>", colorbar: cbar });
      }
      if (out.length) {
        tr.push({ type: "choropleth", locationmode: "ISO-3", locations: out.map(function (r) { return r.iso; }),
          z: out.map(function () { return 0; }), colorscale: [[0, "#ebe9e3"], [1, "#ebe9e3"]], showscale: false,
          marker: { line: { color: "#fff", width: 0.5 } }, customdata: out.map(cd),
          hovertemplate: "<b>%{customdata[0]}</b> · ngoài châu lục đang lọc<extra></extra>" });
      }
      tr.push({ type: "choropleth", locationmode: "ISO-3", locations: [S.iso], z: [0], showscale: false,
        colorscale: [[0, "#fff"], [1, "#fff"]], marker: { line: { color: INK, width: 1.6 } },
        hovertemplate: "<b>" + esc(ten(S.iso)) + "</b> · nước đang xem<extra></extra>" });
      var kh = KHUNG[S.ca] || KHUNG.all;
      draw("g-side", tr, {
        margin: { l: 0, r: 0, t: 0, b: 0 },
        geo: { projection: { type: "natural earth" }, showframe: false, showcoastlines: false,
               showland: true, landcolor: LAND, showcountries: true, countrycolor: "#fff", countrywidth: 0.5,
               showocean: false, showlakes: false, bgcolor: "rgba(0,0,0,0)", resolution: 50,
               lonaxis: { range: kh[0] }, lataxis: { range: kh[1] } }
      }, function (pt) {
        var iso = pt.location;
        if (!iso || iso === S.iso || d.dt.indexOf(iso) < 0) return;
        S.dt = S.dt === iso ? null : iso;
        render();
      });
      var all = cs(S.iso)[m === "m" ? "m" : "x"][i];
      var phu = all ? sum(TQ.rows(i).map(function (r) { return m === "m" ? r.m : r.x; })) / all * 100 : 0;
      $("n-side").textContent = "Tô " + f(d.dt.length) + " đối tác lớn nhất, chiếm " + pct(phu) +
        (m === "m" ? " nhập khẩu" : " xuất khẩu") + "; phần còn lại gộp vào “Các nước khác”. Nền xám nhạt: không thuộc nhóm này. Viền đậm: nước đang xem. Bấm một nước để lọc cả trang.";
    },
    trend: function () {
      var m = S.m.tq, s = TQ.series(m), i = idx(), j = soI(), sc = TQ.scope();
      $("t-trend").textContent = { x: "Xuất khẩu", m: "Nhập khẩu", cc: "Cán cân thương mại" }[m] +
        (sc ? (m === "x" ? " sang " : m === "m" ? " từ " : " với ") + sc : "") + " theo năm (tỷ USD)";
      chip(S.dt ? ten(S.dt) : S.ca !== "all" ? S.ca : null, function () { S.dt = null; S.ca = "all"; render(); });
      var col = s.map(function (v, k) {
        var base = m === "cc" && v < 0 ? DOWN : INK;
        if (k === i) return base;
        if (k === j) return mix(base, 0.45);
        return mix(base, 0.78);
      });
      draw("g-trend", [{
        type: "bar", x: W.nam, y: s.map(function (v) { return v / 1e6; }), marker: { color: col },
        customdata: s.map(function (v) { return m === "cc" ? sgn(usd(v), v) : usd(v); }),
        hovertemplate: "%{x}: %{customdata}<extra></extra>"
      }], {
        bargap: 0.18, margin: { l: 46, r: 30, t: 18 },
        xaxis: { dtick: 5, range: [W.nam[0] - 0.6, W.nam[W.nam.length - 1] + 0.6] },
        yaxis: { zeroline: m === "cc", zerolinecolor: RULE },
        annotations: annYears(s, i, j, m === "cc")
      }, function (pt) { setYear(+pt.x); });
    },
    brk: function () {
      var m = S.m.tq, d = D(), i = idx(), j = soI();
      var dir = m === "m" ? "m" : "x";
      $("t-break").textContent = (m === "cc" ? "Cán cân theo khu vực (tỷ USD)" :
        (m === "x" ? "Xuất khẩu" : "Nhập khẩu") + " theo khu vực (% tổng)") + (S.ca !== "all" ? " · " + S.ca : "");
      function g(dd, r, t) { return (dd[r] || [])[t] || 0; }
      function val(r, t) { return m === "cc" ? (g(d.kv.x, r, t) - g(d.kv.m, r, t)) / 1e6 : g(d.kv[dir], r, t); }
      var regs = Object.keys(m === "cc" ? merge(d.kv.x, d.kv.m) : d.kv[dir])
        .filter(function (r) { return S.ca === "all" || kvCa[r] === S.ca; });
      function tot(t) { return sum(regs.map(function (r) { return g(d.kv[dir], r, t); })); }
      function v(r, t) { if (t < 0) return null; if (m === "cc") return val(r, t); var T = tot(t); return T ? val(r, t) / T * 100 : 0; }
      regs.sort(function (a, b) { return Math.abs(v(b, i)) - Math.abs(v(a, i)); });
      var top = regs.slice(0, 8), rest = regs.slice(8);
      function rv(t) {
        if (t < 0) return null;
        var o = top.map(function (r) { return v(r, t); });
        if (rest.length) o.push(sum(rest.map(function (r) { return v(r, t); })));
        return o;
      }
      var lab = top.concat(rest.length ? ["Khu vực khác"] : []);
      var cur = rv(i), prev = rv(j), hiRg = S.dt && nuoc[S.dt] ? nuoc[S.dt].kv : null;
      var fmt = function (x) { return m === "cc" ? sgn(f(x, 1), x) : pct(x); };
      var tr = [];
      if (prev) tr.push({ type: "bar", orientation: "h", y: lab, x: prev, name: String(soY()),
        marker: { color: lab.map(function (_, k) { return m === "cc" && prev[k] < 0 ? mix(DOWN, 0.7) : LIGHT; }) },
        hovertemplate: "%{y}: %{x:,.1f}" + (m === "cc" ? " tỷ USD" : "%") + "<extra>" + soY() + "</extra>" });
      tr.push({ type: "bar", orientation: "h", y: lab, x: cur, name: String(S.y),
        marker: { color: lab.map(function (r, k) { var c = m === "cc" && cur[k] < 0 ? DOWN : INK; return hiRg && r !== hiRg ? mix(c, 0.55) : c; }) },
        text: cur.map(fmt), textposition: "outside", cliponaxis: false, textfont: { size: 10.5, color: INK2 },
        hovertemplate: "%{y}: %{x:,.1f}" + (m === "cc" ? " tỷ USD" : "%") + "<extra>" + S.y + "</extra>" });
      draw("g-break", tr, {
        barmode: "group", bargap: 0.28, bargroupgap: 0.05, showlegend: !!prev,
        legend: { orientation: "h", x: 1, xanchor: "right", y: 1.06, font: { size: 10.5 }, traceorder: "reversed" },
        margin: { l: 8, r: 46, t: prev ? 20 : 6, b: 22 },
        yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 10.5 } },
        xaxis: { ticksuffix: m === "cc" ? "" : "%", zeroline: m === "cc", zerolinecolor: RULE }
      });
    },
    table: function () {
      var m = S.m.tq, i = idx(), j = soI(), d = D(), y = soY();
      var key = m === "m" ? "m" : "x";
      var cur = TQ.rows(i), prev = j >= 0 ? TQ.rows(j) : null;
      var tot = { x: cs(S.iso).x[i], m: cs(S.iso).m[i] };
      cur.forEach(function (r, k) {
        r.tt = tot[key] ? r[key] / tot[key] * 100 : null;
        r.p = prev ? prev[k][m] : null;
        r._s = r.ten + " " + r.kv + " " + r.iso;
      });
      var rows = cur.filter(function (r) { return (r.x || r.m) && (S.ca === "all" || r.ca === S.ca); });
      if (S.ca === "all") {
        var o = { iso: "", ten: "Các nước khác", kv: "", x: d.xk[i], m: d.mk[i], _s: "Các nước khác", _last: true };
        o.cc = o.x - o.m; o.tt = tot[key] ? o[key] / tot[key] * 100 : null;
        o.p = j >= 0 ? { x: d.xk[j], m: d.mk[j], cc: d.xk[j] - d.mk[j] }[m] : null;
        rows.push(o);
      }
      function ch(r) {
        if (!ok(r.p) || r.p === null) return null;
        return m === "cc" ? r[m] - r.p : (r.p ? (r[m] - r.p) / Math.abs(r.p) * 100 : null);
      }
      var mil = function (v) { return f(v / 1e3, 1); };
      var cols = [
        { k: "ten", label: "Đối tác", v: function (r) { return r.ten; }, f: function (r) { return r.ten; } },
        { k: "kv", label: "Khu vực", v: function (r) { return r.kv; }, f: function (r) { return r.kv; } },
        { k: "x", label: "Xuất khẩu (triệu USD)", num: true, bar: m === "x", v: function (r) { return r.x; }, f: function (r) { return mil(r.x); } },
        { k: "m", label: "Nhập khẩu (triệu USD)", num: true, bar: m === "m", v: function (r) { return r.m; }, f: function (r) { return mil(r.m); } },
        { k: "cc", label: "Cán cân (triệu USD)", num: true, bar: m === "cc", v: function (r) { return r.cc; },
          f: function (r) { return sgn(mil(r.cc), r.cc); }, cls: function (r) { return r.cc < 0 ? "down" : ""; } },
        { k: "tt", label: "Tỷ trọng " + (key === "m" ? "nhập" : "xuất"), num: true, v: function (r) { return r.tt; },
          f: function (r) { return ok(r.tt) ? pct(r.tt, 2) : "—"; } }
      ];
      if (y !== null) cols.push({ k: "ch", label: "So với " + y + (m === "cc" ? " (triệu USD)" : ""), num: true, v: ch,
        f: function (r) { var c = ch(r); return c === null ? "—" : m === "cc" ? sgn(mil(c), c) : sgn(pct(c), c); },
        cls: function (r) { var c = ch(r); return c !== null && c < 0 ? "down" : ""; } });
      renderTable({
        title: "Đối tác của " + ten(S.iso) + " · " + S.y, rows: rows, cols: cols, noun: "dòng",
        def: { k: m, dir: -1 },
        foot: function (rs) {
          var sx = sum(rs.map(function (r) { return r.x; })), sm = sum(rs.map(function (r) { return r.m; }));
          return { ten: "Tổng · " + f(rs.length) + " dòng", x: mil(sx), m: mil(sm), cc: sgn(mil(sx - sm), sx - sm),
                   tt: tot[key] ? pct((key === "m" ? sm : sx) / tot[key] * 100, 2) : "" };
        },
        sel: function (r) { return r.iso && r.iso === S.dt; },
        row: function (r) { return r.iso || null; },
        onRow: function (k) { S.dt = S.dt === k ? null : k; render(); }
      });
    }
  };

  // Nhãn năm đang xem và năm so sánh trên cột
  function annYears(s, i, j, signed) {
    var a = [];
    var near = i >= 0 && j >= 0 && Math.abs(i - j) <= 2;
    [[i, INK, true], [j, MUTED, false]].forEach(function (p) {
      if (p[0] < 0 || !ok(s[p[0]])) return;
      var v = s[p[0]], other = p[2] ? j : i;
      var anchor = !near ? "center" : (p[0] > other ? "left" : "right");
      a.push({ x: W.nam[p[0]], y: v / 1e6, yanchor: v < 0 ? "top" : "bottom", xanchor: anchor, showarrow: false,
               text: (p[2] ? "<b>" : "") + (signed ? sgn(f(v / 1e6, 1), v) : f(v / 1e6, 1)) + (p[2] ? "</b>" : ""),
               font: { size: 10.5, color: p[1] }, yshift: v < 0 ? -2 : 2 });
    });
    return a;
  }

  /* ========================================================== TRANG 2: MẶT HÀNG */

  var MH = {
    title: "Mặt hàng",
    help: "Bấm một thẻ chỉ số để đổi chỉ số cho cả trang. Bấm một ngành ở ô bên trái để lọc, bấm một dòng trong bảng để đánh dấu nhóm hàng đó trên biểu đồ RCA × PCI.",
    js: function (ng) {
      var o = [];
      for (var j = 0; j < hs2Ng.length; j++) if (ng === "all" || hs2Ng[j] === +ng) o.push(j);
      return o;
    },
    val: function (m, ng, t) {
      var d = D(), js = MH.js(ng);
      if (t < 0 || !d.sp[t]) return null;
      if (m === "v") return sum(js.map(function (j) { return d.p[t][j]; }));
      if (m === "rca") { var n = 0; js.forEach(function (j) { var r = rca(d, t, j); if (r !== null && r >= 1) n++; }); return n; }
      var a = 0, b = 0;
      js.forEach(function (j) { var p = W.pci[t][j]; if (p !== null && d.p[t][j] > 0) { a += p * d.p[t][j]; b += d.p[t][j]; } });
      return b ? a / b : null;
    },
    series: function (m, ng) { return W.nam.map(function (_, t) { return MH.val(m, ng, t); }); },
    // Phần giá trị ở lại trong nước (OECD TiVA): chỉ có cho Việt Nam, 1995–2022 (B31).
    // Năm sau năm TiVA cuối thì lấy năm cuối và ghi rõ trên thẻ.
    dvaOn: function () { return !!(W.dva && S.iso === "VNM"); },
    dvaK: function (y) {
      var Dv = W.dva, k = Dv.nam.indexOf(y);
      return k >= 0 ? k : y > Dv.nam[Dv.nam.length - 1] ? Dv.nam.length - 1 : -1;
    },
    dvaVal: function (ng, k) {
      var Dv = W.dva;
      if (k < 0) return null;
      if (ng === "all") return Dv.rb[k];
      var j = Dv.ng.indexOf(+ng);
      return j >= 0 ? Dv.v[k][j] : null;
    },
    kpis: function () {
      var g = S.ng !== "all" ? nganh[S.ng].ten : null, nj = MH.js(S.ng).length;
      var out = MH.kpis3(g, nj);
      if (MH.dvaOn()) {
        var Dv = W.dva, cuoi = Dv.nam[Dv.nam.length - 1];
        out.push({ id: "dva", label: "Giá trị ở lại trong nước" + (g ? " · " + g : ""), kind: "pp1",
          s: W.nam.map(function (y) { return Dv.nam.indexOf(y) >= 0 ? MH.dvaVal(S.ng, Dv.nam.indexOf(y)) : null; }),
          now: MH.dvaVal(S.ng, MH.dvaK(S.y)),
          // Sau năm TiVA cuối: để trống dòng so sánh (so số năm cuối với chính nó vô nghĩa)
          dnote: S.y > cuoi ? " " : null,
          val: function (v) { return [ok(v) ? f(v, 1) : "—", "% (TiVA)"]; },
          tip: "Phần giá trị xuất khẩu thực sự làm ra trong nước (OECD TiVA), không tính phần linh kiện, nguyên liệu nhập về. Chỉ có cho Việt Nam, 1995–" + cuoi + "; ngành Atlas được ghép sang ngành TiVA qua nhóm HS2." });
      }
      return out;
    },
    kpis3: function (g, nj) {
      return [
        { id: "v", label: "Kim ngạch xuất khẩu" + (g ? " · " + g : ""), kind: "pct", s: MH.series("v", S.ng),
          val: function (v) { return ok(v) ? usdP(v) : ["—", ""]; },
          tip: "Tổng xuất khẩu cộng theo 97 nhóm hàng HS2. Có thể lệch rất nhỏ so với tổng cộng theo đối tác." },
        { id: "rca", label: "Nhóm hàng có RCA ≥ 1", kind: "n", s: MH.series("rca", S.ng),
          val: function (v) { return [ok(v) ? f(v) : "—", "/ " + nj + " nhóm"]; },
          tip: "RCA (lợi thế so sánh hiện hữu) = tỷ trọng nhóm hàng trong xuất khẩu của nước này chia cho tỷ trọng của nó trong thương mại thế giới. RCA ≥ 1 nghĩa là nước có lợi thế ở nhóm đó." },
        { id: "pci", label: "Độ phức tạp của rổ hàng", kind: "d2", s: MH.series("pci", S.ng),
          val: function (v) { return [ok(v) ? f(v, 2) : "—", "PCI"]; },
          tip: "PCI (Atlas) đo độ khó của một sản phẩm: dương là khó hơn mức trung bình. Đây là PCI trung bình của các nhóm hàng, trọng số theo kim ngạch: càng cao, nước càng bán nhiều hàng phức tạp." }
      ];
    },
    // Ô trái khi chỉ số là TiVA: phần ở lại theo ngành, xếp theo PCI giảm dần (B30),
    // vạch mảnh là khoảng giữa hai cách ghép HS2 sang ISIC, vạch đứt là bình quân cả rổ.
    sideDva: function () {
      var Dv = W.dva, k = MH.dvaK(S.y), cuoi = Dv.nam[Dv.nam.length - 1];
      $("t-side").textContent = "Giá trị ở lại theo ngành · TiVA " + Dv.nam[Math.max(k, 0)];
      seg([], null, null);
      var rows = [];
      Dv.ng.forEach(function (id, j) {
        if (k < 0 || Dv.v[k][j] === null) return;
        rows.push({ id: id, ten: nganh[id].ten, v: Dv.v[k][j], lo: Dv.lo[k][j], hi: Dv.hi[k][j], pci: Dv.pci[k][j], tt: Dv.tt[k][j] });
      });
      rows.sort(function (a, b) { return (b.pci === null ? -9 : b.pci) - (a.pci === null ? -9 : a.pci); });
      var on = function (r) { return S.ng === "all" || +S.ng === r.id; };
      var rb = k >= 0 ? Dv.rb[k] : null;
      draw("g-side", [{
        type: "bar", orientation: "h", x: rows.map(function (r) { return r.v; }), y: rows.map(function (r) { return r.ten; }),
        marker: { color: rows.map(function (r) { return on(r) ? nganh[r.id].mau : mix(nganh[r.id].mau, 0.7); }), line: { color: "#fff", width: 1 } },
        error_x: { type: "data", symmetric: false, color: INK2, thickness: 1, width: 3,
                   array: rows.map(function (r) { return Math.max(0, r.hi - r.v); }),
                   arrayminus: rows.map(function (r) { return Math.max(0, r.v - r.lo); }) },
        text: rows.map(function (r) { return pct(r.v); }), textposition: "outside", cliponaxis: false,
        textfont: { size: 10.5, color: INK2 },
        customdata: rows.map(function (r) {
          return [r.ten, pct(r.v), f(r.lo, 1), pct(r.hi), ok(r.pci) ? sgn(f(r.pci, 2), r.pci) : "—", pct(r.tt), r.id];
        }),
        hovertemplate: "<b>%{customdata[0]}</b><br>Giữ lại trong nước: %{customdata[1]}" +
          "<br>Khoảng theo hai cách ghép: %{customdata[2]}–%{customdata[3]}" +
          "<br>PCI %{customdata[4]} · %{customdata[5]} xuất khẩu ghép được<extra></extra>"
      }], {
        margin: { l: 8, r: 40, t: 18, b: 24 }, bargap: 0.3,
        xaxis: { range: [0, 100], ticksuffix: "%", tickvals: [0, 25, 50, 75, 100] },
        yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 10.5 } },
        shapes: rb === null ? [] : [{ type: "line", xref: "x", yref: "paper", x0: rb, x1: rb, y0: 0, y1: 1, line: { color: MUTED, width: 1, dash: "dash" } }],
        annotations: rb === null ? [] : [{ xref: "x", x: rb, yref: "paper", y: 1, yanchor: "bottom", showarrow: false,
                                           text: "Bình quân cả rổ " + pct(rb), font: { size: 10.5, color: MUTED } }]
      }, function (pt) {
        var id = pt.customdata && pt.customdata[6];
        if (id === undefined) return;
        S.ng = String(S.ng) === String(id) ? "all" : String(id);
        S.hs = null;
        render();
      });
      $("n-side").textContent = "Luôn là Việt Nam. " + (S.y > cuoi ? "TiVA dừng ở " + cuoi + ", đang hiện số năm đó. " : "") +
        "Xếp theo PCI giảm dần. Chưa tính ngành Khác (" + pct(k >= 0 ? Dv.khac[k] : 0) +
        " xuất khẩu: HS97, HS99 không ghép được). Vạch mảnh: khoảng giữa hai cách ghép HS2 sang ISIC. Nguồn: OECD TiVA 2025.";
    },
    side: function () {
      var m = S.m.mh, i = idx(), j = soI();
      if (m === "dva") return MH.sideDva();
      $("t-side").textContent = { v: "Tỷ trọng theo ngành", rca: "Số nhóm RCA ≥ 1 theo ngành", pci: "PCI theo ngành" }[m] + " · " + S.y;
      seg([], null, null);
      var tot = MH.val("v", "all", i), totJ = j >= 0 ? MH.val("v", "all", j) : null;
      var gs = W.nganh.slice();
      function v(g, t, T) {
        var x = MH.val(m, g.id, t);
        return m === "v" ? (T && ok(x) ? x / T * 100 : null) : x;
      }
      var cur = gs.map(function (g) { return v(g, i, tot); });
      var order = gs.map(function (_, k) { return k; }).sort(function (a, b) { return (cur[b] || -1e9) - (cur[a] || -1e9); });
      gs = order.map(function (k) { return gs[k]; });
      cur = order.map(function (k) { return cur[k]; });
      var prev = j >= 0 ? gs.map(function (g) { return v(g, j, totJ); }) : null;
      var fmt = function (x) { return !ok(x) ? "" : m === "v" ? pct(x) : m === "rca" ? f(x) : f(x, 2); };
      var on = function (g) { return S.ng === "all" || +S.ng === g.id; };
      var tr = [];
      if (prev) tr.push({ type: "bar", orientation: "h", y: gs.map(function (g) { return g.ten; }), x: prev, name: String(soY()),
        marker: { color: gs.map(function (g) { return mix(g.mau, on(g) ? 0.7 : 0.88); }) },
        customdata: gs.map(function (g) { return g.id; }), text: prev.map(fmt), textposition: "none",
        hovertemplate: "%{y}: %{text}<extra>" + soY() + "</extra>" });
      tr.push({ type: "bar", orientation: "h", y: gs.map(function (g) { return g.ten; }), x: cur, name: String(S.y),
        marker: { color: gs.map(function (g) { return on(g) ? g.mau : mix(g.mau, 0.7); }),
                  line: { color: "rgba(0,0,0,0.15)", width: 0.5 } },
        customdata: gs.map(function (g) { return g.id; }),
        text: cur.map(fmt), textposition: "outside", cliponaxis: false, textfont: { size: 10.5, color: INK2 },
        hovertemplate: "%{y}: %{text}<extra>" + S.y + "</extra>" });
      draw("g-side", tr, {
        margin: { l: 8, r: 44, t: 4, b: 24 }, bargap: 0.22, bargroupgap: 0.04, barmode: "group",
        yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 10.5 } },
        xaxis: { ticksuffix: m === "v" ? "%" : "", zeroline: m === "pci", zerolinecolor: RULE }
      }, function (pt) {
        var id = pt.customdata;
        if (id === undefined) return;
        S.ng = String(S.ng) === String(id) ? "all" : String(id);
        S.hs = null;
        render();
      });
      $("n-side").textContent = "Màu là ngành hàng." + (prev ? " Thanh nhạt phía trên: năm " + soY() + "." : "") + " Bấm một ngành để lọc cả trang, bấm lần nữa để bỏ lọc.";
    },
    trend: function () {
      var m = S.m.mh, d = D(), i = idx(), j = soI(), g = S.ng !== "all" ? nganh[S.ng] : null;
      chip(g ? g.ten : null, function () { S.ng = "all"; S.hs = null; render(); });
      var tr = [], shapes = [yearLine(S.y)];
      if (j >= 0) shapes.push(yearLine(soY(), true));
      if (m === "v") {
        $("t-trend").textContent = "Cơ cấu xuất khẩu " + (g ? "trong ngành " + g.ten.toLowerCase() : "theo ngành") + " (tỷ USD)";
        if (!g) {
          W.nganh.forEach(function (gg) {
            tr.push({ type: "scatter", mode: "lines", stackgroup: "a", name: gg.ten, x: W.nam,
              y: W.nam.map(function (_, t) { return (MH.val("v", gg.id, t) || 0) / 1e6; }),
              line: { width: 0.5, color: "#fff" }, fillcolor: gg.mau,
              hovertemplate: "%{y:,.2f} tỷ USD<extra>" + esc(gg.ten) + "</extra>" });
          });
        } else {
          var js = MH.js(g.id);
          js.sort(function (p, q) { return d.p[i][q] - d.p[i][p]; });
          var top = js.slice(0, 6), rest = js.slice(6);
          top.forEach(function (jj, k) {
            var h = W.hs2[jj];
            tr.push({ type: "scatter", mode: "lines", stackgroup: "a", name: h.ma + " " + h.ten, x: W.nam,
              y: W.nam.map(function (_, t) { return d.p[t][jj] / 1e6; }),
              line: { width: 0.5, color: "#fff" }, fillcolor: mix(g.mau, k * 0.12),
              hovertemplate: "%{y:,.2f} tỷ USD<extra>" + esc(h.ma + " " + h.ten) + "</extra>" });
          });
          if (rest.length) tr.push({ type: "scatter", mode: "lines", stackgroup: "a", name: "Nhóm khác", x: W.nam,
            y: W.nam.map(function (_, t) { var s = 0; rest.forEach(function (jj) { s += d.p[t][jj]; }); return s / 1e6; }),
            line: { width: 0.5, color: "#fff" }, fillcolor: "#dcd9d0", hovertemplate: "%{y:,.2f} tỷ USD<extra>Nhóm khác</extra>" });
        }
      } else {
        var s = m === "dva"
          ? W.nam.map(function (y) { var k = W.dva.nam.indexOf(y); return k >= 0 ? MH.dvaVal(S.ng, k) : null; })
          : MH.series(m, S.ng);
        $("t-trend").textContent = (m === "rca" ? "Số nhóm hàng có RCA ≥ 1" : m === "pci" ? "PCI bình quân của rổ hàng xuất khẩu"
          : "Phần giá trị ở lại trong nước (%, TiVA)") + (g ? " · " + g.ten : "") + " theo năm";
        tr.push({ type: "scatter", mode: "lines+markers", x: W.nam, y: s, line: { color: g ? g.mau : INK, width: 2 },
          marker: { size: W.nam.map(function (_, k) { return k === i ? 8 : k === j ? 7 : 0; }),
                    color: W.nam.map(function (_, k) { return k === j ? "#fff" : INK; }), line: { color: INK, width: 1.4 } },
          hovertemplate: "%{x}: %{y:,." + (m === "rca" ? "0" : m === "dva" ? "1" : "2") + "f}" + (m === "dva" ? "%" : "") + "<extra></extra>" });
      }
      draw("g-trend", tr, {
        hovermode: m === "v" ? "x unified" : "closest", margin: { l: 44, t: 8 },
        xaxis: { dtick: 5, range: [W.nam[0], W.nam[W.nam.length - 1]] },
        yaxis: { zeroline: m === "pci", zerolinecolor: RULE, rangemode: m === "rca" ? "tozero" : "normal",
                 range: m === "dva" ? [0, 100] : null, ticksuffix: m === "dva" ? "%" : "" }, shapes: shapes
      }, function (pt) { setYear(+pt.x); });
    },
    brk: function () {
      var d = D(), i = idx(), tot = d.sp[i], pts = [];
      $("t-break").textContent = "RCA × PCI · nhóm hàng chiếm ≥ 0,1% xuất khẩu · " + S.y;
      MH.js(S.ng).forEach(function (j) {
        var v = d.p[i][j], r = rca(d, i, j), p = W.pci[i][j];
        if (!tot || v < tot * 0.001 || !r || p === null) return;
        pts.push({ j: j, v: v, r: r, p: p });
      });
      var vmax = Math.max.apply(null, pts.map(function (q) { return q.v; }).concat([1]));
      var tick = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100];
      var sel = S.hs !== null ? +S.hs : -1;
      draw("g-break", [{
        type: "scatter", mode: "markers", x: pts.map(function (q) { return q.r; }), y: pts.map(function (q) { return q.p; }),
        marker: { size: pts.map(function (q) { return 6 + 30 * Math.sqrt(q.v / vmax); }),
                  color: pts.map(function (q) { var c = nganh[hs2Ng[q.j]].mau; return sel < 0 || q.j === sel ? c : mix(c, 0.65); }),
                  line: { color: pts.map(function (q) { return q.j === sel ? INK : "rgba(0,0,0,0.35)"; }),
                          width: pts.map(function (q) { return q.j === sel ? 2.4 : 0.6; }) }, opacity: 0.92 },
        customdata: pts.map(function (q) { var h = W.hs2[q.j]; return [h.ma + " " + h.ten, f(q.r, 2), f(q.p, 2), usd(q.v), q.j]; }),
        hovertemplate: "<b>%{customdata[0]}</b><br>RCA %{customdata[1]} · PCI %{customdata[2]}<br>%{customdata[3]}<extra></extra>"
      }], {
        margin: { l: 40, r: 10, t: 6, b: 34 },
        xaxis: { type: "log", title: { text: "RCA (thang log) — bên phải vạch: có lợi thế", font: { size: 10.5 }, standoff: 4 },
                 tickmode: "array", tickvals: tick, ticktext: tick.map(function (t) { return f(t, t < 1 ? 2 : 0); }) },
        yaxis: { title: { text: "PCI — trên vạch: hàng phức tạp", font: { size: 10.5 }, standoff: 2 } },
        shapes: [
          { type: "line", xref: "x", yref: "paper", x0: 1, x1: 1, y0: 0, y1: 1, line: { color: MUTED, width: 1, dash: "dash" } },
          { type: "line", xref: "paper", yref: "y", x0: 0, x1: 1, y0: 0, y1: 0, line: { color: MUTED, width: 1, dash: "dash" } }
        ]
      }, function (pt) {
        var j = pt.customdata && pt.customdata[4];
        if (j === undefined) return;
        S.hs = S.hs !== null && +S.hs === j ? null : String(j);
        render();
      });
    },
    table: function () {
      var m = S.m.mh, d = D(), i = idx(), j = soI(), y = soY(), tot = d.sp[i];
      var rows = [];
      MH.js(S.ng).forEach(function (k) {
        var h = W.hs2[k], v = d.p[i][k];
        if (v <= 0) return;
        var pv = j >= 0 ? d.p[j][k] : null;
        rows.push({ k: k, ma: h.ma, ten: h.ten, ng: nganh[h.ng].ten, mau: nganh[h.ng].mau, gt: v,
                    tt: tot ? v / tot * 100 : 0, ch: pv > 0 ? (v - pv) / pv * 100 : null,
                    rca: rca(d, i, k), pci: W.pci[i][k], _s: h.ma + " " + h.ten + " " + nganh[h.ng].ten });
      });
      var cols = [
        { k: "ma", label: "Mã", v: function (r) { return r.ma; }, f: function (r) { return r.ma; } },
        { k: "ten", label: "Nhóm hàng", v: function (r) { return r.ten; }, f: function (r) { return r.ten; } },
        { k: "ng", label: "Ngành", v: function (r) { return r.ng; }, f: function (r) { return r.ng; },
          html: function (r, v) { return '<span class="sw" style="background:' + r.mau + '"></span>' + esc(v); } },
        { k: "gt", label: "Kim ngạch (triệu USD)", num: true, bar: m === "v", v: function (r) { return r.gt; }, f: function (r) { return f(r.gt / 1e3, 1); } },
        { k: "tt", label: "Tỷ trọng", num: true, v: function (r) { return r.tt; }, f: function (r) { return pct(r.tt, 2); } }
      ];
      if (y !== null) cols.push({ k: "ch", label: "So với " + y, num: true, v: function (r) { return r.ch; },
        f: function (r) { return r.ch === null ? "—" : sgn(pct(r.ch), r.ch); }, cls: function (r) { return r.ch !== null && r.ch < 0 ? "down" : ""; } });
      cols.push({ k: "rca", label: "RCA", num: true, bar: m === "rca", v: function (r) { return r.rca; }, f: function (r) { return ok(r.rca) ? f(r.rca, 2) : "—"; } });
      cols.push({ k: "pci", label: "PCI", num: true, v: function (r) { return r.pci; }, f: function (r) { return ok(r.pci) ? f(r.pci, 2) : "—"; },
        cls: function (r) { return m === "pci" && r.pci < 0 ? "down" : ""; } });
      renderTable({
        title: "Nhóm hàng HS2 · " + ten(S.iso) + " · " + S.y, rows: rows, cols: cols, noun: "nhóm hàng",
        def: { k: { v: "gt", rca: "rca", pci: "pci", dva: "gt" }[m], dir: -1 },
        foot: function (rs) {
          var s = sum(rs.map(function (r) { return r.gt; }));
          return { ma: "Tổng", ten: f(rs.length) + " nhóm", gt: f(s / 1e3, 1), tt: tot ? pct(s / tot * 100, 2) : "" };
        },
        sel: function (r) { return S.hs !== null && +S.hs === r.k; },
        row: function (r) { return String(r.k); },
        onRow: function (k) { S.hs = S.hs === k ? null : k; render(); }
      });
    }
  };

  /* ========================================================== TRANG 3: SO SÁNH */

  var SS = {
    title: "So sánh",
    help: "So sánh nước đang xem với một nhóm nước. Bấm một thẻ chỉ số để đổi chỉ số cho cả trang; bấm tên một nước trên biểu đồ xếp hạng hoặc trong bảng để chuyển sang xem nước đó.",
    peers: function () {
      var i = idx(), ds;
      if (S.nhom === "asean") ds = ASEAN.slice();
      else if (S.nhom === "kv") {
        var kv = nuoc[S.iso].kv;
        ds = W.co.filter(function (iso) { return nuoc[iso].kv === kv; });
      } else ds = hang[i].ds.slice(0, 10).map(function (r) { return r[0]; });
      if (ds.indexOf(S.iso) < 0) ds.push(S.iso);
      return ds.filter(function (iso) { return W.cs[iso]; });
    },
    val: function (m, iso, t) {
      if (t < 0) return null;
      var c = W.cs[iso];
      if (m === "hx") return hang[t].h[iso] || null;
      if (m === "er") return c.er[t] || null;
      return sumX[t] && c.x[t] ? c.x[t] / sumX[t] * 100 : null;
    },
    series: function (m, iso) { return W.nam.map(function (_, t) { return SS.val(m, iso, t); }); },
    kpis: function () {
      var i = idx(), c = cs(S.iso);
      return [
        { id: "hx", label: "Hạng xuất khẩu", kind: "rank", invert: true, s: SS.series("hx", S.iso),
          val: function (v) { return [ok(v) ? f(v) : "—", "/ " + f(hang[i].n)]; },
          tip: "Thứ hạng theo tổng giá trị xuất khẩu hàng hóa trong năm, trong số các nước có số liệu. Hạng 1 là lớn nhất." },
        { id: "er", label: "Hạng ECI", kind: "rank", invert: true, s: SS.series("er", S.iso),
          val: function (v) { return [ok(v) ? f(v) : "—", c.en[i] ? "/ " + f(c.en[i]) : ""]; },
          tip: "ECI (chỉ số phức tạp kinh tế, Atlas) đo năng lực sản xuất qua độ đa dạng và độ khó của rổ hàng xuất khẩu. Hạng 1 là phức tạp nhất." },
        { id: "tp", label: "Thị phần xuất khẩu thế giới", kind: "pp", s: SS.series("tp", S.iso),
          val: function (v) { return [ok(v) ? f(v, 2) : "—", "%"]; },
          tip: "Xuất khẩu của nước này chia cho tổng xuất khẩu của mọi nước trong năm." }
      ];
    },
    unit: function (m) { return { hx: "hạng", er: "hạng", tp: "%" }[m]; },
    fmt: function (m, v) { return !ok(v) ? "—" : m === "tp" ? pct(v, 2) : f(v); },
    side: function () {
      var m = S.m.ss, i = idx(), j = soI(), ds = SS.peers();
      $("t-side").textContent = { hx: "Hạng xuất khẩu", er: "Hạng ECI", tp: "Thị phần xuất khẩu" }[m] + " · " + S.y;
      seg([["asean", "ASEAN"], ["kv", "Cùng khu vực"], ["top", "Top 10 xuất khẩu"]], S.nhom, function (v) { S.nhom = v; render(); });
      var rows = ds.map(function (iso) { return { iso: iso, v: SS.val(m, iso, i), p: SS.val(m, iso, j) }; })
        .filter(function (r) { return ok(r.v); });
      var rank = m !== "tp";
      rows.sort(function (a, b) { return rank ? a.v - b.v : b.v - a.v; });
      var lab = rows.map(function (r) { return ten(r.iso); }), tr = [];
      if (j >= 0) tr.push({ type: "bar", orientation: "h", y: lab, x: rows.map(function (r) { return r.p; }), name: String(soY()),
        customdata: rows.map(function (r) { return r.iso; }), marker: { color: rows.map(function (r) { return r.iso === S.iso ? "#a9acb4" : "#e6e3dc"; }) },
        text: rows.map(function (r) { return SS.fmt(m, r.p); }), textposition: "none",
        hovertemplate: "%{y}: %{text}<extra>" + soY() + "</extra>" });
      tr.push({ type: "bar", orientation: "h", y: lab, x: rows.map(function (r) { return r.v; }), name: String(S.y),
        customdata: rows.map(function (r) { return r.iso; }),
        marker: { color: rows.map(function (r) { return r.iso === S.iso ? INK : GREY; }) },
        text: rows.map(function (r) { return SS.fmt(m, r.v); }), textposition: "outside", cliponaxis: false,
        textfont: { size: 10.5, color: INK2 }, hovertemplate: "%{y}: %{text}<extra>" + S.y + "</extra>" });
      draw("g-side", tr, {
        margin: { l: 8, r: 40, t: 4, b: 24 }, bargap: 0.22, bargroupgap: 0.04, barmode: "group",
        yaxis: { autorange: "reversed", gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 10.5 } },
        xaxis: { ticksuffix: m === "tp" ? "%" : "", rangemode: "tozero" }
      }, function (pt) { if (pt.customdata && pt.customdata !== S.iso) change(pt.customdata, S.y); });
      $("n-side").textContent = (rank ? "Thanh ngắn hơn là hạng cao hơn. " : "") + (j >= 0 ? "Thanh nhạt phía trên: năm " + soY() + ". " : "") +
        "Bấm một nước để chuyển sang xem nước đó.";
    },
    trend: function () {
      var m = S.m.ss, ds = SS.peers(), i = idx();
      chip(null);
      $("t-trend").textContent = { hx: "Hạng xuất khẩu", er: "Hạng ECI", tp: "Thị phần xuất khẩu (%)" }[m] + " theo năm";
      var ordered = ds.filter(function (iso) { return iso !== S.iso; }).concat([S.iso]);
      var ends = [];
      var tr = ordered.map(function (iso) {
        var me = iso === S.iso, y = SS.series(m, iso), last = -1;
        for (var t = y.length - 1; t >= 0; t--) if (ok(y[t])) { last = t; break; }
        if (last >= 0) ends.push({ iso: iso, me: me, x: W.nam[last], y: y[last] });
        return { type: "scatter", mode: "lines", name: ten(iso), x: W.nam, y: y, connectgaps: false,
                 line: { color: me ? INK : GREY, width: me ? 3 : 1.3 },
                 hovertemplate: "%{x}: %{y:" + (m === "tp" ? ",.2f}%" : ",.0f}") + "<extra>" + esc(ten(iso)) + "</extra>" };
      });
      var ys = ends.map(function (e) { return e.y; });
      var span = (Math.max.apply(null, ys) - Math.min.apply(null, ys)) || 1, placed = [], ann = [];
      ends.sort(function (a, b) { if (a.me !== b.me) return a.me ? -1 : 1; return m === "tp" ? b.y - a.y : a.y - b.y; })
        .forEach(function (e) {
          if (!e.me && placed.some(function (p) { return Math.abs(p - e.y) < span * 0.07; })) return;
          placed.push(e.y);
          ann.push({ x: e.x, y: e.y, xanchor: "left", text: " " + esc(ten(e.iso)), showarrow: false,
                     font: { size: e.me ? 11.5 : 10, color: e.me ? INK : MUTED } });
        });
      var shapes = [yearLine(S.y)];
      if (soI() >= 0) shapes.push(yearLine(soY(), true));
      draw("g-trend", tr, {
        margin: { l: 40, r: 96, t: 8 }, xaxis: { dtick: 5, range: [W.nam[0], W.nam[W.nam.length - 1]] },
        yaxis: { autorange: m === "tp" ? true : "reversed" }, annotations: ann, shapes: shapes
      }, function (pt) { setYear(+pt.x); });
    },
    brk: function () {
      var i = idx(), ds = SS.peers();
      $("t-break").textContent = "Quy mô và năng lực · " + S.y;
      var pts = ds.map(function (iso) { var c = W.cs[iso]; return { iso: iso, x: c.x[i], e: c.eci[i] }; })
        .filter(function (p) { return p.x > 0 && ok(p.e); });
      var tick = [0.1, 1, 10, 100, 1000];
      draw("g-break", [{
        type: "scatter", mode: "markers+text", x: pts.map(function (p) { return p.x / 1e6; }), y: pts.map(function (p) { return p.e; }),
        text: pts.map(function (p) { return ten(p.iso); }), textposition: "top center", cliponaxis: false,
        textfont: { size: pts.map(function (p) { return p.iso === S.iso ? 11.5 : 10; }), color: pts.map(function (p) { return p.iso === S.iso ? INK : MUTED; }) },
        marker: { size: pts.map(function (p) { return p.iso === S.iso ? 13 : 9; }), color: pts.map(function (p) { return p.iso === S.iso ? INK : GREY; }),
                  line: { color: "#fff", width: 1 } },
        customdata: pts.map(function (p) { return [p.iso, usd(p.x), f(p.e, 2)]; }),
        hovertemplate: "<b>%{text}</b><br>Xuất khẩu %{customdata[1]} · ECI %{customdata[2]}<extra></extra>"
      }], {
        margin: { l: 40, r: 16, t: 14, b: 34 },
        xaxis: { type: "log", title: { text: "Xuất khẩu (tỷ USD, thang log)", font: { size: 10.5 }, standoff: 4 },
                 tickmode: "array", tickvals: tick, ticktext: tick.map(function (t) { return f(t, t < 1 ? 1 : 0); }) },
        yaxis: { title: { text: "ECI — cao hơn: phức tạp hơn", font: { size: 10.5 }, standoff: 2 }, zeroline: true, zerolinecolor: RULE }
      }, function (pt) { var iso = pt.customdata && pt.customdata[0]; if (iso && iso !== S.iso) change(iso, S.y); });
    },
    table: function () {
      var m = S.m.ss, i = idx(), j = soI(), y = soY();
      var rows = SS.peers().map(function (iso) {
        var c = W.cs[iso];
        return { iso: iso, ten: ten(iso), kv: nuoc[iso].kv, x: c.x[i], tp: SS.val("tp", iso, i), hx: SS.val("hx", iso, i),
                 eci: c.eci[i], er: SS.val("er", iso, i), p: SS.val(m, iso, j), _s: ten(iso) + " " + nuoc[iso].kv + " " + iso };
      });
      function ch(r) { var v = r[m]; if (!ok(v) || !ok(r.p)) return null; return m === "tp" ? v - r.p : r.p - v; }
      var cols = [
        { k: "ten", label: "Nước", v: function (r) { return r.ten; }, f: function (r) { return r.ten; } },
        { k: "kv", label: "Khu vực", v: function (r) { return r.kv; }, f: function (r) { return r.kv; } },
        { k: "x", label: "Xuất khẩu (tỷ USD)", num: true, bar: true, v: function (r) { return r.x; }, f: function (r) { return f(r.x / 1e6, 1); } },
        { k: "tp", label: "Thị phần", num: true, v: function (r) { return r.tp; }, f: function (r) { return ok(r.tp) ? pct(r.tp, 2) : "—"; } },
        { k: "hx", label: "Hạng xuất khẩu", num: true, v: function (r) { return r.hx; }, f: function (r) { return ok(r.hx) ? f(r.hx) : "—"; } },
        { k: "eci", label: "ECI", num: true, v: function (r) { return r.eci; }, f: function (r) { return ok(r.eci) ? f(r.eci, 2) : "—"; } },
        { k: "er", label: "Hạng ECI", num: true, v: function (r) { return r.er; }, f: function (r) { return ok(r.er) ? f(r.er) : "—"; } }
      ];
      if (y !== null) cols.push({ k: "ch", label: { hx: "Đổi hạng XK", er: "Đổi hạng ECI", tp: "Đổi thị phần" }[m] + " so với " + y, num: true, v: ch,
        f: function (r) { var c = ch(r); return c === null ? "—" : m === "tp" ? sgn(f(c, 3), c) + " điểm %" : sgn(f(c), c) + " bậc"; },
        cls: function (r) { var c = ch(r); return c !== null && c < 0 ? "down" : ""; } });
      renderTable({
        title: { asean: "ASEAN", kv: "Cùng khu vực " + nuoc[S.iso].kv, top: "10 nước xuất khẩu lớn nhất" }[S.nhom] + " · " + S.y,
        rows: rows, cols: cols, noun: "nước", def: { k: m, dir: m === "tp" ? -1 : 1 },
        foot: function (rs) {
          var s = sum(rs.map(function (r) { return r.x; }));
          return { ten: "Tổng · " + f(rs.length) + " nước", x: f(s / 1e6, 1), tp: sumX[i] ? pct(s / sumX[i] * 100, 2) : "" };
        },
        sel: function (r) { return r.iso === S.iso; },
        row: function (r) { return r.iso; },
        onRow: function (k) { if (k !== S.iso) change(k, S.y); }
      });
    }
  };

  var PAGES = { tq: TQ, mh: MH, ss: SS };

  /* ---------------------------------------------------------- vẽ cả trang */

  var lastPg = null;
  function render() {
    if (!D()) return;
    if (S.m.mh === "dva" && !MH.dvaOn()) S.m.mh = "v";     // TiVA chỉ có cho Việt Nam
    var P = PAGES[S.pg];
    document.body.dataset.pg = S.pg;
    $("pg-title").textContent = P.title;
    $("pg-help").dataset.tip = P.help;
    document.querySelectorAll(".rail__pages button").forEach(function (b) {
      if (b.dataset.pg === S.pg) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    renderKpis(P.kpis());
    P.side(); P.trend(); P.brk(); P.table();
    writeHash();
    if (lastPg !== S.pg) { lastPg = S.pg; requestAnimationFrame(resizeAll); }
  }

  function setYear(y) { if (W.nam.indexOf(y) >= 0 && y !== S.y) change(S.iso, y); }

  /* ---------------------------------------------------------- #hash */

  // #tq-VNM-2023-auto-x  (trang-nước-năm-so với-chỉ số); vẫn đọc dạng cũ #VNM-2023
  function writeHash() {
    var h = "#" + [S.pg, S.iso, S.y, S.so, S.m[S.pg]].join("-");
    if (location.hash !== h && history.replaceState) history.replaceState(null, "", h);
  }
  function readHash() {
    var o = { pg: S.pg, iso: S.iso, y: S.y || W.nam[W.nam.length - 1], so: S.so, m: null };
    var a = /^#(tq|mh|ss)-([A-Z]{3})-(\d{4})-(auto|\d{4})-([a-z]+)$/.exec(location.hash);
    var b = /^#([A-Z]{3})-(\d{4})$/.exec(location.hash);
    if (a) { o.pg = a[1]; o.iso = a[2]; o.y = +a[3]; o.so = a[4]; o.m = a[5]; }
    else if (b) { o.iso = b[1]; o.y = +b[2]; }
    if (W.co.indexOf(o.iso) < 0) o.iso = S.iso;
    if (W.nam.indexOf(o.y) < 0) o.y = W.nam[W.nam.length - 1];
    return o;
  }
  function applyHash() {
    var o = readHash();
    S.pg = o.pg; S.so = o.so;
    var valid = { tq: ["x", "m", "cc"], mh: ["v", "rca", "pci", "dva"], ss: ["hx", "er", "tp"] };
    if (o.m && valid[o.pg].indexOf(o.m) >= 0) S.m[o.pg] = o.m;
    change(o.iso, o.y);
  }

  /* ---------------------------------------------------------- dựng & nối */

  function setup() {
    var fn = $("f-nuoc"), fy = $("f-nam"), fs = $("f-so");
    var groups = {};
    W.co.forEach(function (iso) { var n = nuoc[iso]; (groups[n.kv] = groups[n.kv] || []).push(n); });
    fn.innerHTML = Object.keys(groups).sort(function (a, b) { return a.localeCompare(b, "vi"); })
      .map(function (k) {
        return '<optgroup label="' + esc(k) + '">' + groups[k].sort(function (a, b) {
          return a.ten.localeCompare(b.ten, "vi");
        }).map(function (n) { return '<option value="' + n.iso + '">' + esc(n.ten) + "</option>"; }).join("") + "</optgroup>";
      }).join("");
    var ys = W.nam.slice().reverse();
    fy.innerHTML = ys.map(function (y) { return '<option value="' + y + '">' + y + "</option>"; }).join("");
    fs.innerHTML = '<option value="auto">Năm trước</option><option value="none">Không so sánh</option>' +
      ys.map(function (y) { return '<option value="' + y + '">' + y + "</option>"; }).join("");

    fn.addEventListener("change", function () { change(fn.value, S.y); });
    fy.addEventListener("change", function () { change(S.iso, +fy.value); });
    fs.addEventListener("change", function () { S.so = fs.value; render(); });
    $("f-nam-lui").addEventListener("click", function () { change(S.iso, S.y - 1); });
    $("f-nam-toi").addEventListener("click", function () { change(S.iso, S.y + 1); });

    document.querySelectorAll(".rail__pages button").forEach(function (b) {
      b.addEventListener("click", function () { if (S.pg !== b.dataset.pg) { S.pg = b.dataset.pg; S.q = ""; $("f-q").value = ""; render(); } });
    });
    var kp = $("kpis");
    function pick(ev) {
      if (ev.target.closest(".q")) return;
      var k = ev.target.closest(".kpi");
      if (!k || S.m[S.pg] === k.dataset.m) return;
      S.m[S.pg] = k.dataset.m;
      S.sort[S.pg] = null;
      render();
      var again = kp.querySelector('[data-m="' + k.dataset.m + '"]');
      if (again && ev.type === "keydown") again.focus();
    }
    kp.addEventListener("click", pick);
    kp.addEventListener("keydown", function (ev) {
      if ((ev.key === "Enter" || ev.key === " ") && ev.target.classList.contains("kpi")) { ev.preventDefault(); pick(ev); }
    });

    var t = $("tbl");
    function sortBy(th) {
      var k = th.dataset.k, so = sortOf();
      var txt = TB.cols.filter(function (c) { return c.k === k; })[0];
      var isStr = txt && TB.rows.length && typeof txt.v(TB.rows[0]) === "string";
      S.sort[S.pg] = k === so.k ? { k: k, dir: -so.dir } : { k: k, dir: isStr ? 1 : -1 };
      PAGES[S.pg].table();
    }
    t.querySelector("thead").addEventListener("click", function (ev) { var th = ev.target.closest("th"); if (th) sortBy(th); });
    t.querySelector("thead").addEventListener("keydown", function (ev) {
      var th = ev.target.closest("th");
      if (th && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); sortBy(th); }
    });
    t.querySelector("tbody").addEventListener("click", function (ev) {
      var tr = ev.target.closest("tr[data-k]");
      if (tr && TB.onRow) TB.onRow(tr.dataset.k);
    });
    $("f-q").addEventListener("input", function () { S.q = this.value; PAGES[S.pg].table(); });
    $("f-csv").addEventListener("click", csv);
    window.addEventListener("hashchange", applyHash);
  }

  var busy = 0;
  function change(iso, y) {
    if (W.nam.indexOf(y) < 0) return;
    var ticket = ++busy, status = $("status");
    status.textContent = C[iso] ? "" : "Đang tải dữ liệu " + ten(iso) + "…";
    load(iso).then(function () {
      if (ticket !== busy) return;
      if (iso !== S.iso) { S.dt = null; S.hs = null; }
      S.iso = iso; S.y = y;
      if (S.dt && C[iso].dt.indexOf(S.dt) < 0) S.dt = null;
      $("f-nuoc").value = iso;
      $("f-nam").value = String(y);
      $("f-so").value = S.so;
      $("f-nam-lui").disabled = y <= W.nam[0];
      $("f-nam-toi").disabled = y >= W.nam[W.nam.length - 1];
      status.textContent = "";
      $("noi-dung").setAttribute("aria-busy", "false");
      render();
    }).catch(function (e) {
      status.textContent = "Không tải được dữ liệu " + iso + " (" + e.message + ").";
    });
  }

  function start() {
    fetch("data/world.json").then(function (r) { return r.json(); }).then(function (w) {
      W = w;
      prep();
      setup();
      applyHash();
    }).catch(function (e) {
      $("status").textContent = "Không tải được dữ liệu (" + e.message + ").";
    });
  }

  if (window.Plotly) start();
  else window.addEventListener("load", start);
})();
