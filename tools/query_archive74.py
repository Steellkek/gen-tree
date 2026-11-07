#!/usr/bin/env python3
"""Запрос к базе ОГАЧО «Награды Родины» (dbases.archive74.ru/worker).

Форма поиска — GET с параметрами WorkerFilter[name1..3], district, city,
work_place, reward_id. Страница отдаётся в cp1251.
Результат пишется в sources/result-<slug>.txt (UTF-8), HTML страницы — рядом.
"""
from __future__ import annotations

import html
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://dbases.archive74.ru/worker"
OUT = Path(__file__).resolve().parent.parent / "sources"
OUT.mkdir(exist_ok=True)


def fetch(params: dict[str, str]) -> tuple[str, str, bytes]:
    url = BASE + "?" + urllib.parse.urlencode(params)
    raw = urllib.request.urlopen(url, timeout=90).read()
    m = re.search(rb"charset=[\"']?([\w-]+)", raw[:2000])
    enc = (m.group(1).decode("ascii").lower() if m else "utf-8")
    if enc in {"windows-1251", "cp1251"}:
        enc = "cp1251"
    return url, raw.decode(enc, "replace"), raw


def parse(text: str) -> tuple[str, list[list[str]], list[str]]:
    m = re.search(r"Найдено записей:\s*(?:<[^>]+>\s*)*([\d\s\u00a0]+)", text)
    total = m.group(1).strip() if m else ("0" if "Ничего не найдено" in text else "?")
    rows = []
    for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", text):
        cells = [
            html.unescape(re.sub(r"<[^>]+>", " ", c)).strip()
            for c in re.findall(r"(?is)<td[^>]*>(.*?)</td>", tr)
        ]
        if cells and not cells[0].startswith("Фамилия"):
            rows.append(cells)
    pages = sorted({int(p) for p in re.findall(r"[?&]page=(\d+)", text)})
    return total.replace("\u00a0", " "), rows, [str(p) for p in pages]


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: query_archive74.py 'Фамилия' [Имя] [Отчество] [--city=...] [--page=N]")
        return 2
    params: dict[str, str] = {}
    free: list[str] = []
    city = None
    page = None
    for arg in args:
        if arg.startswith("--city="):
            city = arg.split("=", 1)[1]
        elif arg.startswith("--page="):
            page = arg.split("=", 1)[1]
        elif arg.startswith("--name1="):
            params["WorkerFilter[name1]"] = arg.split("=", 1)[1]
        elif arg.startswith("--name2="):
            params["WorkerFilter[name2]"] = arg.split("=", 1)[1]
        else:
            free.append(arg)
    for key, value in zip(("name1", "name2", "name3"), free):
        params[f"WorkerFilter[{key}]"] = value
    if city:
        params["WorkerFilter[city]"] = city
    if page:
        params["page"] = page

    label_parts = [f"{k.split('[')[1].rstrip(']')}={v}" for k, v in params.items()]
    slug = re.sub(r"[^0-9A-Za-zА-Яа-яЁё_.-]+", "_", "_".join(label_parts))[:80]

    url, text, raw = fetch(params)
    (OUT / f"archive74-{slug}.html").write_bytes(raw)
    total, rows, pages = parse(text)
    lines = [
        f"URL: {url}",
        f"Запрос: {'; '.join(label_parts)}",
        f"Найдено записей: {total}; строк: {len(rows)}; страницы: {','.join(pages) or '—'}",
        "",
        "Фамилия | Имя | Отчество | Район | Город | Место работы | Награда | Дата",
    ]
    lines += [" | ".join(r) for r in rows]
    out = OUT / f"result-{slug}.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Записано: {out} (строк: {len(rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
