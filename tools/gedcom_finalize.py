#!/usr/bin/env python3
"""Prepare the case GEDCOM for exchange: split long values with CONC, write BOM + CRLF.

GEDCOM 5.5.1 limits a line to 255 bytes (BOM included) and recommends shorter values.
Cyrillic text in UTF-8 takes two bytes per character, so the notes here exceed that.
This script keeps the same content and only adds CONC continuation lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

MAX_BYTES = 200  # safety margin under the 255-byte limit


def split_value(value: str, limit: int) -> list[str]:
    chunks: list[str] = []
    rest = value
    while len(rest.encode("utf-8")) > limit:
        cut = 0
        for index in range(1, len(rest) + 1):
            if len(rest[:index].encode("utf-8")) > limit:
                break
            cut = index
        head = rest[:cut]
        space = head.rfind(" ")
        if space > 0:
            head = head[:space]
            cut = space
        chunks.append(head)
        rest = rest[cut:].lstrip(" ")
    chunks.append(rest)
    return chunks


def main(path: Path) -> int:
    raw = path.read_text(encoding="utf-8-sig")
    out: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split(" ", 2)
        level = int(parts[0])
        if len(parts) < 2:
            out.append(line)
            continue
        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ""
        if not value or tag in {"CONC", "CONT"} or len(value.encode("utf-8")) <= MAX_BYTES:
            out.append(line.rstrip())
            continue
        chunks = split_value(value, MAX_BYTES)
        out.append(f"{level} {tag} {chunks[0]}".rstrip())
        for chunk in chunks[1:]:
            out.append(f"{level + 1} CONC {chunk}".rstrip())

    text = "\r\n".join(out) + "\r\n"
    path.write_text(text, encoding="utf-8-sig", newline="")
    print(f"Записано строк: {len(out)}; BOM + CRLF; {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
