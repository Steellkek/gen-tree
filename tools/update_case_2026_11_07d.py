#!/usr/bin/env python3
"""Четвёртое обновление: фотографии надгробий (07.11.2026)."""
from __future__ import annotations

import csv
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


MONUMENTS = [
    dict(
        artifact_id="A-0033", file="photos/01-minikaev-farit-1952-2013.jpg",
        sha="dfeebf9b8b8c078caf8d323eca8812b02cb507ecd927cfaa52b1063f18641631",
        title="Фотография надгробия: Миникаев Фарит Салихович",
        person="P-0004", names="Миникаев Фарит Салихович",
        text="Миникаев / Фарит / Салихович / 17.12.1952 - 04.11.2013",
        place="Левобережное кладбище, г. Магнитогорск",
        legibility="полная: чёрный гранит, читается уверенно",
        note="Памятник с портретом и полумесяцем; установлен после 2013 г.",
        claims="C-0037; C-0060",
    ),
    dict(
        artifact_id="A-0034", file="photos/02-minikaev-salih-1926-1997.jpg",
        sha="3691c297f7705be7f23a7b2244e288715b4ef1973e06b2be83b583d0973746db",
        title="Фотография надгробия: Миникаев Салих Хузиахметович",
        person="P-0016", names="Миникаев Салих Хузиахметович",
        text="МИНИКАЕВ / САЛИХ / ХУЗИАХМЕТОВИЧ / 20 11 1926 — 2 6 1997",
        place="Ново-Северное кладбище, г. Магнитогорск",
        legibility="полная: белый камень, буквы читаются",
        note="Отчество на памятнике — «Хузиахметович», как в индексе МВД РТ; на фото видна только лицевая плита",
        claims="C-0038; C-0045; C-0059; C-0060",
    ),
    dict(
        artifact_id="A-0035", file="photos/03-minikaev-khuznakhmet-1898-1969.jpg",
        sha="5e6434f6657b8b76911f998ee5568b3a42cddeb649621880c4f0a3719f0ea651",
        title="Фотография надгробия: Миникаев Хузнахмәт Миникай углы",
        person="P-0010", names="МИНИКАЕВ Хузнахмәт Миникай углы",
        text="МИНИКАЕВ / Хузнахмәт Миникай углы / 04.01.1898 / 19.10.1969",
        place="Ново-Северное кладбище, г. Магнитогорск",
        legibility="полная: металлическая табличка на камне, читается",
        note="Татарская форма патронима «Миникай углы» и «ә» в имени; даты совпадают с семейным сообщением",
        claims="C-0039; C-0060; C-0061; C-0062",
    ),
    dict(
        artifact_id="A-0036", file="photos/04-abzalutdinov-nurmuhamed-1950-2014.jpg",
        sha="562629a1b9a61850ee37b9f2902ef412fd2a46805acd06e87a43db73759eeac3",
        title="Фотография надгробия: Абзалутдинов Нурмухамет Минимухаметович",
        person="P-0005", names="Абзалутдинов Нурмухамет Минимухаметович",
        text="АБЗАЛУТДИНОВ / НУРМУХАМЕТ / МИНИМУХАМЕТОВИЧ / 25.8.1950 - 7.8.2014",
        place="Левобережное кладбище, г. Магнитогорск",
        legibility="полная: белый камень, рельефные буквы читаются",
        note="Даты совпадают с семейным сообщением",
        claims="C-0040; C-0060",
    ),
    dict(
        artifact_id="A-0037", file="photos/05-abzalutdinov-minimuhamed-1924-2016.jpg",
        sha="fd192054926e64bfda924d424c6afb0cf8bdddbef3c005fca5dd26fd14f45326",
        title="Фотография надгробия: Абзалутдинов Минимухамет Габдулович",
        person="P-0017", names="[надпись не прочитана]",
        text="[неразборчиво]: четыре строки рельефного текста, выветрены и засняты с большого расстояния",
        place="Левобережное кладбище, г. Магнитогорск",
        legibility="неразборчиво: при увеличении и усилении контраста буквы не восстанавливаются",
        note="Нужен крупный план при рассеянном свете; надпись предположительно того же типа, что у соседних памятников",
        claims="C-0060",
    ),
    dict(
        artifact_id="A-0038", file="photos/06-gilemov-aknaf-1926-1976.jpg",
        sha="143d187fdfa070146f46934bc3fbde46cbe273ed8a52509259684e5092019f95",
        title="Фотография надгробия: Гилемов Ахнаф Гилемович",
        person="P-0008", names="ГИЛЕМОВ Ахнаф Гилемович",
        text="ГИЛЕМОВ / Ахнаф Гилемович / 19 XI 26 — 25 I 76",
        place="Левобережное кладбище, г. Магнитогорск",
        legibility="полная: овальная белая табличка, римские цифры месяцев",
        note="19 ноября 1926 — 25 января 1976; даты совпадают с семейным сообщением",
        claims="C-0049; C-0060",
    ),
    dict(
        artifact_id="A-0039", file="photos/07-gilemova-zulfia-1926-2002.jpg",
        sha="82fc1be20c12db07a59442daf0e979df51761aaf3f5da285a5f724a7d6421018",
        title="Фотография надгробия: Гилемова Зульхия Закиевна",
        person="P-0018", names="ГИЛЕМОВА Зульхия Закиевна",
        text="ГИЛЕМОВА / ЗУЛЬХИЯ / ЗАКИЕВНА / 15.8.1926 - 22.6.2002",
        place="Левобережное кладбище, г. Магнитогорск",
        legibility="полная: рельефные буквы, читаются",
        note="Даты совпадают с семейным сообщением",
        claims="C-0043; C-0060",
    ),
]

