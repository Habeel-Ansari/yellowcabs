// Yellow Cabs Whitecourt — shared site behaviour

document.addEventListener('DOMContentLoaded', () => {
  /* Sticky header shadow */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Mobile nav toggle */
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('is-open');
        toggle.classList.remove('is-open');
        document.body.style.overflow = '';
      });
    });
  }

  /* Gallery lightbox (only present on gallery.html) */
  const galleryGrid = document.querySelector('[data-gallery]');
  if (galleryGrid) {
    initGallery(galleryGrid);
  }
});

function initGallery(grid) {
  const loading = document.querySelector('.gallery-loading');
  try {
    const items = window.GALLERY_ITEMS || [];
    if (!items.length) throw new Error('Gallery data not found');

    const frag = document.createDocumentFragment();
    items.forEach((item, i) => {
      const fig = document.createElement('figure');
      fig.dataset.index = i;
      fig.tabIndex = 0;
      fig.setAttribute('role', 'button');
      fig.setAttribute('aria-label', `Open photo ${i + 1} of ${items.length}, enlarged`);
      fig.innerHTML = `
        <img src="images/gallery/thumb/${item.slug}.webp" alt="${(item.alt || 'Yellow Cabs Whitecourt taxi').replace(/"/g, '&quot;')}" loading="lazy" width="${item.w}" height="${item.h}">
        <span class="zoom-badge" aria-hidden="true" focusable="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3" stroke-linecap="round"/><path d="M11 8v6M8 11h6" stroke-linecap="round"/></svg></span>
      `;
      frag.appendChild(fig);
    });
    grid.appendChild(frag);
    if (loading) loading.remove();

    setupLightbox(grid, items);
  } catch (err) {
    if (loading) loading.textContent = 'Unable to load gallery right now — please refresh, or call 780-527-5050.';
    console.error(err);
  }
}

function setupLightbox(grid, items) {
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Photo viewer');
  lb.innerHTML = `
    <button class="lightbox-close" aria-label="Close photo viewer"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12" stroke-linecap="round"/></svg></button>
    <button class="lightbox-prev" aria-label="Previous photo"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <button class="lightbox-next" aria-label="Next photo"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <img src="" alt="">
    <div class="lightbox-counter" aria-live="polite"></div>
  `;
  document.body.appendChild(lb);

  const img = lb.querySelector('img');
  const counter = lb.querySelector('.lightbox-counter');
  const closeBtn = lb.querySelector('.lightbox-close');
  const prevBtn = lb.querySelector('.lightbox-prev');
  const nextBtn = lb.querySelector('.lightbox-next');
  const focusable = [prevBtn, nextBtn, closeBtn];
  let current = 0;
  let trigger = null;

  const show = (i) => {
    current = (i + items.length) % items.length;
    const item = items[current];
    img.src = `images/gallery/full/${item.slug}.webp`;
    img.alt = item.alt || 'Yellow Cabs Whitecourt taxi';
    counter.textContent = `${current + 1} / ${items.length}`;
  };

  const open = (i, triggerEl) => {
    trigger = triggerEl || null;
    show(i);
    lb.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  };
  const close = () => {
    lb.classList.remove('is-open');
    document.body.style.overflow = '';
    if (trigger) trigger.focus();
  };

  const activate = (fig) => open(parseInt(fig.dataset.index, 10), fig);

  grid.addEventListener('click', (e) => {
    const fig = e.target.closest('figure');
    if (fig) activate(fig);
  });
  grid.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const fig = e.target.closest('figure');
    if (!fig) return;
    e.preventDefault();
    activate(fig);
  });

  closeBtn.addEventListener('click', close);
  prevBtn.addEventListener('click', () => show(current - 1));
  nextBtn.addEventListener('click', () => show(current + 1));
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'ArrowLeft') { show(current - 1); return; }
    if (e.key === 'ArrowRight') { show(current + 1); return; }
    if (e.key === 'Tab') {
      // Simple focus trap: keep Tab cycling within the three controls.
      const idx = focusable.indexOf(document.activeElement);
      e.preventDefault();
      const dir = e.shiftKey ? -1 : 1;
      const next = focusable[(idx + dir + focusable.length) % focusable.length] || focusable[0];
      next.focus();
    }
  });
}
