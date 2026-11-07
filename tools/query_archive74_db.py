import html as H
import re
import sys
import urllib.parse
import urllib.request
import pathlib

base = pathlib.Path(r"A:\gen-tree\sources")


def query(page: str, params: dict[str, str], slug: str):
    url = f"https://dbases.archive74.ru/{page}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=90).read()
    (base / f"raw-{slug}.html").write_bytes(raw)
    t = raw.decode("utf-8", "replace")
    total = re.search(r"(?:Найдено|Всего)[^<]{0,30}<[^>]*>\s*([\d\s\u00a0]+)", t)
    rows = []
    for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", t):
        cells = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"(?is)<td[^>]*>(.*?)</td>", tr)]
        if cells and any(cells):
            rows.append(cells)
    head = re.findall(r"(?is)<th[^>]*>(.*?)</th>", t)
    head = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip() for h in head]
    out = [f"URL: {url}", f"Всего (по разметке): {total.group(1).strip() if total else '?'}",
           f"Колонки: {' | '.join(head)}", f"Строк: {len(rows)}", ""]
    out += [" | ".join(r) for r in rows]
    (base / f"result-{slug}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(rows)


if __name__ == "__main__":
    page, slug = sys.argv[1], sys.argv[2]
    params = {}
    for arg in sys.argv[3:]:
        k, v = arg.split("=", 1)
        params[k] = v
    n = query(page, params, slug)
    print(f"{page}: {n} строк")