af, artifacts = load("artifact-register.csv")
for m in MONUMENTS:
    upsert(artifacts, "artifact_id", {
        "artifact_id": m["artifact_id"],
        "captured_at": "2026-11-07",
        "source_title": m["title"],
        "source_url_or_path": m["file"],
        "source_type": "фотография надгробия",
        "repository_or_archive": "семейный архив пользователя; фото передано в чате 07.11.2026",
        "archival_reference": "надпись на памятнике; место захоронения указано пользователем",
        "record_date": "2026-11-07 (съёмка); памятник установлен после смерти",
        "place_as_written": m["place"],
        "language_script": "русский, кириллица" + ("; татарская орфография" if m["artifact_id"] == "A-0035" else ""),
        "person_ids": m["person"],
        "names_as_written": m["names"],
        "summary": m["text"],
        "provenance_level": "фотография, сделанная семьёй; надпись читается с оригинала",
        "directness": "indirect",
        "originality": "original",
        "independence_group": "IG-18-GRAVE-MONUMENTS",
        "legibility": m["legibility"],
        "access_notes": "Получено в чате 07.11.2026; оригинал сохранён, нормализованная копия совпала по sha256",
        "sha256": m["sha"],
        "related_claim_ids": m["claims"],
        "reliability_notes": m["note"] + " Надпись сделана после смерти и может опираться на те же семейные сведения, поэтому независимость от рассказа ограничена.",
        "status": "active",
    })
save("artifact-register.csv", af, artifacts)

pf, persons = load("person-register.csv")
burials = {
    "P-0004": "Левобережное кладбище, г. Магнитогорск",
    "P-0005": "Левобережное кладбище, г. Магнитогорск",
    "P-0008": "Левобережное кладбище, г. Магнитогорск",
    "P-0010": "Ново-Северное кладбище, г. Магнитогорск",
    "P-0016": "Ново-Северное кладбище, г. Магнитогорск",
    "P-0017": "Левобережное кладбище, г. Магнитогорск",
    "P-0018": "Левобережное кладбище, г. Магнитогорск",
}
for pid, place in burials.items():
    for p in persons:
        if p["person_id"] == pid:
            p["places"] = (p["places"] + "; " if p["places"] else "") + f"похоронен: {place}" if "похорон" not in p["places"] else p["places"]
            p["source_artifact_ids"] = p["source_artifact_ids"] + "; " + {
                "P-0004": "A-0033", "P-0005": "A-0036", "P-0008": "A-0038",
                "P-0010": "A-0035", "P-0016": "A-0034", "P-0017": "A-0037", "P-0018": "A-0039",
            }[pid]
save("person-register.csv", pf, persons)

