import io

import pymorphy2
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from tempfile import NamedTemporaryFile
morph = pymorphy2.MorphAnalyzer()


def create_report(week, month, month3, priorities):
    word_forms_data = create_word_forms_data(priorities)
    wb = Workbook()
    week_ws: Worksheet = wb.active
    week_ws.title = "Неделя"
    week_ws.append(["Поисковый запрос", "", "", "Товаров", "Проверить", "1", "2", "3", "4", "5"])
    for record in week:
        record = dict(record)
        record.pop("search_id")
        record["is_need_check"] = "Да" if record["is_need_check"] else ""
        week_ws.append(list(record.values()))

    month_ws = wb.create_sheet("Месяц")
    month_ws.append(["Поисковый запрос", "", "", "Товаров", "Проверить", "1", "2", "3", "4", "5"])
    for record in month:
        record = dict(record)
        record.pop("search_id")
        record["is_need_check"] = "Да" if record["is_need_check"] else ""
        month_ws.append(list(record.values()))

    month3_ws = wb.create_sheet("3 месяца")
    month3_ws.append(["Поисковый запрос", "", "", "Товаров", "Проверить", "1", "2", "3", "4", "5"])
    for record in month3:
        record = dict(record)
        record.pop("search_id")
        record["is_need_check"] = "Да" if record["is_need_check"] else ""
        month3_ws.append(list(record.values()))

    priorities_ws = wb.create_sheet("Запросы")
    priorities_ws.append(["Поисковый запрос", "Частотность", "Кол-во товаров", "Приоритет"])
    for record in priorities:
        record = dict(record)
        record.pop("search_id")
        priorities_ws.append(list(record.values()))

    word_forms_ws = wb.create_sheet("Словоформы")
    word_forms_ws.append(["Слово", "Словоформа", "Кол-во вхождений", "Суммарная частотность"])
    for record in word_forms_data:
        word_forms_ws.append(list(record.values()))

    wb.save("report.xlsx")


def create_word_forms_data(priorities):
    word_forms_data = {}
    for record in priorities:
        for word in record["query"].split(" "):
            normal_form = morph.parse(word)[0].normal_form
            try:

                word_forms_data[normal_form]["entries_count"] += 1
                word_forms_data[normal_form]["frequency"] = max(record["frequency"],
                                                                word_forms_data[normal_form]["frequency"])
                if word not in word_forms_data[normal_form]["word_forms"]:
                    word_forms_data[normal_form]["word_forms"].append(word)
            except KeyError:
                word_forms_data[normal_form] = {"name": normal_form, "word_forms": [word], "entries_count": 1,
                                                "frequency": record["frequency"]}

    res = []
    for value in word_forms_data.values():
        value["word_forms"] = ", ".join(value["word_forms"])
        res.append(value)
    return res
