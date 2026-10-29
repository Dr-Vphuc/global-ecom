/* Dashboard — global-ecom.
 *
 * Bốn việc:
 *  1. Tab: ba nhóm biểu đồ, đúng mẫu ARIA tablist (mũi tên, Home, End), nhớ tab
 *     trên #hash để gửi link thẳng tới một tab.
 *  2. Cắt khung: mỗi biểu đồ là đúng file của bài viết, mang tiêu đề và nguồn ở
 *     lề. Sau khi Plotly vẽ xong, đo các annotation lề trên/lề dưới (chỉ số do
 *     build_dashboard.py ghi trong #chart-meta) rồi chỉ chừa phần ở giữa.
 *  3. Nút phân đoạn trong từng thẻ: như bài viết, nút chỉ bị khoá khi không tổ
 *     hợp nào khớp với các lựa chọn ở những chiều đứng trước nó.
 *  4. Bộ chọn năm toàn trang: đổi giá trị ở sáu ô chỉ số và chuyển mọi thẻ có
 *     chiều "Năm" sang năm đó.
 */
(function () {
  "use strict";

  var META = JSON.parse(document.getElementById("chart-meta").textContent);
  var crop = {};          // tên file → [trên, dưới] đã đo
  var PAD = 6;

  /* ---------------------------------------------------------- cắt khung */

  function fit(card) {
    var frame = card.querySelector(".card__frame");
    var ifr = frame.querySelector("iframe");
    var m = META[card._file];
    if (!m) return;
    var c = crop[card._file] || m.cat;
    var s = frame.clientWidth / m.w;
    frame.style.setProperty("--w", m.w);
    frame.style.setProperty("--ch", Math.max(1, c[1] - c[0]));
    ifr.style.transform = "scale(" + s + ") translateY(" + (-c[0]) + "px)";
  }

  function measure(card, file, tries) {
    var ifr = card.querySelector("iframe");
    var doc;
    try { doc = ifr.contentDocument; } catch (e) { doc = null; }
    var m = META[file];
    var ann = doc ? doc.querySelectorAll(".annotation[data-index]") : [];
    if (!doc || !ann.length) {
      if (tries < 120) {
        requestAnimationFrame(function () { measure(card, file, tries + 1); });
      } else {
        ready(card);   // không đo được (file:// chặn truy cập): giữ ước lượng
      }
      return;
    }
    var byIdx = {}, bo = {};
    for (var i = 0; i < ann.length; i++) byIdx[ann[i].getAttribute("data-index")] = ann[i];
    var top = 0, bottom = m.h;
    m.tren.forEach(function (k) {
      var el = byIdx[k];
      if (!el) return;
      top = Math.max(top, el.getBoundingClientRect().bottom + PAD);
      bo[k] = el;
    });
    m.duoi.forEach(function (k) {
      var el = byIdx[k];
      if (!el) return;
      bottom = Math.min(bottom, el.getBoundingClientRect().top - PAD);
      bo[k] = el;
    });
    // Ở vài hình, phụ đề gốc chồng lên tiêu đề ô con và chú giải chồng lên dòng
    // nguồn. Nên: ẩn hẳn annotation bị bỏ, rồi nới chỗ cắt cho không phạm vào
    // bất kỳ phần tử nào còn giữ (annotation khác, chú giải, nhãn trục).
    Object.keys(bo).forEach(function (k) { bo[k].style.visibility = "hidden"; });
    var giu = doc.querySelectorAll(".annotation, .legend, .xtick, .ytick, .g-xtitle, .g-ytitle");
    for (var j = 0; j < giu.length; j++) {
      var el = giu[j];
      if (el.classList.contains("annotation") && bo[el.getAttribute("data-index")]) continue;
      var r = el.getBoundingClientRect();
      if (r.height <= 0 || r.width <= 0) continue;
      top = Math.min(top, r.top - 2);
      bottom = Math.max(bottom, r.bottom + 2);
    }
    top = Math.max(0, top);
    bottom = Math.min(m.h, bottom);
    if (bottom - top > 40) crop[file] = [Math.round(top), Math.round(bottom)];
    if (card._file === file) ready(card);
  }

  function ready(card) {
    fit(card);
    card.querySelector(".card__frame").classList.add("is-ready");
  }

  function show(card, file) {
    var m = META[file];
    if (!m) return;
    card._file = file;
    card.querySelector(".card__title").textContent = m.tieu_de;
    card.querySelector(".card__sub").textContent = m.phu_de;
    card.querySelector(".card__open").setAttribute("href", "charts/" + file + ".html");
    if (!card._live) { fit(card); return; }
    var frame = card.querySelector(".card__frame");
    var ifr = frame.querySelector("iframe");
    var src = "charts/" + file + ".html";
    if (ifr.getAttribute("src") === src) return;
    frame.classList.remove("is-ready");
    ifr.setAttribute("width", m.w);
    ifr.setAttribute("height", m.h);
    ifr.setAttribute("title", m.tieu_de);
    fit(card);
    ifr.onload = function () { measure(card, file, 0); };
    ifr.setAttribute("src", src);
  }

  /* ---------------------------------------------------------- nút trong thẻ */

  function setupCard(card) {
    var map = JSON.parse(card.getAttribute("data-map"));
    var keys = Object.keys(map);
    var segs = Array.prototype.slice.call(card.querySelectorAll(".seg"));
    var state = segs.map(function (seg) {
      return seg.querySelector('[aria-pressed="true"]').getAttribute("data-val");
    });
    card._map = map;
    card._state = state;
    card._segs = segs;
    card._file = map[state.join("|")];

    function exists(prefix) {
      return keys.some(function (k) {
        var p = k.split("|");
        return prefix.every(function (v, i) { return p[i] === v; });
      });
    }

    function resolve(from) {
      // Giữ các chiều trước `from`, các chiều sau lấy giá trị hợp lệ đầu tiên.
      if (map[state.join("|")]) return;
      for (var d = from + 1; d < segs.length; d++) {
        var vals = Array.prototype.map.call(segs[d].querySelectorAll(".seg__btn"),
          function (b) { return b.getAttribute("data-val"); });
        for (var j = 0; j < vals.length; j++) {
          var trial = state.slice(0, d).concat([vals[j]]);
          if (exists(trial)) { state[d] = vals[j]; break; }
        }
      }
    }

    card._render = function () {
      segs.forEach(function (seg, d) {
        Array.prototype.forEach.call(seg.querySelectorAll(".seg__btn"), function (b) {
          var v = b.getAttribute("data-val");
          b.setAttribute("aria-pressed", v === state[d] ? "true" : "false");
          b.disabled = d > 0 && !exists(state.slice(0, d).concat([v]));
        });
      });
      show(card, map[state.join("|")]);
    };

    card._set = function (d, v) {
      state[d] = v;
      resolve(d);
      if (!map[state.join("|")]) {
        // Chiều sau không cứu được (vd. năm 1995 khi đang xem node-link): đổi
        // các chiều trước sang tổ hợp đầu tiên có giá trị này.
        for (var i = 0; i < keys.length; i++) {
          var p = keys[i].split("|");
          if (p[d] === v) { for (var j = 0; j < p.length; j++) state[j] = p[j]; break; }
        }
      }
      card._render();
    };

    segs.forEach(function (seg, d) {
      seg.addEventListener("click", function (ev) {
        var b = ev.target.closest(".seg__btn");
        if (!b || b.disabled) return;
        card._set(d, b.getAttribute("data-val"));
      });
    });
    card._render();
  }

  var cards = Array.prototype.slice.call(document.querySelectorAll(".card[data-map]"));
  cards.forEach(setupCard);

  function goLive(panel) {
    Array.prototype.forEach.call(panel.querySelectorAll(".card[data-map]"), function (c) {
      if (c._live) { fit(c); return; }
      c._live = true;
      var f = c._file;
      c.querySelector("iframe").removeAttribute("src");
      show(c, f);
    });
  }

  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(function (entries) {
      entries.forEach(function (en) { fit(en.target.closest(".card")); });
    });
    cards.forEach(function (c) { ro.observe(c.querySelector(".card__frame")); });
  } else {
    window.addEventListener("resize", function () { cards.forEach(fit); });
  }

  /* ---------------------------------------------------------- tab */

  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));

  function activate(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) tab.focus();
    var panel = document.getElementById(tab.getAttribute("aria-controls"));
    goLive(panel);
    if (history.replaceState) history.replaceState(null, "", "#" + panel.id);
  }

  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { activate(t, false); });
    t.addEventListener("keydown", function (ev) {
      var j = null;
      if (ev.key === "ArrowRight") j = (i + 1) % tabs.length;
      else if (ev.key === "ArrowLeft") j = (i - 1 + tabs.length) % tabs.length;
      else if (ev.key === "Home") j = 0;
      else if (ev.key === "End") j = tabs.length - 1;
      if (j === null) return;
      ev.preventDefault();
      activate(tabs[j], true);
    });
  });

  var start = tabs.filter(function (t) {
    return "#" + t.getAttribute("aria-controls") === location.hash;
  })[0] || tabs[0];
  activate(start, false);

  /* ---------------------------------------------------------- năm toàn trang */

  var yearBtns = Array.prototype.slice.call(document.querySelectorAll(".seg--global .seg__btn"));
  var NOW = yearBtns[0].getAttribute("data-year");

  function setYear(y) {
    yearBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-year") === y ? "true" : "false");
    });
    Array.prototype.forEach.call(document.querySelectorAll(".kpi"), function (k) {
      var v = JSON.parse(k.getAttribute("data-values"))[y];
      if (!v) return;
      k.querySelector(".kpi__num").textContent = v[0];
      k.querySelector(".kpi__unit").textContent = v[1];
      var d = k.querySelector(".kpi__delta");
      d.textContent = d.getAttribute(y === NOW ? "data-now" : "data-base");
      Array.prototype.forEach.call(k.querySelectorAll(".spark__dot"), function (c) {
        c.classList.toggle("is-on", c.getAttribute("data-year") === y);
      });
    });
    cards.forEach(function (c) {
      c._segs.forEach(function (seg, d) {
        if (seg.getAttribute("data-name") !== "Năm") return;
        if (seg.querySelector('[data-val="' + y + '"]')) c._set(d, y);
      });
    });
  }

  yearBtns.forEach(function (b) {
    b.addEventListener("click", function () { setYear(b.getAttribute("data-year")); });
  });
  setYear(NOW);
})();
