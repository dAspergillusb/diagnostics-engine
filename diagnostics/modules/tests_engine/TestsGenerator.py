from collections import defaultdict
from typing import Type
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Connection
)
from random import randint
from diagnostics.modules._types.Types import DataBase, BaseTable
from diagnostics.modules.config import SUBJECTS
from diagnostics.modules.databases.EnglishDB import English
from diagnostics.modules.databases.ReadingComprehensionDB import ReadingComprehension


class TestsGenerator:

    def __init__(self, subject: str, school_class: str, topic: str = None):
        self.subject = subject
        #self.topic = topic
        # self.school_class = school_class
        questions: DataBase | ReadingComprehension | English = SUBJECTS[subject]["db"]()
        match subject:
            case "reading_comprehension":
                variants: list[Type[ReadingComprehension]] = [
                    test for test in questions.session.query(ReadingComprehension).all()
                    if test.school_class == school_class
                ]
                self.random_variant: Type[ReadingComprehension] = variants[
                    randint(0, len(variants) - 1)
                ] if variants else None
            case "english":
                blocks_for_school_class: list[Type[English]] = [
                    block for block in questions.session.query(English).all()
                    if block.school_class == school_class
                ]
                self.blocks_variants: defaultdict[Column[Integer], list[English]] = defaultdict(list)
                for block in blocks_for_school_class:
                    self.blocks_variants[block.q_block].append(block)
            case "mathematics":
                questions_for_subject: list[BaseTable] = [
                    question for question in questions.session.query(SUBJECTS[subject]["base"]).all()
                    if question.school_class == school_class and question.topic == topic
                ]
                self.question_variants: defaultdict[Column[Integer], list[BaseTable]] = defaultdict(list)
                for question in questions_for_subject:
                    self.question_variants[question.q_number].append(question)
            case _:
                questions_for_subject: list[BaseTable] = [
                    question for question in questions.session.query(SUBJECTS[subject]["base"]).all()
                    if question.school_class == school_class
                ]
                self.question_variants: defaultdict[Column[Integer], list[BaseTable]] = defaultdict(list)
                for question in questions_for_subject:
                    self.question_variants[question.q_number].append(question)

    def generate_test_variant(self) -> dict[
        Column[Integer] | int | str,
        BaseTable | English | Column[String] | Column[Integer] | list[Column[String]]
    ]:
        match self.subject:
            case "reading_comprehension":
                return self.generate_reading_comprehension() if self.random_variant else {}
            case "english":
                return self.generate_english()
            case _:
                return self.generate_other()

    def generate_reading_comprehension(self) -> dict[
        int | str,
        Column[String] | Column[Integer] | list[Column[String]]
    ]:
        generated_test: dict[int | str, Column[String] | Column[Integer] | list[Column[String]]] = {
            attr: getattr(self.random_variant, attr) for attr in dir(self.random_variant)
            if not attr.startswith(("_", "reg", "meta"))
        }
        return generated_test

    def generate_english(self) -> dict[Column[Integer] | int, English | None]:
        generated_test: dict[Column[Integer] | int, English | None] = {
            block: None for block in range(1, len(self.blocks_variants) + 1)
        }
        for block in self.blocks_variants:
            all_block_variants: int = len(self.blocks_variants[block]) - 1
            generated_test[block] = self.blocks_variants[block][randint(0, all_block_variants)]
        return generated_test

    def generate_other(self) -> dict[Column[Integer], BaseTable]:
        generated_test: dict[Column[Integer] | int, BaseTable | None] = {
            question: None for question in range(1, len(self.question_variants) + 1)
        }
        for question_number in self.question_variants:
            questions_count: int = len(self.question_variants[question_number]) - 1  # Index number of questions in list
            generated_test[question_number] = self.question_variants[question_number][randint(0, questions_count)]

        return generated_test


if __name__ == '__main__':
    pass
    # test = TestsGenerator(subject="mathematics", school_class="5")
    # test_ = test.generate_test_variant()
    # print(test_)
