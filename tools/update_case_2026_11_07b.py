#!/usr/bin/env python3
"""Второе обновление реестров gen-tree: уточнения от 07.11.2026 (A-0031).

Меняет: имя прадеда (Салих, не Салик), статус тождества с индексом, статус
«Зульхия — мать Рамзии», вопрос о годе рождения. Добавляет A-0031 и C-0053–C-0055.
"""
from __future__ import annotations

import csv
from pathlib import Path

CASE = Path(__file__).resolve().parent.parent


def load(name: str):
    with (CASE / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [{k: (v or "") for k, v in row.items()} for row in reader]


def save(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (CASE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def upsert(rows, key, row):
    for existing in rows:
        if existing.get(key) == row[key]:
            existing.update(row)
            return
    rows.append(row)


# ---------------------------------------------------------------- артефакт
af, artifacts = load("artifact-register.csv")
upsert(artifacts, "artifact_id", {
    "artifact_id": "A-0031",
    "captured_at": "2026-11-07",
    "source_title": "Седьмое сообщение пользователя: уточнения к шестому (дословная запись)",
    "source_url_or_path": "input/interview-2026-11-07-7.md",
    "source_type": "устное свидетельство / уточнение",
    "repository_or_archive": "дело gen-tree (локальный файл)",
    "archival_reference": "",
    "record_date": "2026-11-07",
    "place_as_written": "—",
    "language_script": "русский, кириллица",
    "person_ids": "P-0001; P-0010; P-0016; P-0018",
    "names_as_written": "Салих; Зульхия; Рамзия",
    "summary": "Ответы на вопросы отчёта: (1) список предков относится к линии Артура; (2) Зульхия — мама Рамзии; (3) документов пока нет; (4) «Салик» — опечатка, имя прадеда Салих",
    "provenance_level": "первичный информант, уточнение к A-0017",
    "directness": "direct",
    "originality": "original",
    "independence_group": "IG-15-INTERVIEW-6",
    "legibility": "полная: текст",
    "access_notes": "Получено в чате 07.11.2026",
    "sha256": "67e383f42b7c8c6e7b76f3369a93bbf45037838a1009d42e71bfd632d62eba3b",
    "related_claim_ids": "C-0025; C-0038; C-0044; C-0045; C-0046; C-0053; C-0054; C-0055",
    "reliability_notes": "Тот же информант, что A-0017: доказательной независимости не добавляет, но снимает неоднозначность прочтения",
    "status": "active",
})
save("artifact-register.csv", af, artifacts)

# ---------------------------------------------------------------- лица
pf, persons = load("person-register.csv")
upsert(persons, "person_id", {
    "person_id": "P-0016",
    "preferred_label": "Миникаев Салих Хузнахметович (1926–1997)",
    "names_as_written": "Миникаев Салих Хузнахметович",
    "normalized_name_variants": "Салих Хузнахметович Миникаев; Салик (опечатка в шестом сообщении, исправлена в A-0031); Салих Хузиахметович (в индексе МВД РТ)",
    "source_artifact_ids": "A-0017; A-0031",
    "merge_or_split_rationale": "Полное имя, даты и место в цепочке — из шестого сообщения; имя исправлено на «Салих» седьмым сообщением. Отождествление с записью индекса «Салих Хузиахметович (1926)» — C-0045 (подкреплено двумя цепочками), но P-0013 сохранён отдельно до дела № 15358",
    "notes": "Прадед по отцу, отец Фарита Салиховича. Если тождество с делом № 15358 подтвердится, он был выслан ребёнком в 1931 г. вместе с отцом.",
})
upsert(persons, "person_id", {
    "person_id": "P-0013",
    "notes": "Запись индекса МВД РТ. Совпадает с P-0016 по имени (Салих), отчеству в варианте, году, деревне и ссылке — C-0045; не слит до получения дела № 15358.",
})
save("person-register.csv", pf, persons)

# ---------------------------------------------------------------- утверждения
cf, claims = load("claims-register.csv")
updates = {
    "C-0025": {
        "claim_text": "Семья Миникаевых происходит из с. Фомкино Октябрьского (ныне Нурлатского) района ТАССР и была выслана оттуда в Челябинскую область в 1931 г.",
        "artifact_ids": "A-0008; A-0009; A-0011; A-0017; A-0023; A-0031",
        "supporting_independence_groups": "IG-07-OPENLIST-TATARSTAN; IG-09-TATARICA; IG-15-INTERVIEW-6",
        "status": "corroborated",
        "confidence": "высокая: две независимые цепочки, совпадают имя, отчество в варианте, год, деревня и сценарий ссылки",
        "rationale": "После уточнения имени (Салих, A-0031) запись индекса «Салих Хузиахметович (1926)» совпадает с прадедом по всем признакам, кроме года его отца; семейное предание о ссылке из Татарстана совпадает с делом № 15358. Документ, называющий Фарита сыном Салиха, не найден",
        "next_action": "Дело ИЦ УВД Челябинской обл. № 15358: состав семьи и место поселения",
    },
    "C-0026": {
        "claim_text": "Год рождения главы семьи: 04.01.1898 по семье против 1893 в индексе МВД РТ (и 1903 в соседнем деле № 15376)",
        "artifact_ids": "A-0007; A-0008; A-0017; A-0026",
        "supporting_independence_groups": "IG-06-INTERVIEW-3; IG-07-OPENLIST-TATARSTAN; IG-15-INTERVIEW-6",
        "status": "unresolved",
        "confidence": "низкая: три разных года для одного имени",
        "rationale": "Тождество лиц подкреплено (C-0046), но дата рождения расходится: семья помнит 04.01.1898, индекс даёт 1893, соседнее дело — 1903. Ошибка может быть и в семье, и в деле",
        "next_action": "Метрическая книга Фомкино за 1898 г.; отчество и год главы в деле № 15358",
    },
    "C-0038": {
        "claim_text": "Миникаев Салих Хузнахметович, прадед по отцу, родился 20.11.1926 и умер 02.06.1997",
        "artifact_ids": "A-0017; A-0031",
        "supporting_independence_groups": "IG-15-INTERVIEW-6",
        "confidence": "высокая для семейного свидетельства",
        "rationale": "Сообщено внуком; имя уточнено седьмым сообщением («Салик» — опечатка). Запись о рождении 1926 г. в Фомкино не найдена",
        "next_action": "Метрическая книга Фомкино 1926 г.; дело № 15358",
    },
    "C-0044": {
        "claim_text": "Зульхия Закиевна Гилемова — мать Рамзии Ахнафовны",
        "artifact_ids": "A-0017; A-0031",
        "supporting_independence_groups": "IG-15-INTERVIEW-6",
        "status": "single-source",
        "confidence": "высокая для семейного свидетельства",
        "rationale": "Прямое подтверждение субъекта: «Зульхия — мама Рамзии». Прежде вывод держался только на фамилии и паре с Ахнафом",
        "next_action": "Запись о рождении Рамзии 1953 г.: родители",
    },
    "C-0045": {
        "claim_text": "Миникаев Салих Хузнахметович (1926–1997) — тот же человек, что Миникаев Салих Хузиахметович (1926) из дела № 15358",
        "artifact_ids": "A-0009; A-0017; A-0031",
        "supporting_independence_groups": "IG-07-OPENLIST-TATARSTAN; IG-15-INTERVIEW-6",
        "status": "corroborated",
        "confidence": "высокая: совпадают имя, отчество в варианте, год, деревня и сценарий ссылки",
        "rationale": "Две независимые цепочки (индекс МВД РТ и семья). После уточнения имени совпадение полное, кроме варианта отчества; документ, связывающий запись с Фаритом, ещё не получен",
        "next_action": "Дело № 15358: состав семьи и возраст детей",
    },
    "C-0046": {
        "claim_text": "Миникаев Хузнахмет Миникаевич (1898–1969) — тот же человек, что Миникаев Хузиахмет (1893) из дела № 15358",
        "artifact_ids": "A-0008; A-0017; A-0026; A-0031",
        "supporting_independence_groups": "IG-07-OPENLIST-TATARSTAN; IG-15-INTERVIEW-6",
        "status": "corroborated",
        "confidence": "средняя: тождество подкреплено, год рождения — нет",
        "rationale": "Если Салих из индекса — прадед (C-0045), то его отец в деле носит имя Хузиахмет, то есть Хузнахмет; связь подтверждается со стороны сына. Расхождение годов вынесено в C-0026",
        "next_action": "Метрическая книга Фомкино 1898 г.; дело № 15358",
    },
}
for cid, patch in updates.items():
    upsert(claims, "claim_id", {"claim_id": cid, **patch})

NEW = [
    {
        "claim_id": "C-0053",
        "claim_text": "Список предков из шестого сообщения относится к линии Артура Альбертовича, а не к линии супруги",
        "subject_person_ids": "P-0001",
        "claim_type": "атрибуция записи",
        "artifact_ids": "A-0017; A-0031",
        "supporting_independence_groups": "IG-15-INTERVIEW-6",
        "contradicting_artifact_ids": "",
        "status": "single-source",
        "confidence": "высокая: прямое подтверждение субъекта",
        "rationale": "Субъект подтвердил, что родословная — его; это согласуется с именами родителей (Альфия Нурмухаметовна, Альберт Фаритович)",
        "next_action": "Не требует проверки",
    },
    {
        "claim_id": "C-0054",
        "claim_text": "Имя прадеда по отцу — Салих; написание «Салик» в шестом сообщении было опечаткой",
        "subject_person_ids": "P-0016",
        "claim_type": "имя",
        "artifact_ids": "A-0017; A-0031",
        "supporting_independence_groups": "IG-15-INTERVIEW-6",
        "contradicting_artifact_ids": "",
        "status": "single-source",
        "confidence": "высокая: исправление самого информанта",
        "rationale": "Информант прямо указал на опечатку; вариант «Салих» совпадает с записью индекса МВД РТ",
        "next_action": "Сверить с записью о рождении 1926 г.",
    },
    {
        "claim_id": "C-0055",
        "claim_text": "Ахнаф Гилемович Гилемов и Зульхия Закиевна Гилемова — супруги",
        "subject_person_ids": "P-0008; P-0018",
        "claim_type": "брак",
        "artifact_ids": "A-0017",
        "supporting_independence_groups": "IG-15-INTERVIEW-6",
        "contradicting_artifact_ids": "",
        "status": "hypothesis",
        "confidence": "средняя: пара родителей Рамзии, но брак прямо не назван",
        "rationale": "Подтверждено только материнство Зульхии (C-0044); то, что Ахнаф — её муж, следует из общей фамилии и из того, что оба названы прадедом и прабабушкой",
        "next_action": "Запись о рождении Рамзии 1953 г.: оба родителя",
    },
]
for claim in NEW:
    upsert(claims, "claim_id", claim)
save("claims-register.csv", cf, claims)

# ---------------------------------------------------------------- связи
rf, rels = load("relationship-register.csv")
rel_updates = {
    "R-0012": {
        "rationale": "Салих Хузнахметович назван прадедом по отцу, Фарит Салихович — дедом; звено между ними устанавливается по отчеству Фарита",
    },
    "R-0013": {
        "rationale": "Хузнахмет назван прапрадедом, Салих — прадедом; отчество Салиха «Хузнахметович» подтверждает звено",
    },
    "R-0015": {
        "relationship_type": "мать — дочь",
        "claim_ids": "C-0044",
        "supporting_artifact_ids": "A-0017; A-0031",
        "independence_groups": "IG-15-INTERVIEW-6",
        "status": "single-source",
        "confidence": "высокая для семейного свидетельства",
        "rationale": "Прямое подтверждение субъекта: «Зульхия — мама Рамзии». Документ не проверялся",
    },
    "R-0016": {
        "claim_ids": "C-0055",
        "rationale": "Пара родителей Рамзии; брак прямо не назван, поэтому связь остаётся вероятной, хотя общая фамилия Гилемов/Гилемова её поддерживает",
    },
    "R-0017": {
        "claim_ids": "C-0045",
        "supporting_artifact_ids": "A-0009; A-0017; A-0031",
        "status": "corroborated",
        "confidence": "высокая",
        "rationale": "Две независимые цепочки: запись индекса и семейное свидетельство. После исправления имени совпадают имя, отчество в варианте, год, деревня и сценарий ссылки; дело № 15358 остаётся документальной проверкой",
    },
    "R-0018": {
        "claim_ids": "C-0046",
        "supporting_artifact_ids": "A-0008; A-0017; A-0031",
        "status": "corroborated",
        "confidence": "средняя",
        "rationale": "Тождество следует из тождества сына (R-0017) и имени отца в деле; год рождения расходится (C-0026), но это вопрос даты, а не личности",
    },
}
for rid, patch in rel_updates.items():
    upsert(rels, "relationship_id", {"relationship_id": rid, **patch})
save("relationship-register.csv", rf, rels)

print("artifacts:", len(artifacts), "persons:", len(persons), "claims:", len(claims), "rels:", len(rels))
