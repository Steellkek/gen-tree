#!/usr/bin/env python3
"""Пересобрать многострочные значения GEDCOM (NOTE + CONC) без потери пробелов.

Причина: разбиение длинного значения на CONC-строки часто теряет пробел на стыке,
и после склейки получается «в древоне включены». Скрипт склеивает цепочку,
восстанавливает пробелы на стыках и заново переносит по словам, оставляя пробел
в конце перенесённой строки (так требует конкатенация GEDCOM). Пишет BOM + CRLF.

    python tools/gedcom_reflow.py gen-tree.ged

Содержание не меняется: только переносы строк и восстановленные пробелы на стыках.
"""
from __future__ import annotations

import sys
from pathlib import Path

MAX_BYTES = 220  # с запасом до предела 255 байт


def join_chain(value: str, parts: list[str]) -> str:
    text = value
    for part in parts:
        if not text or not part:
            continue
        if text.endswith((" ", "\t")) or part.startswith((" ", "\t")):
            text += part
        else:
            text += " " + part
    return text


def wrap(prefix: str, text: str, cont_prefix: str) -> list[str]:
    lines: list[str] = []
    words = text.split()
    current = ""
    for word in words:
        candidate = f"{current} {word}" if current else word
        if current and len((prefix + candidate + " ").encode("utf-8")) > MAX_BYTES:
            lines.append((prefix + current + " ").rstrip("\r\n"))
            current = word
        else:
            current = candidate
    if current:
        lines.append(prefix + current)
    if not lines:
        lines.append(prefix.rstrip())
    return [lines[0]] + [cont_prefix + line[len(prefix):] for line in lines[1:]]


def main(path: Path) -> int:
    raw = path.read_text(encoding="utf-8-sig")
    out: list[str] = []
    i = 0
    lines = raw.splitlines()
    rewrapped = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        parts = line.split(" ", 2)
        if len(parts) < 3:
            out.append(line.rstrip())
            i += 1
            continue
        level, tag, value = int(parts[0]), parts[1], parts[2]
        if tag in {"CONC", "CONT"}:
            # Осиротевшая строка продолжения: оставить как есть.
            out.append(line.rstrip())
            i += 1
            continue
        chain: list[str] = []
        j = i + 1
        while j < len(lines):
            nxt = lines[j].split(" ", 2)
            if len(nxt) >= 2 and nxt[0] == str(level + 1) and nxt[1] == "CONC":
                chain.append(nxt[2] if len(nxt) > 2 else "")
                j += 1
            else:
                break
        if not chain:
            out.append(line.rstrip())
            i += 1
            continue
        text = join_chain(value, chain)
        out.extend(wrap(f"{level} {tag} ", text, f"{level + 1} CONC "))
        rewrapped += 1
        i = j

    path.write_text("\r\n".join(out) + "\r\n", encoding="utf-8-sig", newline="")
    print(f"Пересобрано значений: {rewrapped}; строк: {len(out)}; BOM + CRLF; {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
