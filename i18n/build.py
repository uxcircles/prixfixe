"""Build the French (fr/) and Traditional Chinese (zh/) pages from the English ones.

Run from the repo root after changing any English page:  python3 i18n/build.py

English pages are the source. The script streams each page through Python's HTML
parser and copies it through unchanged except for: text and alt/aria/placeholder
attributes found in i18n/translations.py, asset paths (one folder deeper), the
<html lang>, and the language switcher + hreflang links it adds (also to the English
pages). Anything not in translations.py (wine names, places, brands) stays as written.
"""
import html, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "i18n"))
from translations import T

PAGES = ["index.html", "menu.html", "about.html", "contact.html", "reservation.html"]
LANGS = {"en": ("en", None), "fr": ("fr", 0), "zh": ("zh-Hant", 1)}
SWITCH = [("en", "EN", "English"), ("fr", "FR", "Français"), ("zh", "中文", "中文")]
TEXT_ATTRS = ("alt", "aria-label", "placeholder", "title")
ZH_FONT = "https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;600&amp;display=swap"
VOID = {"meta", "link", "img", "br", "input", "source", "hr"}


def href(lang, page, from_lang):
    up = "" if from_lang == "en" else "../"
    return f"{up}{page}" if lang == "en" else f"{up}{lang}/{page}"


class Rewriter(HTMLParser):
    def __init__(self, page, lang, missing):
        super().__init__(convert_charrefs=True)
        self.page, self.lang, self.missing = page, lang, missing
        self.idx = LANGS[lang][1]
        self.out, self.stack, self.skip = [], [], 0

    # -- helpers
    def tr(self, s):
        key = s.strip()
        if self.idx is None or not key:
            return s
        if key in T:
            t = T[key][self.idx]
            # no space before full-width punctuation, e.g. after a link: "…</a>，我們…"
            lead = "" if t[:1] in "，。、：；！？）" else s[: len(s) - len(s.lstrip())]
            return lead + t + s[len(s.rstrip()):]
        if re.search(r"[A-Za-z]{3}", key):
            self.missing.add(key)
        return s

    def relink(self, v):
        if self.lang == "en" or re.match(r"^(https?:|//|#|mailto:|tel:|data:)", v) or v.split("#")[0].endswith(".html"):
            return v
        return "../" + v

    def emit_tag(self, tag, attrs, closed):
        parts = [f"<{tag}"]
        for k, v in attrs:
            parts.append(f" {k}" if v is None else f' {k}="{html.escape(v, quote=True)}"')
        parts.append(" />" if closed and tag not in VOID else ">")
        self.out.append("".join(parts))

    def switcher(self, indent):
        links = []
        for code, label, name in SWITCH:
            hl = LANGS[code][0]
            cur = ' aria-current="true"' if code == self.lang else ""
            links.append(f'<a href="{href(code, self.page, self.lang)}" hreflang="{hl}" lang="{hl}" aria-label="{name}"{cur}>{label}</a>')
        return f'{indent}<span class="lang-switch">{"".join(links)}</span>\n'

    # -- parser events
    def handle_decl(self, d): self.out.append(f"<!{d}>")
    def handle_comment(self, d): self.out.append(f"<!--{d}-->")

    def handle_starttag(self, tag, attrs, closed=False):
        a = dict(attrs)
        if self.skip or (tag == "span" and "lang-switch" in (a.get("class") or "")):
            if tag not in VOID and not closed:
                self.skip += 1
            return
        if tag == "link" and "hreflang" in a:
            return
        if tag not in VOID and not closed:
            self.stack.append((tag, a))
        new = []
        for k, v in attrs:
            if v is not None:
                if k in TEXT_ATTRS:
                    v = self.tr(v)
                elif k in ("href", "src"):
                    v = self.relink(v)
                elif k == "content" and a.get("name") == "description":
                    v = self.tr(v)
                elif tag == "html" and k == "lang":
                    v = LANGS[self.lang][0]
            new.append((k, v))
        if new == attrs:
            self.out.append(self.get_starttag_text())
        else:
            self.emit_tag(tag, new, closed)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in VOID:
                self.skip -= 1
            return
        if tag == "head":
            for code, _, _ in SWITCH:
                self.out.append(f'  <link rel="alternate" hreflang="{LANGS[code][0]}" href="{href(code, self.page, self.lang)}">\n')
            if self.lang == "zh":
                self.out.append(f'  <link rel="stylesheet" href="{ZH_FONT}">\n')
        if tag == "nav" and self.stack and "nav" in (self.stack[-1][1].get("class") or "").split():
            self.out.append(self.switcher("  ") + "      ")
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        self.out.append(f"</{tag}>")

    def handle_data(self, d):
        if self.skip:
            return
        if self.stack and self.stack[-1][0] in ("script", "style"):
            self.out.append(d)
            return
        self.out.append(html.escape(self.tr(d), quote=False))


def render(page, lang, missing):
    src = (ROOT / page).read_text()
    # remove what an earlier run added, so the build is repeatable
    src = re.sub(r'\n[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", src)
    src = re.sub(r'\n[ \t]*<span class="lang-switch">.*?</span>', "", src)
    r = Rewriter(page, lang, missing)
    r.feed(src)
    r.close()
    return "".join(r.out)


def main():
    missing = set()
    for page in PAGES:
        english = render(page, "en", missing)
        (ROOT / page).write_text(english)
        for lang in ("fr", "zh"):
            out = ROOT / lang / page
            out.parent.mkdir(exist_ok=True)
            out.write_text(render(page, lang, missing))
    kept = sorted(missing)
    print(f"built {len(PAGES) * 2} pages; {len(kept)} strings kept as written:")
    print("\n".join("   " + k for k in kept))


if __name__ == "__main__":
    main()
