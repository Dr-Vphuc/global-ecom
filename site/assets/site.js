/* Trang demo — global-ecom. Không phụ thuộc thư viện nào.
 *
 * 1. Mỗi biểu đồ nằm trong iframe giữ đúng KHUNG GỐC của nó (rộng 454 pt, cao
 *    theo tỷ lệ PNG — xem build_web.py), rồi được phóng bằng transform cho vừa
 *    cột. Để Plotly tự giãn thì tiêu đề trong hình đè lên vùng vẽ.
 * 2. Iframe chỉ được nạp khi sắp cuộn tới, để 22 hình không cùng tải một lúc.
 * 3. Nút chọn phương án (năm, cách vẽ) đổi file trong cùng khung; tổ hợp không
 *    có file thì nút bị khoá, không bị giấu.
 */
(function () {
  "use strict";

  var figures = Array.prototype.slice.call(document.querySelectorAll(".fig"));

  // ---------------------------------------------------------- thu phóng
  function fit(frame) {
    var iframe = frame.querySelector("iframe");
    var w = parseFloat(iframe.getAttribute("width"));
    var s = frame.clientWidth / w;
    iframe.style.transform = "scale(" + s + ")";
  }

  var ro = "ResizeObserver" in window
    ? new ResizeObserver(function (entries) {
        entries.forEach(function (e) { fit(e.target); });
      })
    : null;

  // ---------------------------------------------------------- nạp lười
  function load(fig) {
    var iframe = fig.querySelector("iframe");
    if (iframe.getAttribute("src")) return;
    iframe.setAttribute("src", iframe.getAttribute("data-src"));
  }

  var io = "IntersectionObserver" in window
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { load(e.target); io.unobserve(e.target); }
        });
      }, { rootMargin: "900px 0px" })
    : null;

  // ---------------------------------------------------------- phương án
  function setup(fig) {
    var map = JSON.parse(fig.getAttribute("data-map"));
    var size = JSON.parse(fig.getAttribute("data-size"));
    var frame = fig.querySelector(".fig__frame");
    var iframe = frame.querySelector("iframe");
    var open = fig.querySelector(".fig__open");
    var groups = Array.prototype.slice.call(fig.querySelectorAll(".seg"));

    function current() {
      return groups.map(function (g) {
        return g.querySelector('[aria-pressed="true"]').getAttribute("data-val");
      });
    }

    // Một nút chỉ bị khoá khi KHÔNG tổ hợp nào khớp các chiều đứng TRƯỚC nó.
    // Chiều đầu (cách vẽ) vì vậy không bao giờ bị khoá: đang xem 1995 mà bấm
    // node-link thì năm tự lùi về năm có hình, thay vì bắt người xem đoán phải
    // đổi năm trước.
    var keys = Object.keys(map).map(function (k) { return k.split("|"); });
    function exists(prefix) {
      return keys.some(function (k) {
        for (var i = 0; i < prefix.length; i++) if (k[i] !== prefix[i]) return false;
        return true;
      });
    }
    function refresh() {
      var cur = current();
      groups.forEach(function (g, i) {
        g.querySelectorAll(".seg__btn").forEach(function (b) {
          var ok = exists(cur.slice(0, i).concat(b.getAttribute("data-val")));
          b.disabled = !ok;
          b.title = ok ? "" : "Không có hình cho tổ hợp này";
        });
      });
    }

    function show(name) {
      var wh = size[name];
      if (!wh) return;           // tổ hợp không có hình: giữ nguyên hình đang xem
      iframe.setAttribute("width", wh[0]);
      iframe.setAttribute("height", wh[1]);
      frame.style.setProperty("--w", wh[0]);
      frame.style.setProperty("--h", wh[1]);
      var url = "charts/" + name + ".html";
      iframe.setAttribute("data-src", url);
      open.setAttribute("href", url);
      if (iframe.getAttribute("src")) {
        frame.classList.remove("is-ready");
        iframe.setAttribute("src", url);
      }
      fit(frame);
    }

    groups.forEach(function (g, i) {
      g.addEventListener("click", function (ev) {
        var b = ev.target.closest(".seg__btn");
        if (!b || b.disabled || b.getAttribute("aria-pressed") === "true") return;
        g.querySelectorAll(".seg__btn").forEach(function (x) {
          x.setAttribute("aria-pressed", x === b ? "true" : "false");
        });
        // Đổi cách vẽ sang một tổ hợp không có năm đang chọn (node-link chỉ
        // có năm tham chiếu): tự lùi về phương án hợp lệ đầu tiên của chiều kia.
        var cur = current();
        if (!map[cur.join("|")]) {
          groups.forEach(function (h, j) {
            if (j === i) return;
            var btns = Array.prototype.slice.call(h.querySelectorAll(".seg__btn"));
            for (var n = 0; n < btns.length; n++) {
              var k = cur.slice(); k[j] = btns[n].getAttribute("data-val");
              if (map[k.join("|")]) {
                btns.forEach(function (x) { x.setAttribute("aria-pressed", x === btns[n] ? "true" : "false"); });
                cur = k;
                break;
              }
            }
          });
        }
        refresh();
        show(map[cur.join("|")]);
      });
    });

    iframe.addEventListener("load", function () { frame.classList.add("is-ready"); });
    if (groups.length) refresh();
    fit(frame);
    if (ro) ro.observe(frame);
    if (io) io.observe(fig); else load(fig);
  }

  figures.forEach(setup);
  if (!ro) window.addEventListener("resize", function () {
    figures.forEach(function (f) { fit(f.querySelector(".fig__frame")); });
  });

  // ---------------------------------------------------------- điều hướng
  var links = {};
  document.querySelectorAll("[data-nav]").forEach(function (a) {
    links[a.getAttribute("data-nav")] = a;
  });
  var sections = Array.prototype.slice.call(document.querySelectorAll(".beat"));
  var active = null;

  function mark(id) {
    if (id === active) return;
    active = id;
    Object.keys(links).forEach(function (k) {
      if (k === id) links[k].setAttribute("aria-current", "true");
      else links[k].removeAttribute("aria-current");
    });
    if (id && links[id] && links[id].scrollIntoView) {
      // Thanh điều hướng cuộn ngang trên điện thoại: giữ mục đang đọc trong tầm mắt.
      var nav = links[id].closest(".mast__nav");
      if (nav && nav.scrollWidth > nav.clientWidth) {
        nav.scrollLeft = links[id].offsetLeft - 24;
      }
    }
    if (history.replaceState) {
      history.replaceState(null, "", id ? "#" + id : location.pathname + location.search);
    }
  }

  // Mục đang đọc = mục cuối cùng có mép trên đã đi qua 40% chiều cao màn hình.
  function spy() {
    var line = window.innerHeight * 0.4;
    var id = null;
    sections.forEach(function (s) {
      if (s.getBoundingClientRect().top <= line) id = s.id;
    });
    var limits = document.getElementById("gioi-han");
    if (limits && limits.getBoundingClientRect().top <= line) id = null;
    mark(id);
  }

  var bar = document.querySelector(".mast__progress span");
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = "scaleX(" + (h > 0 ? window.scrollY / h : 0) + ")";
      spy();
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
