from datetime import date, datetime
from base64 import b64encode
from werkzeug.datastructures import FileStorage
from flask import request, render_template, session
from sqlalchemy import (
    Column,
    Integer,
    String
)
from diagnostics.modules.tests_engine.QuestionsRange import QuestionsRange
from diagnostics.modules.databases.EnglishDB import English
from diagnostics.modules.databases.TeacherStatisticsDB import TeacherStatisticsDB
from diagnostics.modules.log.LogEngine import AddQuestionLog
from diagnostics.modules._types.Types import BaseTable, DataBase
from diagnostics.modules.config import SUBJECTS, SUPPORTED_IMAGE_TYPES, SUBJECTS_NAME_TO_LINK, SUBJECTS_RANGES_FOR_CLASS
from diagnostics.modules.functions.files_operations import write_image_file, get_filepath


# Functions for students
def get_questions_range(subject: str, length: int) -> range:
    _range: range = range(0)
    match subject:
        case "reading_comprehension":
            _range = range(1, 16)
        case _:
            _range = range(1, length + 1)
    return _range


def get_answers(subject: str, _range: range) -> dict[int, list[str] | dict[int, list[str]]]:
    answers: dict[int, list[str] | dict[int, list[str]]] = {}
    match subject:
        case "english":
            for block_num in _range:
                answers[block_num] = {}
                answers[block_num].update(
                    {
                        q_num: request.form.getlist(f"{block_num}_{q_num}")
                        for q_num in range(1, 11)
                        if request.form.getlist(f"{block_num}_{q_num}")
                    }
                )
        case _:
            for q_num in _range:
                answers[q_num] = request.form.getlist(f"{q_num}")
    return answers


def get_right_answers_and_answers(
        subject: str,
        variant: dict[
            Column[Integer] | int | str,
            BaseTable | English | Column[String] | Column[Integer] | list[Column[String]]
        ],
        marks: list[int],
        questions: list[str]
) -> dict[int, tuple[tuple[int, int, str]], ...]:

    match subject:
        case "english" | "reading_comprehension":
            return for_english_or_rc(
                subject=subject,
                variant=variant,
                marks=marks,
                questions=questions
            )
        case _:
            return for_other_subjects(
                subject=subject,
                variant=variant,
                marks=marks,
                questions=questions
            )


def for_english_or_rc(subject: str, variant, marks: list[int], questions: list[str]) -> dict[int, tuple[tuple[int, int, str]], ...]:
    right_answers_and_answers: dict[int, tuple[tuple[int, int, str]], ...] = {}
    delta: int = 0
    _range: range = range(1, 11) if subject == "english" else range(1, 16)
    for block in variant:
        right_answers: list[int] = [
            len(getattr(variant[block], f"q_right_ans_{num}").split("&"))
            for num in _range
            if getattr(variant[block], f"q_right_ans_{num}")
        ]
        answer_points: list[int] = [marks[index] for index in range(delta, len(right_answers) + delta)]
        block_questions: list[str] = [questions[index] for index in range(delta, len(right_answers) + delta)]
        right_answers_and_answers[block] = tuple(zip(right_answers, answer_points, block_questions))
        delta += len(right_answers)

    return right_answers_and_answers


def for_other_subjects(subject: str, variant, marks: list[int], questions: list[str]) -> dict[int, tuple[tuple[int, int, str]], ...]:
    right_answers_and_answers: dict[int, tuple[tuple[int, int, str]], ...] = {}
    delta: int = 0
    for block in variant:
        right_answers: list[int] = [
            len(getattr(variant[block], "q_right_answer").split("&"))
        ]
        answer_points: list[int] = [marks[delta] for index in range(len(right_answers))]
        block_questions: list[str] = [questions[delta] for index in range(len(right_answers))]
        right_answers_and_answers[block] = tuple(zip(right_answers, answer_points, block_questions))
        delta += 1
    return right_answers_and_answers


