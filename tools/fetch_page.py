import re
import sys
import urllib.parse
import urllib.request
import pathlib

OUT = pathlib.Path(r"A:\gen-tree\sources")


def get(url: str, name: str, headers: dict | None = None) -> str:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    (OUT / f"raw-{name}.html").write_bytes(raw)
    m = re.search(rb"charset=[\"']?([\w-]+)", raw[:3000])
    enc = m.group(1).decode().lower() if m else "utf-8"
    if enc in {"windows-1251"}:
        enc = "cp1251"
    text = raw.decode(enc, "replace")
    plain = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = re.sub(r"[ \t\r\f\v]+", " ", plain)
    plain = re.sub(r"\n\s*\n+", "\n", plain)
    (OUT / f"text-{name}.txt").write_text(plain, encoding="utf-8")
    return f"{url} -> {len(raw)} bytes, {len(plain)} text chars, enc={enc}"


if __name__ == "__main__":
    url, name = sys.argv[1], sys.argv[2]
    print(get(url, name))
