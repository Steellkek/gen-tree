import re
import html as H
import urllib.parse
import urllib.request
import pathlib

OUT = pathlib.Path(r"A:\gen-tree\sources")
queries = ["Абзалутдинов", "Гилемов", "Миникаев", "Минимухамет"]
lines = []
for q in queries:
    url = "https://www.moypolk.ru/search/soldiers?" + urllib.parse.urlencode({"s": q})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=60).read()
    except Exception as exc:  # noqa: BLE001
        lines.append(f"### {q}: ОШИБКА {exc}")
        continue
    t = raw.decode("utf-8", "replace")
    (OUT / f"raw-moypolk-{q}.html").write_bytes(raw)
    cards = re.findall(r'(?is)<a[^>]+href="(/soldier/[^"]+)"[^>]*>(.*?)</a>', t)
    uniq = {}
    for href, inner in cards:
        text = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
        if text and href not in uniq:
            uniq[href] = text
    lines.append(f"### {q}: найдено ссылок {len(uniq)}")
    for href, text in list(uniq.items())[:20]:
        lines.append(f"  {text} — https://www.moypolk.ru{href}")
    lines.append("")
(OUT / "moypolk-results.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