# Functions for teachers
def save_one_question(subject_db: DataBase, input_subject: str, q_number: int) -> str:
    """
    Saves one test question for subjects excepts reading comprehension and english. If there is at least one
    mistake while filling form function returns htmp-pade with modal about mistake.
    :param subject_db: Subject database-object.
    :param input_subject: What subject is? (for example -> mathematics)
    :param q_number: What question number of test is?
    :return: generates htms-page from template with variables.
    """
    username: str = session.get("username")
    parameters: dict[str, str | int] = get_parameters(input_subject=input_subject, q_number=q_number)
    print(parameters)
    if all([parameters.get("q_title"), parameters.get("q_text"),
            any(
                [
                    not parameters.get("q_answer_variants") and parameters.get("q_right_answer"),
                    parameters.get("q_answer_variants") and parameters.get("q_right_answer")
                ])]):
        parameters.update(
            {"q_image": get_filepath(
                subject=input_subject,
                file=request.files.get(f"q_image_{q_number}"),
                num=q_number)
            }
        )
        subject_db.add_question(**parameters)

        question_id: list[str] = [f"{subject_db.session.query(SUBJECTS[input_subject]['base']).all()[-1].id}"]
        add_statistics_and_log(input_subject=input_subject, username=username, questions_id=question_id)
        return render_template(
            "/teacher_panel/teacher_panel.html",
            firstname=session.get("firstname"),
            lastname=session.get("lastname"),
            username=username,
            subjects=sorted(session["subjects"].split("&")),
            links=SUBJECTS_NAME_TO_LINK,
            school_class=session.get("school_class"),
            question_add_value=1,
            modal_success="other"
        )
    subjects_names: dict[str, str] = {SUBJECTS_NAME_TO_LINK[subject]: subject.title() for subject in
                                      SUBJECTS_NAME_TO_LINK}
    return render_template(
        f"/teacher_panel/subjects/teacher_common.html",
        subject=subjects_names[input_subject],
        school_class=session.get("school_class"),
        input_subject=input_subject,
        firstname=session.get("firstname"),
        lastname=session.get("lastname"),
        username=username,
        subjects=sorted(session["subjects"].split("&")),
        links=SUBJECTS_NAME_TO_LINK,
        _range=QuestionsRange(input_subject, session.get("school_class")).get_range(),
        _range_classes=SUBJECTS_RANGES_FOR_CLASS,
        html_page="teacher_panel",
        session_input=request.form,
        session_files=request.files,
        modal_failed=True
    )


def save_all_questions(subject_db: DataBase, input_subject: str) -> str:
    """
    Saves all test questions for subjects excepts reading comprehension and english. If there is at least one
    mistake while filling form function returns htmp-pade with modal about mistake.
    :param subject_db: Subject database-object.
    :param input_subject: What subject is? (for example -> mathematics)
    :return: generates htms-page from template with variables.
    """
    username: str = session.get("username")
    _range: range = QuestionsRange(input_subject, request.args.get("school_class")).get_range()
    questions_id: list[str] = []
    question_add_value: int = 0
    for number in _range:
        parameters: dict[str, str | int] = get_parameters(input_subject=input_subject, q_number=number)
        if all([parameters.get("q_title"), parameters.get("q_text"),
                any(
                    [
                        not parameters.get("q_answer_variants") and parameters.get("q_right_answer"),
                        parameters.get("q_answer_variants") and parameters.get("q_right_answer")
                    ])]):
            question_add_value += 1
            parameters.update(
                {"q_image": get_filepath(
                        subject=input_subject,
                        file=request.files.get(f"q_image_{number}"),
                        num=number)
                }
            )
            subject_db.add_question(**parameters)
            questions_id.append(f"{subject_db.session.query(SUBJECTS[input_subject]['base']).all()[-1].id}")

    if question_add_value:
        add_statistics_and_log(input_subject=input_subject, username=username, questions_id=questions_id)

        return render_template(
            "/teacher_panel/teacher_panel.html",
            firstname=session.get("firstname"),
            lastname=session.get("lastname"),
            username=username,
            subjects=sorted(session["subjects"].split("&")),
            links=SUBJECTS_NAME_TO_LINK,
            school_class=session.get("school_class"),
            question_add_value=question_add_value,
            modal_success="other"
        )
    subjects_names: dict[str, str] = {SUBJECTS_NAME_TO_LINK[subject]: subject.title() for subject in
                                      SUBJECTS_NAME_TO_LINK}
    return render_template(
        "/teacher_panel/subjects/teacher_common.html",
        subject=subjects_names[input_subject],
        school_class=session.get("school_class"),
        input_subject=input_subject,
        firstname=session.get("firstname"),
        lastname=session.get("lastname"),
        username=username,
        session_input=request.form,
        subjects=sorted(session["subjects"].split("&")),
        links=SUBJECTS_NAME_TO_LINK,
        _range=_range,
        _range_classes=SUBJECTS_RANGES_FOR_CLASS,
        html_page="teacher_panel",
        modal_failed=True
    )


