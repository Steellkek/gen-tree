import re
import html as H
import urllib.parse
import urllib.request
import pathlib

OUT = pathlib.Path(r"A:\gen-tree\sources")
SLUGS = [
    "Миникаев_Хузахамет_(1903)",
    "Миникаева_Нафиса_(1915)",
    "Миникаева_Сауда_(1924)",
    "Миникаева_Салима_(1928)",
    "Миникаев_Анас_(1931)",
    "Миникаев_Анвар_(1941)",
    "Миникаева_Набира_(1933)",
    "Миникаева_Наиля_(1938)",
    "Миникаева_Асия_(1939)",
    "Миникаев_Амер_(1935)",
    "Миникаева_Нурия_Гаясовна_(1938)",
]
FIELDS = ["Дата рождения", "Место рождения", "Варианты ФИО", "Место проживания", "Обвинение",
          "Осуждение", "Осудивший орган", "Приговор", "Место отбывания", "Дата реабилитации", "Архивное дело"]

lines = []
for slug in SLUGS:
    url = "https://ru.openlist.wiki/" + urllib.parse.quote(slug)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=60).read()
    except Exception as exc:  # noqa: BLE001
        lines.append(f"### {slug}\nОШИБКА: {exc}\n")
        continue
    text = raw.decode("utf-8", "replace")
    body = text.split('<div id="mw-content-text"', 1)[-1]
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", body)
    plain = H.unescape(re.sub(r"<[^>]+>", " ", body))
    plain = re.sub(r"[ \t\r\f\v]+", " ", plain)
    plain = re.sub(r"\n\s*\n+", "\n", plain)
    cut = plain.find("Помочь проекту")
    if cut > 0:
        plain = plain[:cut]
    flat = re.sub(r"\s+", " ", plain)
    lines.append(f"### {slug}")
    for f in FIELDS:
        m = re.search(re.escape(f) + r":\s*(.+?)(?=\s(?:Дата рождения|Место рождения|Варианты ФИО|Место проживания|Обвинение|Осуждение|Осудивший орган|Приговор|Место отбывания|Дата реабилитации|Архивное дело|Источники данных):| Биография|$)", flat)
        if m:
            lines.append(f"  {f}: {m.group(1).strip()}")
    lines.append("")

(OUT / "openlist-cards2.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok", len(SLUGS))
