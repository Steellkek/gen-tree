#!/usr/bin/env python3
"""Structural check of a GEDCOM 5.5.1 file against the parts this case relies on.

Checks: BOM, CRLF, line syntax, level steps, xref definition/resolution, record
termination, 255-byte line limit and the 5.5.1 header requirements.
It does not judge genealogical conclusions.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINE_RE = re.compile(r"^(\d+)(?: (@[^@]+@))? ([A-Z0-9_]+)(?: (.*))?$")
ALLOWED_HEADER_TAGS = {"SOUR", "DEST", "DATE", "SUBM", "FILE", "GEDC", "CHAR", "LANG", "PLAC", "NOTE", "COPR"}


def main(path: Path) -> int:
    data = path.read_bytes()
    errors: list[str] = []
    warnings: list[str] = []

    if not data.startswith(b"\xef\xbb\xbf"):
        errors.append("нет BOM в начале файла (5.5.1 для UTF-8 требует BOM)")
    if b"\r\n" not in data:
        errors.append("строки не завершаются CRLF")
    text = data.decode("utf-8-sig")

    lines = text.split("\r\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != "0 HEAD":
        errors.append("файл не начинается с '0 HEAD'")
    if not lines or lines[-1] != "0 TRLR":
        errors.append("файл не заканчивается '0 TRLR'")

    defined: dict[str, str] = {}
    referenced: list[tuple[int, str]] = []
    previous_level = 0
    in_head = False

    for number, line in enumerate(lines, start=1):
        if len(line.encode("utf-8")) > 255:
            errors.append(f"строка {number}: более 255 байт ({len(line.encode('utf-8'))})")
        match = LINE_RE.match(line)
        if not match:
            errors.append(f"строка {number}: неверный синтаксис: {line[:60]!r}")
            continue
        level = int(match.group(1))
        xref = match.group(2)
        tag = match.group(3)

        if level > previous_level + 1:
            errors.append(f"строка {number}: уровень {level} после {previous_level} (скачок)")
        previous_level = level

        if level == 0:
            if tag == "HEAD":
                in_head = True
                continue
            in_head = False
            if xref:
                if xref in defined:
                    errors.append(f"строка {number}: повторное определение {xref}")
                defined[xref] = tag
            elif tag != "TRLR":
                warnings.append(f"строка {number}: запись уровня 0 без xref ({tag})")
        elif in_head:
            if level == 1 and tag not in ALLOWED_HEADER_TAGS:
                warnings.append(f"строка {number}: необычный тег в HEAD: {tag}")
        value = (match.group(4) or "").strip()
        if value.startswith("@") and value.endswith("@") and level > 0:
            for token in value.split():
                if token.startswith("@") and token.endswith("@"):
                    referenced.append((number, token))

        if tag == "CHAR" and level == 1 and (match.group(4) or "").strip().upper() != "UTF-8":
            errors.append(f"строка {number}: CHAR={match.group(4)!r}, ожидалось UTF-8")

    if "@U1@" not in defined or defined.get("@U1@") != "SUBM":
        errors.append("нет записи SUBM с указателем @U1@")
    if not any(tag == "INDI" for tag in defined.values()):
        errors.append("нет ни одной записи INDI")

    for number, xref in referenced:
        if xref not in defined:
            errors.append(f"строка {number}: ссылка на неопределённый {xref}")

    # Каждая INDI/FAM должна иметь хотя бы одну ссылку (кроме изолированных записей).
    linked = {xref for _, xref in referenced}
    for xref, tag in defined.items():
        if tag in {"INDI", "FAM"} and xref not in linked:
            warnings.append(f"{xref} ({tag}) ни с чем не связана")

    counts: dict[str, int] = {}
    for tag in defined.values():
        counts[tag] = counts.get(tag, 0) + 1

    print(f"Файл: {path}")
    print(f"Строк: {len(lines)}; записей: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if errors:
        print("\nОШИБКИ:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\nПРЕДУПРЕЖДЕНИЯ:")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("Структурных ошибок и предупреждений нет.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