def get_datas_rc(test: bool = False) -> str | dict[str, str]:
    """
    Gets the data from test form. If there is at least one mistake, returns html-string with mistake message.
    :return: Html-string if there is mistake else  datas dictionary.
    """
    school_class = request.args.get("school_class")
    test_title: str = request.form.get("test_title")
    test_text: str = request.form.get("test_text")
    datas: dict[str, str] = {
        "school_class": school_class,
        "test_title": test_title,
        "test_text": test_text
    }
    for number in range(1, 16):
        question: str = request.form.get(f"q_{number}")
        q_answer_variants: list[str] = request.form.getlist(f"q_ans_var_{number}")
        q_right_answer: list[str] = request.form.getlist(f"q_right_ans_{number}")
        if all(
                (
                    test_title,
                    test_text,
                    question,
                    any(
                        (
                            q_answer_variants[0] and not q_right_answer,
                            len(q_answer_variants) > 1 and q_right_answer
                        )
                    )
                )
        ):
            datas.update(
                {
                    f"q_{number}": question,
                    f"q_ans_var_{number}": "&".join(q_answer_variants) if q_right_answer else "",
                    f"q_right_ans_{number}": "&".join(q_right_answer) if q_right_answer else "&".join(q_answer_variants)
                }
            )
        else:
            return failed_with_data(
                username=session.get("username"),
                subject="Читательская грамотность",
                html_page="reading_comprehension",
                template="reading_comprehension"
            )
    # If it's ok, then we're adding all images
    if test:
        for number in range(1, 16):
            image = request.files.get(f"q_i_{number}")
            image_type = image.filename.split(".")[-1] if image else ""
            b64_image = b64encode(image.read()).decode() if image else ""
            datas.update({
                f"q_i_{number}": f"data:image/{image_type};base64,{b64_image}" if image else ""
            })
    else:
        datas.update(
            {
                f"q_i_{number}": get_filepath(
                    subject="reading_comprehension",
                    file=request.files.get(f"q_i_{number}"),
                    num=number) for number in range(1, 16)
            }
        )

    return datas


def get_block_data_english(username: str, test: bool = False) -> str | dict[str, list[str] | str | int | None] | dict[str, str | int]:
    school_class: str = request.args.get("school_class")
    block_number: str = request.form.get("button").split()[-1] if test else request.form.get("button")
    block_data: dict[str, list[str] | str | int | None] | dict[str, str | int] = {
        "q_block": int(block_number), "school_class": school_class
    }
    match block_number:
        case "1":
            data = get_block_data_english_one(
                username=username,
                block_data=block_data,
                test=test
            )
            if isinstance(data, str):
                return data
        case "2":
            data = get_block_data_english_two(
                username=username,
                block_data=block_data,
                test=test
            )
            if isinstance(data, str):
                return data
        case _:
            data = get_block_data_english_other(
                username=username,
                block_data=block_data,
                block_number=block_number,
                test=test
            )
            if isinstance(data, str):
                return data

    block_data.update(data)
    return block_data


def get_block_data_english_one(
        username: str,
        block_data: dict[str, list[str] | str | int | None],
        test: bool
) -> str | dict[str, list[str] | str | int | None]:
    audio_file: FileStorage = request.files.get("q_audio")
    block_data.update({"q_title": request.form.get("1 q_title")})
    for num in range(1, 11):
        q_ans_var: list[str] | str = request.form.getlist(f"1 q_ans_var_{num}")
        q_right_ans: list[str] | str = request.form.getlist(f"1 q_right_ans_{num}")
        if test:
            q_ans_var = "&".join(q_ans_var) if q_right_ans else ""
            q_right_ans = "&".join(q_right_ans) if q_right_ans else "&".join(q_ans_var)
        block_data.update(
            {
                f"q_{num}": request.form.get(f"1 q_{num}"),
                f"q_ans_var_{num}": q_ans_var,
                f"q_right_ans_{num}": q_right_ans
            }
        )
    if test:
        audio_file_type = audio_file.filename.split(".")[-1] if audio_file else ""
        audio_file_b64 = b64encode(audio_file.read()).decode() if audio_file else ""
        q_audio: str = f"data:audio/{audio_file_type};base64,{audio_file_b64}" if audio_file else ""
    else:
        q_audio: str = get_filepath(subject="english", file=audio_file)
    block_data.update({"q_audio": q_audio})
    if not all((
            q_audio,
            block_data.get("q_title"),
            block_data.get("q_1"),
            any((
                    len(block_data.get("q_ans_var_1")) == 1 and not block_data.get("q_right_ans_1"),
                    len(block_data.get("q_ans_var_1")) > 1 and block_data.get("q_right_ans_1")
            )),
    )):
        return failed_with_data(
            username=username,
            subject="Английский язык",
            html_page="english_panel",
            template="english"
        )

    return block_data


