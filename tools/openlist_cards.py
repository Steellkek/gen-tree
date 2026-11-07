import sys
import re
import html as H
import urllib.parse
import urllib.request
import pathlib

OUT = pathlib.Path(r"A:\gen-tree\sources")
SLUGS = [
    "Миникаев_Гаяз_(1908)",
    "Миникаев_Акдас_Мингазеевич_(1927)",
    "Миникаев_Салих_Хузиахметович_(1926)",
    "Миникаев_Хузиахмет_(1893)",
    "Миникаев_Амир_Гаязович_(1946)",
    "Миникаев_Зуфер_Гаязович_(1943)",
    "Миникаев_Минсалих_(1926)",
    "Миникаева_Насима_Гаязовна_(1940)",
]

lines = []
for slug in SLUGS:
    url = "https://ru.openlist.wiki/" + urllib.parse.quote(slug)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=60).read()
    except Exception as exc:  # noqa: BLE001
        lines.append(f"### {slug}\nОШИБКА: {exc}\n")
        continue
    (OUT / f"openlist-{re.sub(r'[^0-9A-Za-zА-Яа-яЁё_-]+', '_', slug)}.html").write_bytes(raw)
    text = raw.decode("utf-8", "replace")
    body = text.split("<div id=\"mw-content-text\"", 1)[-1]
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", body)
    plain = H.unescape(re.sub(r"<[^>]+>", " ", body))
    plain = re.sub(r"[ \t\r\f\v]+", " ", plain)
    plain = re.sub(r"\n\s*\n+", "\n", plain)
    # обрезаем хвост с навигацией
    cut = plain.find("Помочь проекту")
    if cut > 0:
        plain = plain[:cut]
    lines.append(f"### {slug}\n{plain[:3000]}\n")

(OUT / "openlist-cards.txt").write_text("\n".join(lines), encoding="utf-8")
print("cards:", len(SLUGS))
