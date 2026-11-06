"""Проверка HTML-отчёта: структура, внутренние ссылки, кодировка."""
import collections
import sys

from lxml import html

path = sys.argv[1]
doc = html.parse(path)
root = doc.getroot()
ids = {e.get("id") for e in root.iter() if e.get("id")}
broken = []
for a in root.iter("a"):
    href = a.get("href") or ""
    if href.startswith("#") and len(href) > 1 and href[1:] not in ids:
        broken.append(href)
print("ids:", len(ids))
print("broken internal links:", broken)
print("title:", root.findtext(".//title"))
print("h2:", [h.text_content().strip() for h in root.iter("h2")])
print("tags:", collections.Counter(e.tag for e in root.iter()).most_common(10))
imgs = list(root.iter("img"))
print("images:", len(imgs))
