import csv

specs = [
    ("artifact-register.csv", 23),
    ("claims-register.csv", 11),
    ("relationship-register.csv", 12),
    ("person-register.csv", 16),
    ("search-log.csv", 13),
]
for name, expected in specs:
    with open(name, encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    bad = [(i + 1, len(r)) for i, r in enumerate(rows) if len(r) != expected]
    print(f"{name}: data rows={len(rows) - 1}, expected fields={expected}, bad={bad}")
