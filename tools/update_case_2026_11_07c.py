#!/usr/bin/env python3
"""Третье обновление: база ОГАЧО «Спецпереселенцы» и база «Награды Родины» — новые источники."""
from __future__ import annotations

import csv
import hashlib
import pathlib

CASE = pathlib.Path(__file__).resolve().parent.parent


def load(name):
    with (CASE / name).open(encoding="utf-8-sig", newline="") as h:
        r = csv.DictReader(h)
        return list(r.fieldnames or []), [{k: (v or "") for k, v in row.items()} for row in r]


def save(name, fields, rows):
    with (CASE / name).open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def upsert(rows, key, row):
    for e in rows:
        if e.get(key) == row[key]:
            e.update(row)
            return
    rows.append(row)


sha = hashlib.sha256((CASE / "sources" / "raw-settlers-Миникаев.html").read_bytes()).hexdigest() \
    if (CASE / "sources" / "raw-settlers-Миникаев.html").exists() else ""
if not sha:
    for p in (CASE / "sources").glob("raw-settlers-*.html"):
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        break

af, artifacts = load("artifact-register.csv")
upsert(artifacts, "artifact_id", {
    "artifact_id": "A-0032",
    "captured_at": "2026-11-07",
    "source_title": "База ОГАЧО «Спецпереселенцы»: Миникаевы, расселённые в Магнитогорске",
    "source_url_or_path": "https://dbases.archive74.ru/settlers?SettlersSearch%5Bsurname%5D=%D0%9C%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%D0%B5%D0%B2",
    "source_type": "архивная база данных (производная от документов о спецпоселенцах)",
    "repository_or_archive": "ГУ «Объединённый государственный архив Челябинской области» (ОГАЧО)",
    "archival_reference": "база «Спецпереселенцы» (citizens, выселенные на Южный Урал); выдача по фамилии Миникаев, 11 записей",
    "record_date": "2026-11-07 (просмотр)",
    "place_as_written": "Магнитогорский район, пос. Ново-Туковый; г. Магнитогорск, пос. Ново-Северный",
    "language_script": "русский, кириллица",
    "person_ids": "",
    "names_as_written": "Миникаев (Минекаев) Гаус; Миникаева (Минекаева) [Набира]; Миникаев Мингаз (1883); Миникаев Магсут (1916); Миникаева Халида (1897); Миникаева Фахры (1913); Миникаева Наиля (1919); Миникаева Лальминура (1921); Миникаева Саида (1924); Миникаев Акдес (1927); Миникаев Апас (1931)",
    "summary": "11 записей Миникаевых: Мингаз (1883) с семьёй — Магнитогорск, пос. Ново-Северный; Гаус и [Набира] — пос. Ново-Туковый. Хузнахмет (1898) и Салих (1926) в базе не найдены",
    "provenance_level": "архивная база, составленная по документам о спецпоселенцах",
    "directness": "indirect",
    "originality": "index",
    "independence_group": "IG-17-ARCHIVE74-SETTLERS",
    "legibility": "полная: таблица",
    "access_notes": "Открытый поиск по фамилии, 07.11.2026; страницы сохранены",
    "sha256": sha,
    "related_claim_ids": "C-0056; C-0057; C-0058",
    "reliability_notes": "База неполна (не все списки спецпоселенцев и не все районы); отсутствие записи не доказывает отсутствия человека. Год рождения указан не у всех",
    "status": "active",
})
save("artifact-register.csv", af, artifacts)

cf, claims = load("claims-register.csv")
for claim in [
    {
        "claim_id": "C-0056",
        "claim_text": "В Магнитогорске и Магнитогорском районе в базе ОГАЧО «Спецпереселенцы» значатся 11 Миникаевых: Мингаз (1883) с семьёй в пос. Ново-Северный и Гаус с [Набирой] в пос. Ново-Туковый",
        "subject_person_ids": "",
        "claim_type": "репрессия и расселение",
        "artifact_ids": "A-0032",
        "supporting_independence_groups": "IG-17-ARCHIVE74-SETTLERS",
        "contradicting_artifact_ids": "",
        "status": "single-source",
        "confidence": "средняя: архивная база, документы не просматривались",
        "rationale": "Записи базы подтверждают сам факт расселения Миникаевых в Магнитогорске как спецпоселенцев; к нашей линии прямо не привязаны",
        "next_action": "Сверить с делами № 15358 и № 15376 и с поселковыми списками Ново-Северного",
    },
    {
        "claim_id": "C-0057",
        "claim_text": "Хузнахмет (1898) и Салих (1926) Миникаевы в базе ОГАЧО «Спецпереселенцы» не значатся",
        "subject_person_ids": "P-0010; P-0016",
        "claim_type": "поиск (отрицательный результат)",
        "artifact_ids": "A-0032",
        "supporting_independence_groups": "IG-17-ARCHIVE74-SETTLERS",
        "contradicting_artifact_ids": "",
        "status": "unresolved",
        "confidence": "низкая: база неполна, отсутствие записи ничего не доказывает",
        "rationale": "Проверены написания Миникаев, Минекаев, Миникаева; в выдаче только семья Мингаза и запись Гауса. Возможны другие списки, другие написания или иной район высылки",
        "next_action": "Дело № 15358: место поселения семьи; запрос в ИЦ УВД Челябинской обл.",
    },
    {
        "claim_id": "C-0058",
        "claim_text": "Миникаевы из с. Кук-Тяка Азнакаевского района (Мингаз 1883, Акдас 1927, дело № 15734) — отдельная семья, не наша линия",
        "subject_person_ids": "",
        "claim_type": "исключение кандидата",
        "artifact_ids": "A-0030; A-0032",
        "supporting_independence_groups": "IG-07-OPENLIST-TATARSTAN; IG-17-ARCHIVE74-SETTLERS",
        "contradicting_artifact_ids": "",
        "status": "hypothesis",
        "confidence": "средняя: другая деревня, другое дело, другой состав семьи",
        "rationale": "Кук-Тяка и Фомкино — разные деревни разных районов; в семье Мингаза нет ни Хузнахмета, ни Салиха",
        "next_action": "Не разрабатывать без новых данных",
    },
]:
    upsert(claims, "claim_id", claim)
save("claims-register.csv", cf, claims)

sf, searches = load("search-log.csv")
upsert(searches, "search_id", {
    "search_id": "S-0036",
    "timestamp": "2026-11-07",
    "target_person_ids": "P-0010; P-0016; P-0017",
    "research_goal": "спецпоселенцы и раскулаченные Миникаевы, Абзалутдиновы, Гилемовы в Челябинской области",
    "query": "базы ОГАЧО: SettlersSearch[surname]=Миникаев/Минекаев/Миникаева/Абзалутдинов/Гилемов; DispossSearch[name1]=Миникаев",
    "language_locale": "ru",
    "source_or_domain": "dbases.archive74.ru (ОГАЧО: «Спецпереселенцы», «Раскулаченные»)",
    "filters": "фамилия, имя, место поселения",
    "result_status": "found",
    "artifact_ids": "A-0032",
    "blocker": "",
    "captcha_attempts": "0",
    "next_step": "Найдены 11 Миникаевых-спецпоселенцев в Магнитогорске (семья Мингаза, Гаус и Набира); наших Хузнахмета и Салиха нет — см. C-0057",
})
save("search-log.csv", sf, searches)
print("ok: artifacts", len(artifacts), "claims", len(claims), "searches", len(searches))
