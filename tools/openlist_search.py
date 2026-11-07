import sys
import urllib.parse
import urllib.request
import re
import pathlib

OUT = pathlib.Path(r"A:\gen-tree\sources")
term = sys.argv[1]
name = sys.argv[2]
params = {"search": term, "fulltext": "1", "ns0": "1"}
url = "https://ru.openlist.wiki/index.php?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
raw = urllib.request.urlopen(req, timeout=60).read()
(OUT / f"raw-{name}.html").write_bytes(raw)
text = raw.decode("utf-8", "replace")
plain = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
plain = re.sub(r"<[^>]+>", " ", plain)
plain = re.sub(r"[ \t\r\f\v]+", " ", plain)
plain = re.sub(r"\n\s*\n+", "\n", plain)
(OUT / f"text-{name}.txt").write_text(plain, encoding="utf-8")
print(url, len(raw))
