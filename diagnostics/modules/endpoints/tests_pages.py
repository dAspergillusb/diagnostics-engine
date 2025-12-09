from time import time
from datetime import date, datetime
from sqlalchemy import (
    Column,
    String,
    Integer
)
from flask import (
    Flask,
    session,
    request,
    redirect,
    url_for,
    render_template
)
from ..config import (
    SUBJECTS,
    SUBJECTS_NAME_TO_LINK,
    UNIQUE_SUBJECTS
)
from ..databases import (
    UsersStatisticsDB,
    English
)
from .._types import (
    BaseTable
)
from ..tests_engine import (
    TestsChecker,
    TestsGenerator
)
from ..log import StudentsStatisticsLog
from ..functions import (
    get_questions_range,
    get_answers,
    get_right_answers_and_answers
)


def register_tests_pages(main: Flask) -> None:
    """
    Function registers endpoints to pages with tests generation
    :param main: Flask
    :return: None
    """
    @main.route("/generate_test/<subject>", methods=["GET", "POST"])
    def generate_test(subject: str):
        if all((session.get("user_id"), session.get("rank") in ("student", "teacher"))):
            school_class: str = session.get("school_class", None)
            topic: str | None = request.args.get("topic")
            if request.method == "POST":
                length: int = len(session["test_variant_ids"])
                ids = {question.id: question for question in
                       SUBJECTS[subject]["db"]().session.query(SUBJECTS[subject]["base"]).all()}
                variant = {q_num: ids[session["test_variant_ids"][q_num - 1]] for q_num in range(1, length + 1)}
                #print(f"{variant=}")
                if request.form.get("back"):
                    return redirect(url_for("student", username=session.get("username")))
                elif request.form.get("start_test"):
                    if not all((session.get("start_test"), session.get("stop_test"))):
                        start_time: int = int(time())
                        stop_time: int = start_time + 2700  # It's 45 minutes for test (45 minutes * 60 seconds = 2700 seconds)
                        session["start_test"] = start_time
                        session["stop_test"] = stop_time
                        test_time: int = session.get("stop_test") - session.get("start_test")
                    else:
                        test_time: int = session.get("stop_test") - int(time())
                    match subject:
                        case "english":
                            return render_template(
                                "/tests_generation/generated_test_en.html",
                                firstname=session.get("firstname", None),
                                lastname=session.get("lastname", None),
                                variant=variant,
                                test_time=test_time,
                                getattr=getattr,
                                len=len
                            )
                        case "reading_comprehension":
                            variant = {
                                attr: getattr(variant[1], attr) for attr in dir(variant[1])
                                if not attr.startswith(("_", "reg", "meta"))
                            }
                            return render_template(
                                "/tests_generation/generated_test_rc.html",
                                firstname=session.get("firstname", None),
                                lastname=session.get("lastname", None),
                                variant=variant,
                                test_time=test_time,
                                len=len
                            )
                        case _:
                            subjects_names: dict[str, str] = {
                                SUBJECTS_NAME_TO_LINK[subject]: subject.title() for subject in SUBJECTS_NAME_TO_LINK
                            }
                            return render_template(
                                "/tests_generation/generated_test.html",
                                firstname=session.get("firstname", None),
                                lastname=session.get("lastname", None),
                                variant=variant,
                                test_time=test_time,
                                subject=subjects_names.get(subject),
                                len=len
                            )

                _range: range = get_questions_range(
                    subject=subject,
                    length=length
                )

                answers: dict[int, list[str] | dict[int, list[str]]] = get_answers(
                    subject=subject,
                    _range=_range
                )
                #print(f"{answers=}")

                check_: TestsChecker = TestsChecker(
                    subject=subject,
                    answers=answers,
                    variant=variant
                )
                marks, questions = check_.check_test()  # Here we get  list of test marks and test questions
                #print(f"{marks=}\n{questions=}")
                max_value = marks.pop()  # Takes the sum of max test score
                value = sum(marks)  # Takes the value of test score
                not_right = sum([1 for mark in marks if not mark])  # Count of not right answers
                percent = int((value / max_value) * 100) if max_value else 0  # Takes the value of succeed performed test in %

                UsersStatisticsDB().add_statistics(
                    user_id=session["user_id"],
                    firstname=session["firstname"],
                    lastname=session["lastname"],
                    subject=subject,
                    school_class=session["school_class_full"],
                    common_value=value,
                    common_max_value=max_value,
                    common_not_right=not_right,
                    common_percent=percent,
                    test_date=f"{date.today()}"
                )

                StudentsStatisticsLog(
                    _date=datetime.now(),
                    user_id=session.get("user_id"),
                    username=session.get("username"),
                    school_class=session.get("school_class"),
                    subject=subject
                ).add_statistics_log()

                right_answers_and_answers: dict[int, tuple[tuple[int, int, str]], ...] = get_right_answers_and_answers(
                    subject=subject,
                    variant=variant,
                    marks=marks,
                    questions=questions
                )

                session.__delitem__("start_test")
                session.__delitem__("stop_test")

                return render_template(
                    "/testing_result/testing_result_en.html" if subject in UNIQUE_SUBJECTS else "/testing_result/testing_result.html",
                    firstname=session.get("firstname"),
                    lastname=session.get("lastname"),
                    username=session.get("username"),
                    right_answers_and_answers=right_answers_and_answers,
                    len=len,
                    subject=subject,
                    value=value,
                    max_value=max_value,
                    not_right=not_right,
                    percent=percent
                )

            if subject:
                test_generate: TestsGenerator = TestsGenerator(
                    subject=subject,
                    school_class=school_class.split("-")[0],
                    topic=topic
                )
                variant: dict[
                    Column[Integer] | int | str,
                    BaseTable | English | Column[String] | Column[Integer] | list[Column[String]]
                ] = test_generate.generate_test_variant()

                if not variant:
                    subjects_names: dict[str, str] = {
                        SUBJECTS_NAME_TO_LINK[subject]: subject.title() for subject in SUBJECTS_NAME_TO_LINK
                    }
                    return render_template(
                        "/tests_generation/error_no_tests.html",
                        firstname=session.get("firstname", None),
                        lastname=session.get("lastname", None),
                        username=session.get("username"),
                        subject=subjects_names[subject]
                    )

                match subject:
                    case "reading_comprehension":
                        session["test_variant_ids"] = [variant.get("id")]
                        return render_template(
                            "/tests_generation/generated_test_rc_start.html",
                            firstname=session.get("firstname", None),
                            lastname=session.get("lastname", None),
                            variant=variant.keys()
                        )
                    case "english":
                        session["test_variant_ids"] = [variant[block].id for block in variant]
                        return render_template(
                            "/tests_generation/generated_test_en_start.html",
                            firstname=session.get("firstname", None),
                            lastname=session.get("lastname", None),
                            variant=variant.keys()
                        )
                    case _:
                        subjects_names: dict[str, str] = {
                            SUBJECTS_NAME_TO_LINK[subject]: subject.title() for subject in SUBJECTS_NAME_TO_LINK
                        }
                        session["test_variant_ids"] = [variant[question].id for question in variant]
                        return render_template(
                            "/tests_generation/generated_test_start.html",
                            firstname=session.get("firstname", None),
                            lastname=session.get("lastname", None),
                            subject=subjects_names.get(subject),
                            variant=variant.keys()
                        )
        return redirect(url_for("login"))