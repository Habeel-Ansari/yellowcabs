import re, os

SITE = r"C:\Users\habza\Documents\Yellow cabs Whitecourt\website"
FILES = ["index.html", "about.html", "gallery.html", "contact.html"]

HEADER_BLOCK = '''    <a href="index.html" class="brand">
      <svg class="brand-mark" aria-hidden="true" focusable="false" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <rect width="48" height="48" rx="14" fill="#101010"/>
        <rect x="10" y="16" width="28" height="10" rx="5" fill="#f6c216"/>
        <path d="M14 16c1.5-4 4-6 10-6s8.5 2 10 6" fill="none" stroke="#f6c216" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="16" cy="27" r="3.2" fill="#101010" stroke="#f6c216" stroke-width="2"/>
        <circle cx="32" cy="27" r="3.2" fill="#101010" stroke="#f6c216" stroke-width="2"/>
        <rect x="4" y="34" width="8" height="7" fill="#f6c216"/>
        <rect x="20" y="34" width="8" height="7" fill="#f6c216"/>
        <rect x="36" y="34" width="8" height="7" fill="#f6c216"/>
      </svg>
      <span class="brand-text">
        <span class="name">Yellow Cabs</span>
        <span class="place">Whitecourt</span>
      </span>
    </a>'''

HEADER_REPLACEMENT = '''    <a href="index.html" class="brand">
      <img src="images/logo.webp" alt="Yellow Cabs Whitecourt" class="brand-logo" width="68" height="60">
    </a>'''

FOOTER_BLOCK = '''        <a href="index.html" class="brand">
          <svg class="brand-mark" aria-hidden="true" focusable="false" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <rect width="48" height="48" rx="14" fill="#f6c216"/>
            <rect x="10" y="16" width="28" height="10" rx="5" fill="#101010"/>
            <path d="M14 16c1.5-4 4-6 10-6s8.5 2 10 6" fill="none" stroke="#101010" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="16" cy="27" r="3.2" fill="#f6c216" stroke="#101010" stroke-width="2"/>
            <circle cx="32" cy="27" r="3.2" fill="#f6c216" stroke="#101010" stroke-width="2"/>
            <rect x="4" y="34" width="8" height="7" fill="#101010"/>
            <rect x="20" y="34" width="8" height="7" fill="#101010"/>
            <rect x="36" y="34" width="8" height="7" fill="#101010"/>
          </svg>
          <span class="brand-text">
            <span class="name">Yellow Cabs</span>
            <span class="place">Whitecourt</span>
          </span>
        </a>'''

FOOTER_REPLACEMENT = '''        <a href="index.html" class="brand">
          <span class="brand-logo-plate"><img src="images/logo.webp" alt="Yellow Cabs Whitecourt" class="brand-logo" width="68" height="60"></span>
        </a>'''

for fname in FILES:
    path = os.path.join(SITE, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    assert HEADER_BLOCK in html, f"header block not found in {fname}"
    assert FOOTER_BLOCK in html, f"footer block not found in {fname}"

    html = html.replace(HEADER_BLOCK, HEADER_REPLACEMENT, 1)
    html = html.replace(FOOTER_BLOCK, FOOTER_REPLACEMENT, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"updated {fname}")