def get_block_data_english_two(
        username: str,
        block_data: dict[str, list[str] | str | int | None],
        test: bool
) -> str | dict[str, list[str] | str | int | None]:
    block_data.update({"q_title": request.form.get("2 q_title"), "q_text": request.form.get("2 q_text")})
    for num in range(1, 11):
        q_ans_var: list[str] | str = request.form.getlist(f"1 q_ans_var_{num}")
        q_right_ans: list[str] | str = request.form.getlist(f"1 q_right_ans_{num}")
        if test:
            q_ans_var = "&".join(q_ans_var) if q_right_ans else ""
            q_right_ans = "&".join(q_right_ans) if q_right_ans else "&".join(q_ans_var)
        block_data.update(
            {
                f"q_{num}": request.form.get(f"2 q_{num}"),
                f"q_ans_var_{num}": q_ans_var,
                f"q_right_ans_{num}": q_right_ans
            }
        )
    if not all((
            block_data.get("q_title"),
            block_data.get("q_text"),
            block_data.get("q_1"),
            any((
                    len(block_data.get("q_ans_var_1")) == 1 and not block_data.get("q_right_ans_1"),
                    len(block_data.get("q_ans_var_1")) > 1 and block_data.get("q_right_ans_1")
            )),
    )):
        return failed_with_data(
            username=username,
            subject="Английский язык",
            html_page="english_panel",
            template="english"
        )

    return block_data


def get_block_data_english_other(
        username: str,
        block_data: dict[str, str | int],
        block_number: str,
        test: bool
) -> str | dict[str, str | int]:
    block_data.update({"q_title": request.form.get(f"{block_number} q_title")})
    for num in range(1, 11):
        q_ans_var: list[str] | str = request.form.getlist(f"1 q_ans_var_{num}")
        q_right_ans: list[str] | str = request.form.getlist(f"1 q_right_ans_{num}")
        if test:
            q_ans_var = "&".join(q_ans_var) if q_right_ans else ""
            q_right_ans = "&".join(q_right_ans) if q_right_ans else "&".join(q_ans_var)
        block_data.update({
            f"q_{num}": request.form.get(f"{block_number} q_{num}"),
            f"q_ans_var_{num}": q_ans_var,
            f"q_right_ans_{num}": q_right_ans,
        })
    if not all((
            block_data.get("q_title"),
            block_data.get("q_1"),
            any((
                    len(block_data.get("q_ans_var_1")) == 1 and not block_data.get("q_right_ans_1"),
                    len(block_data.get("q_ans_var_1")) > 1 and block_data.get("q_right_ans_1")
            )),
    )):
        return failed_with_data(
            username=username,
            subject="Английский язык",
            html_page="english_panel",
            template="english"
        )
    # If it's ok then we're adding images
    if test:
        for num in range(1, 11):
            image = request.files.get(f"{block_number} q_i_{num}")
            image_type = image.filename.split(".")[-1] if image else ""
            b64_image = b64encode(image.read()).decode() if image else ""
            block_data.update({
                f"q_i_{num}": f"data:image/{image_type};base64,{b64_image}" if image else ""
            })
    else:
        block_data.update(
            {
                f"q_i_{num}": get_filepath(
                    subject="english",
                    file=request.files.get(f"{block_number} q_i_{num}"),
                    num=num) for num in range(1, 11)
            }
        )

    return block_data


def get_parameters(input_subject: str, q_number: int) -> dict[str, str | int]:
    q_answer_variants: list[str] = request.form.getlist(f"q_answer_variants_{q_number}")
    q_right_answer: list[str] = request.form.getlist(f"q_right_answer_{q_number}")
    return {
        "q_number": q_number,
        "q_title": request.form.get(f"q_title_{q_number}"),
        "q_text": request.form.get(f"q_text_{q_number}"),
        "school_class": request.args.get("school_class"),
        "q_answer_variants": "&".join(q_answer_variants) if q_right_answer else "",
        "q_right_answer": "&".join(q_right_answer) if q_right_answer else "&".join(q_answer_variants)
    }


def add_statistics_and_log(
        input_subject: str,
        username: str,
        questions_id: list[str],
        questions_value: int = 0
) -> None:

    TeacherStatisticsDB().add_statistics(
        username=username,
        firstname=session.get("firstname"),
        lastname=session.get("lastname"),
        subject=input_subject,
        questions_value=questions_value if questions_value else len(questions_id),
        questions_id=questions_id,
        date=f"{date.today()}"
    )
    AddQuestionLog(
        _date=datetime.now(),
        subject=input_subject,
        username=username,
        question_ids=questions_id,
        question_value=questions_value if questions_value else len(questions_id)
    ).add_log_new_entry()


def failed_with_data(username: str, subject: str, html_page: str, template: str) -> str:
    return render_template(
        f"/teacher_panel/subjects/teacher_{template}.html",
        firstname=session.get("firstname"),
        lastname=session.get("lastname"),
        username=username,
        subject=subject,
        subjects=sorted(session["subjects"].split("&")),
        links=SUBJECTS_NAME_TO_LINK,
        school_class=request.args.get("school_class"),
        html_page=html_page,
        session_input=request.form,
        _range_classes=SUBJECTS_RANGES_FOR_CLASS,
        _range=QuestionsRange(template, request.args.get("school_class")).get_range(),
        modal_failed=True
    )

