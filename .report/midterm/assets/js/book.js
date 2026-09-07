/**
 * Book Layout & Interactive Controller
 * Chapter 9, Section 9.1 (Ward, Grinstein, Keim)
 */

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('readerCanvas');
  const pageSelect = document.getElementById('pageSelect');
  const zoomInBtn = document.getElementById('zoomInBtn');
  const zoomOutBtn = document.getElementById('zoomOutBtn');
  const zoomResetBtn = document.getElementById('zoomResetBtn');
  const viewModeBtn = document.getElementById('viewModeBtn');
  const printBtn = document.getElementById('printBtn');
  const glossaryBtn = document.getElementById('glossaryBtn');
  const glossaryModal = document.getElementById('glossaryModal');
  const drawerClose = document.getElementById('drawerClose');
  const bilingualBar = document.getElementById('bilingualPreviewBar');
  const bilingualContent = document.getElementById('bilingualContent');

  let currentZoom = 1.0;
  let isContinuous = false;
  let bilingualActive = false;

  // 1. Zoom Controls
  function applyZoom(scale) {
    currentZoom = Math.min(Math.max(scale, 0.6), 1.6);
    if (!isContinuous) {
      canvas.style.transform = `scale(${currentZoom})`;
    } else {
      canvas.style.transform = 'none';
      canvas.style.zoom = currentZoom;
    }
    if (zoomResetBtn) {
      zoomResetBtn.textContent = `${Math.round(currentZoom * 100)}%`;
    }
  }

  if (zoomInBtn) {
    zoomInBtn.addEventListener('click', () => applyZoom(currentZoom + 0.1));
  }

  if (zoomOutBtn) {
    zoomOutBtn.addEventListener('click', () => applyZoom(currentZoom - 0.1));
  }

  if (zoomResetBtn) {
    zoomResetBtn.addEventListener('click', () => applyZoom(1.0));
  }

  // 2. Page Navigation
  if (pageSelect) {
    pageSelect.addEventListener('change', (e) => {
      const pageId = e.target.value;
      const targetElement = document.getElementById(pageId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    // Update select on scroll
    const pages = document.querySelectorAll('.book-page');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
          pageSelect.value = entry.target.id;
        }
      });
    }, { threshold: 0.5 });

    pages.forEach(p => observer.observe(p));
  }

  // 3. Dual View Mode (Book Pages vs Continuous)
  if (viewModeBtn) {
    viewModeBtn.addEventListener('click', () => {
      isContinuous = !isContinuous;
      if (isContinuous) {
        canvas.classList.add('continuous-mode');
        viewModeBtn.classList.add('active');
        viewModeBtn.querySelector('.mode-label').textContent = 'Trang rời';
        canvas.style.transform = 'none';
      } else {
        canvas.classList.remove('continuous-mode');
        viewModeBtn.classList.remove('active');
        viewModeBtn.querySelector('.mode-label').textContent = 'Đọc cuộn';
        applyZoom(currentZoom);
      }
    });
  }

  // 4. Print
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // 5. Glossary & Metadata Modal Drawer
  if (glossaryBtn && glossaryModal && drawerClose) {
    glossaryBtn.addEventListener('click', () => {
      glossaryModal.classList.add('active');
    });

    drawerClose.addEventListener('click', () => {
      glossaryModal.classList.remove('active');
    });

    glossaryModal.addEventListener('click', (e) => {
      if (e.target === glossaryModal) {
        glossaryModal.classList.remove('active');
      }
    });
  }

  // 6. Bilingual English Reference Inspection
  const bilingualTargets = document.querySelectorAll('[data-en]');
  bilingualTargets.forEach(el => {
    el.classList.add('bilingual-target');
    el.addEventListener('mouseenter', () => {
      const enText = el.getAttribute('data-en');
      if (enText && bilingualBar && bilingualContent) {
        bilingualContent.textContent = enText;
        bilingualBar.classList.add('visible');
      }
    });

    el.addEventListener('mouseleave', () => {
      if (bilingualBar) {
        bilingualBar.classList.remove('visible');
      }
    });
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && glossaryModal && glossaryModal.classList.contains('active')) {
      glossaryModal.classList.remove('active');
    }
  });
});
