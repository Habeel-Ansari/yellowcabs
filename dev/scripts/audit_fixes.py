import re, os

SITE = r"C:\Users\habza\Documents\Yellow cabs Whitecourt\website"
FILES = ["index.html", "about.html", "gallery.html", "contact.html"]

SKIP_LINK = '<a class="skip-link" href="#main-content">Skip to main content</a>\n'

for fname in FILES:
    path = os.path.join(SITE, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # 1. Skip link right after <body>
    html = html.replace("<body>\n", "<body>\n" + SKIP_LINK, 1)

    # 2. Wrap main content in <main id="main-content">
    html = html.replace("</header>\n\n<section", "</header>\n\n<main id=\"main-content\">\n<section", 1)
    html = html.replace("\n<footer class=\"site-footer\">", "\n</main>\n\n<footer class=\"site-footer\">", 1)

    # 3. nav-toggle aria-controls
    html = html.replace(
        '<button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">',
        '<button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="mainNav">'
    )

    # 4. phone-pill accessible name (icon-only on mobile otherwise)
    html = html.replace(
        '<a href="tel:7805275050" class="phone-pill">',
        '<a href="tel:7805275050" class="phone-pill" aria-label="Call Yellow Cabs Whitecourt at 780-527-5050">'
    )

    # 5. Decorative SVGs -> hide from assistive tech (every svg in these files is
    #    paired with adjacent visible text or an aria-labelled control)
    html = re.sub(r'<svg viewBox=', '<svg aria-hidden="true" focusable="false" viewBox=', html)
    html = re.sub(r'<svg class="brand-mark" viewBox=',
                   '<svg class="brand-mark" aria-hidden="true" focusable="false" viewBox=', html)

    # 6. Remove eyebrow/kicker labels entirely (anti-pattern: label above heading)
    html = re.sub(r'[ \t]*<div class="eyebrow"[^>]*>.*?</div>\n', '', html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"updated {fname}")
    else:
        print(f"NO CHANGE {fname}")
