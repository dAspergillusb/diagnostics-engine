from sqlalchemy import Column, Integer, String
from jinja2.filters import do_striptags
from diagnostics.modules.types.Types import BaseTable
from diagnostics.modules.databases.ReadingComprehensionDB import ReadingComprehension
from diagnostics.modules.databases.EnglishDB import English


class TestsChecker:

    def __init__(
            self,
            subject: str,
            answers: dict[int, list[str] | dict[int, list[str]]],
            variant: dict[
                Column[Integer] | int | str,
                BaseTable | English | Column[String] | Column[Integer] | list[Column[String]]
            ]
    ):
        self.subject = subject
        self.answers = answers
        self.variant = variant
        self.marks: list[int] = []
        self.questions: list[str] = []

    def check_test(self) -> tuple[list[int], list[str]]:
        match self.subject:
            case "reading_comprehension":
                return self.check_rc()
            case "english":
                return self.check_en()
            case _:
                return self.check_other()

    def check_rc(self) -> tuple[list[int], list[str]]:
        variant_rc: ReadingComprehension = self.variant.get(1)
        max_value_right_answers: int = 0
        for q_num in range(1, 16):
            count_right_answers: int = 0
            right_answers: list[Column[String]] = getattr(variant_rc, f"q_right_ans_{q_num}").split("&")
            max_value_right_answers += len(right_answers)
            for answer in self.answers[q_num]:
                if answer in right_answers:
                    count_right_answers += 1

            self.marks.append(count_right_answers)
            self.questions.append(do_striptags(getattr(variant_rc, f"q_{q_num}")))
        self.marks.append(max_value_right_answers)

        return self.marks, self.questions

    def check_en(self) -> tuple[list[int], list[str]]:
        print(f"{self.answers=}")
        max_value_right_answers: int = 0
        for block in self.answers:
            length = sum([1 for num in range(1, 11) if getattr(self.variant[block], f"q_{num}")]) # 11 is max value of questions in block.
            for q_num in range(1, length + 1):  # plus one because of starts with one
                count_right_answers: int = 0
                right_answers: list[str] = getattr(self.variant[block], f"q_right_ans_{q_num}").split("&")
                max_value_right_answers += len(right_answers)
                print(f"{count_right_answers=}\n{right_answers=}\n{max_value_right_answers}")

                for answer in self.answers[block].get(q_num, ""):
                    if answer in right_answers:
                        count_right_answers += 1

                self.marks.append(count_right_answers)
                self.questions.append(do_striptags(f"{q_num}. {getattr(self.variant[block], f'q_{q_num}')}"))
        self.marks.append(max_value_right_answers)

        return self.marks, self.questions

    def check_other(self):
        length: int = len(self.answers)
        max_value_right_answers: int = 0
        for q_num in range(1, length + 1):  # plus one because of starts with one
            count_right_answers: int = 0
            right_answers: list[Column[String]] = self.variant[q_num].q_right_answer.split("&")
            max_value_right_answers += len(right_answers)
            for answer in self.answers.get(q_num, ""):
                if answer in right_answers:
                    count_right_answers += 1

            self.marks.append(count_right_answers)
            self.questions.append(f"{self.variant[q_num].q_title}")
        self.marks.append(max_value_right_answers)

        return self.marks, self.questions

