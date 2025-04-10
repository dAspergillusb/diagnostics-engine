import sys
sys.path.insert(0, "/home/nikita/PycharmProjects/diagnostics/diagnostics")

from os import path, mkdir, sep
from datetime import datetime
from csv import reader, writer
from collections import defaultdict
from diagnostics.modules import (
    English,
    EnglishDB,
    Informatics,
    InformaticsDB,
    Literature,
    LiteratureDB,
    Mathematics,
    MathematicsDB,
    Physics,
    PhysicsDB,
    ReadingComprehension,
    ReadingComprehensionDB,
    Russian,
    RussianDB
)
from diagnostics.modules import BaseTable
from diagnostics.modules import SUBJECTS


def get_date() -> tuple[int, int, int]:
    _year = datetime.now().year
    _month = datetime.now().month
    _day = datetime.now().day
    return _year, _month, _day


def check_path(_year: int, _month: int, _day: int) -> bool:
    if not path.exists(f"report-{_year}-{_month}-{_day}"):
        return False
    return True


def create_path(_year: int, _month: int, _day: int) -> None:
     return mkdir(f"report-{_year}-{_month}-{_day}")


def connect_to_database(subject: str) -> BaseTable | ReadingComprehensionDB | EnglishDB:
    return SUBJECTS[subject]["db"]()


def get_subject_data(subject: str, subject_db: BaseTable | ReadingComprehension | English):
    questions_classes = defaultdict(list)
    for question in subject_db.session.query(SUBJECTS[subject]["base"]).all():
        questions_classes[int(question.school_class)].append(question)
    sorted_data: dict[int, list[BaseTable | ReadingComprehension | English]] = get_sorted_data(subject, questions_classes)
    return sorted_data


def get_sorted_data(
        subject: str,
        source_data: dict[int, list[BaseTable | ReadingComprehension | English]]
) -> dict[int, list[BaseTable | ReadingComprehension | English]]:
    match subject:
        case "reading_comprehension":
            return get_reading_comprehension_sorted_data(source_data)
        case "english":
            return get_english_sorted_data(source_data)
        case _:
            return get_other_sorted_data(source_data)


def get_other_sorted_data(source_data: dict[int, list[BaseTable]]):
    sorted_data: defaultdict[int, list[BaseTable]] = defaultdict(list)
    for school_class in source_data:
        sorted_data[school_class] = sorted(source_data[school_class], key=lambda data: data.q_number)
    return dict(sorted(sorted_data.items(), key=lambda data: data[0]))


def get_reading_comprehension_sorted_data(source_data: dict[int, list[ReadingComprehension]]):
    sorted_data: defaultdict[int, list[ReadingComprehension]] = defaultdict(list)
    for school_class in source_data:
        sorted_data[school_class] = sorted(source_data[school_class], key=lambda data: data.id)
    return dict(sorted(sorted_data.items(), key=lambda data: data[0]))


def get_english_sorted_data(source_data: dict[int, list[English]]):
    sorted_data: defaultdict[int, list[English]] = defaultdict(list)
    for school_class in source_data:
        sorted_data[school_class] = sorted(source_data[school_class], key=lambda data: data.q_block)
    return dict(sorted(sorted_data.items(), key=lambda data: data[0]))


def transform_to_csv_writable(subject: str, subject_data: dict[int, list[BaseTable | ReadingComprehension | English]]) -> list[list[str]]:
    match subject:
        case "reading_comprehension":
            return get_csv_writable_reading_comprehension(subject_data)
        case "english":
            return get_csv_writable_english(subject_data)
        case _:
            return get_csv_writable_other(subject, subject_data)


def get_csv_writable_english(subject_data: dict[int, list[English]]) -> list[list[str]]:
    date_to_csv = [["Предмет", "id блока вопросов", "Класс", "Номер блока вопросов"]]
    for school_class in subject_data:
        for block in subject_data[school_class]:
            date_to_csv.append(["english", block.id, block.school_class, block.q_block])
    return date_to_csv


def get_csv_writable_reading_comprehension(subject_data: dict[int, list[ReadingComprehension]]) -> list[list[str]]:
    date_to_csv = [["Предмет", "id теста", "Класс", "Номер теста"]]
    for school_class in subject_data:
        for test in subject_data[school_class]:
            date_to_csv.append(["reading comprehension", test.id, test.school_class, test.id])
    return date_to_csv


def get_csv_writable_other(subject: str, subject_data: dict[int, list[BaseTable]]) -> list[list[str]]:
    date_to_csv = [["Предмет", "id вопроса", "Класс", "Номер вопроса"]]
    for school_class in subject_data:
        for question in subject_data[school_class]:
            date_to_csv.append([subject, question.id, question.school_class, question.q_number])
    return date_to_csv


def get_data(subject: str) -> None:
    _year, _month, _day = get_date()
    if not check_path(_year, _month, _day):
        create_path(_year, _month, _day)

    data_base: BaseTable | ReadingComprehensionDB | EnglishDB = connect_to_database(subject)
    subject_data: dict[int, list[BaseTable | ReadingComprehension | English]] = get_subject_data(subject, data_base)
    data_to_csv = transform_to_csv_writable(subject, subject_data)

    with open(f"report-{_year}-{_month}-{_day}{sep}{subject}.csv", "w") as data:
        write_to_csv = writer(data)
        write_to_csv.writerows(data_to_csv)



if __name__ == '__main__':
    subjects = ["english", "informatics", "literature", "mathematics", "physics", "reading_comprehension", "russian"]

    for _subject in subjects:
        get_data(_subject)