cf, claims = load("claims-register.csv")
updates = {
    "C-0037": {
        "artifact_ids": "A-0017; A-0033",
        "status": "corroborated",
        "confidence": "высокая: семейное сообщение и надпись на памятнике",
        "rationale": "Даты 17.12.1952–04.11.2013 совпадают у семьи и на надгробии (A-0033); документы ЗАГС не проверялись",
    },
    "C-0038": {
        "artifact_ids": "A-0017; A-0034",
        "status": "corroborated",
        "confidence": "высокая: семейное сообщение и надпись на памятнике",
        "rationale": "Даты 20.11.1926–02.06.1997 совпадают у семьи и на надгробии (A-0034)",
    },
    "C-0040": {
        "artifact_ids": "A-0017; A-0036",
        "status": "corroborated",
        "confidence": "высокая: семейное сообщение и надпись на памятнике",
        "rationale": "Даты 25.08.1950–07.08.2014 совпадают у семьи и на надгробии (A-0036)",
    },
    "C-0043": {
        "artifact_ids": "A-0017; A-0020; A-0039",
        "status": "corroborated",
        "confidence": "высокая: семейное сообщение, архивная запись о награде и надгробие",
        "rationale": "Даты 15.08.1926–22.06.2002 совпадают у семьи и на надгробии; запись о медали материнства 1965 г. подтверждает существование человека в Магнитогорске",
    },
    "C-0049": {
        "artifact_ids": "A-0017; A-0038",
        "status": "corroborated",
        "confidence": "высокая: семейное сообщение и надпись на памятнике",
        "rationale": "Даты 19.11.1926–25.01.1976 совпадают у семьи и на табличке (A-0038)",
    },
    "C-0041": {
        "rationale": "Даты сообщены внуком; надгробие (A-0037) не читается, поэтому подтвердить их второй цепочкой пока нельзя",
    },
    "C-0039": {
        "rationale": "Даты 04.01.1898–19.10.1969 сообщены внуком и совпадают с надгробием (A-0035), но индекс МВД РТ даёт 1893 — расхождение вынесено в C-0026; поэтому статус остаётся single-source",
    },
    "C-0045": {
        "artifact_ids": "A-0009; A-0017; A-0031; A-0034",
        "rationale": "Две независимые цепочки: запись индекса и семья. Надпись на памятнике (A-0034) даёт отчество «Хузиахметович» — то же, что в индексе; совпадают имя, год, деревня и сценарий ссылки",
    },
}
for cid, patch in updates.items():
    upsert(claims, "claim_id", {"claim_id": cid, **patch})

NEW = [
    {
        "claim_id": "C-0059",
        "claim_text": "Надгробие Салиха даёт отчество «Хузиахметович» — то же написание, что в индексе МВД РТ",
        "subject_person_ids": "P-0016",
        "claim_type": "надпись на памятнике",
        "artifact_ids": "A-0009; A-0034",
        "supporting_independence_groups": "IG-07-OPENLIST-TATARSTAN; IG-18-GRAVE-MONUMENTS",
        "contradicting_artifact_ids": "",
        "status": "corroborated",
        "confidence": "высокая: два независимых носителя",
        "rationale": "Индекс и памятник независимо пишут «Хузиахметович»; семья называет отца Хузнахметом — это варианты одного имени",
        "next_action": "Сверить с записью о рождении 1926 г. в Фомкино",
    },
    {
        "claim_id": "C-0060",
        "claim_text": "Места захоронения: Хузнахмет и Салих — Ново-Северное кладбище Магнитогорска; Фарит, Нурмухамет, Минимухамет, Зульхия и Ахнаф — Левобережное кладбище Магнитогорска",
        "subject_person_ids": "P-0004; P-0005; P-0008; P-0010; P-0016; P-0017; P-0018",
        "claim_type": "место захоронения",
        "artifact_ids": "A-0033; A-0034; A-0035; A-0036; A-0037; A-0038; A-0039",
        "supporting_independence_groups": "IG-18-GRAVE-MONUMENTS",
        "contradicting_artifact_ids": "",
        "status": "single-source",
        "confidence": "высокая: фотографии памятников и указание пользователя",
        "rationale": "Кладбища указаны пользователем и видны на снимках (оградки, ландшафт); разделение на два кладбища отражает два периода жизни семьи",
        "next_action": "При возможности снять номер участка и проверить по книге регистрации захоронений",
    },
    {
        "claim_id": "C-0061",
        "claim_text": "Надгробие Хузнахмета записано по-татарски: «Хузнахмәт Миникай углы»",
        "subject_person_ids": "P-0010",
        "claim_type": "надпись на памятнике",
        "artifact_ids": "A-0035",
        "supporting_independence_groups": "IG-18-GRAVE-MONUMENTS",
        "contradicting_artifact_ids": "",
        "status": "single-source",
        "confidence": "высокая: надпись читается",
        "rationale": "Памятник воспроизводит ту форму, которой семья называет прапрадеда; это подтверждает татарское написание патронима",
        "next_action": "Не требует проверки",
    },
    {
        "claim_id": "C-0062",
        "claim_text": "Даты на надгробии Хузнахмета (04.01.1898–19.10.1969) совпадают с семейным сообщением",
        "subject_person_ids": "P-0010",
        "claim_type": "сверка надписи и свидетельства",
        "artifact_ids": "A-0017; A-0035",
        "supporting_independence_groups": "IG-15-INTERVIEW-6; IG-18-GRAVE-MONUMENTS",
        "contradicting_artifact_ids": "",
        "status": "corroborated",
        "confidence": "высокая: надпись и рассказ независимы по носителю",
        "rationale": "Совпадение полное; при этом индекс МВД РТ даёт 1893, поэтому абсолютная дата остаётся под вопросом (C-0026)",
        "next_action": "Метрическая книга Фомкино за 1898 г.",
    },
]
for claim in NEW:
    upsert(claims, "claim_id", claim)
save("claims-register.csv", cf, claims)

print("artifacts:", len(artifacts), "persons:", len(persons), "claims:", len(claims))
