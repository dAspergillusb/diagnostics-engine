from flask import (
    Flask,
    url_for,
    render_template,
    Response,
    session,
    redirect,
    request
)
from ..config import (
    TEST_DATA,
    TEST_DATA_FULL_TEST,
    TEST_DATA_READING_COMPREHENSION,
    TEST_DATA_ENGLISH,
    SUBJECTS_NAME_TO_LINK
)
from .._types import (
    DataBase
)
from ..databases import (
    ReadingComprehension,
    ReadingComprehensionDB,
    English,
    EnglishDB
)
from ..tests_engine import (
    QuestionsRange
)
from ..functions import (
    get_test_attempt_page,
    connect_database_subject,
    save_all_questions,
    save_one_question,
    get_teacher_panel_main,
    add_statistics_and_log,
    get_block_data_english,
    get_datas_rc
)


def register_teacher_panel_pages(main: Flask) -> None:
    """
    Function registers teacher panel pages.
    :param main: Flask
    :return: None
    """
    @main.route("/teacher/<username>", methods=["GET", "POST"])
    def teacher(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if not session.get("subjects"):
                session.clear()
                return render_template("/teacher_panel/404_error.html")

            subjects: list[str] = sorted(session["subjects"].split("&"))
            firstname: str = session["firstname"]
            lastname: str = session["lastname"]

            if request.method == "POST":
                return get_test_attempt_page(
                    username=username,
                    firstname=firstname,
                    lastname=lastname,
                    subjects=subjects
                )

            return render_template(
                "/teacher_panel/teacher_panel.html",
                firstname=firstname,
                lastname=lastname,
                username=username,
                subjects=subjects,
                links=SUBJECTS_NAME_TO_LINK,
            )
        return redirect(url_for("login"))

    @main.route("/teacher/<username>/test_view")
    def test_view(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if all((TEST_DATA.get("title"), TEST_DATA.get("text"), TEST_DATA.get("right_answer"))):
                return render_template(
                    "/teacher_panel/test_view/test_view.html",
                    firstname=session.get("firstname"),
                    lastname=session.get("lastname"),
                    test_data=TEST_DATA,
                    full=False,
                    len=len
                )
            else:
                return redirect(url_for("teacher", username=session.get("username")))
        return redirect(url_for("login"))

    @main.route("/teacher/<username>/test_view_full")
    def test_view_full(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if all((TEST_DATA.get("title"), TEST_DATA.get("text"), TEST_DATA.get("right_answer"))):
                return render_template(
                    "/teacher_panel/test_view/test_view.html",
                    firstname=session.get("firstname"),
                    lastname=session.get("lastname"),
                    test_data=TEST_DATA_FULL_TEST,
                    full=True,
                    len=len
                )
            else:
                return redirect(url_for("teacher", username=session.get("username")))
        return redirect(url_for("login"))

    @main.route("/teacher/<username>/test_view_rc")
    def test_view_reading_comprehension(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            return render_template(
                "/teacher_panel/test_view/test_view_rc.html",
                firstname=session.get("firstname"),
                lastname=session.get("lastname"),
                variant=TEST_DATA_READING_COMPREHENSION,
                len=len
            )

        return redirect((url_for("login")))

    @main.route("/teacher/<username>/test_view_en")
    def test_view_english(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            return render_template(
                "/teacher_panel/test_view/test_view_en.html",
                firstname=session.get("firstname"),
                lastname=session.get("lastname"),
                block=TEST_DATA_ENGLISH.get("q_block"),
                variant=TEST_DATA_ENGLISH,
                len=len,
                range=range
            )

        return redirect(url_for("login"))

    @main.route("/teacher_panel/<username>/<input_subject>", methods=["GET", "POST"])
    def teacher_panel(username: str, input_subject: str) -> str | tuple[str, int] | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if request.method == "POST":
                clicked_button: str = request.form.get("button")
                if "question_view" in clicked_button:
                    q_number = clicked_button.split()[1]
                    return get_test_attempt_page(
                        username=username,
                        firstname="",
                        lastname="",
                        subjects=[],
                        q_number=q_number
                    )
                elif clicked_button == "test_view":
                    _range: range = QuestionsRange(input_subject, request.args.get("school_class")).get_range()
                    for q_num in _range:
                        get_test_attempt_page(
                            username=username,
                            firstname="",
                            lastname="",
                            subjects=[],
                            q_number=q_num
                        )
                        TEST_DATA_FULL_TEST[q_num] = TEST_DATA.copy()
                    return "", 204

                subject_db: DataBase = connect_database_subject(input_subject)
                if subject_db:

                    match clicked_button:
                        case "all":
                            return save_all_questions(subject_db, input_subject)
                        case _:
                            return save_one_question(subject_db, input_subject, int(clicked_button))

            return get_teacher_panel_main(username=username, input_subject=input_subject)

        return redirect(url_for("login"))

    @main.route("/teacher_panel/<username>/reading_comprehension", methods=["GET", "POST"])
    def reading_comprehension(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if request.method == "POST":
                clicked_button: str = request.form.get("button")
                _reading_comprehension: ReadingComprehensionDB = connect_database_subject("reading_comprehension")
                if _reading_comprehension:
                    datas: str | dict[str, str] = get_datas_rc(
                        test=True) if clicked_button == "test_view" else get_datas_rc()
                    if isinstance(datas, str):
                        return datas
                    elif clicked_button == "test_view":
                        for data in datas:
                            TEST_DATA_READING_COMPREHENSION[data] = datas[data]
                        return redirect(url_for("test_view_reading_comprehension", username=username))

                    _reading_comprehension.add_test(datas)
                    add_statistics_and_log(
                        input_subject="reading_comprehension",
                        username=username,
                        questions_id=[f"{_reading_comprehension.session.query(ReadingComprehension).all()[-1].id}"],
                        questions_value=15
                    )

                    return render_template(
                        "/teacher_panel/teacher_panel.html",
                        firstname=session.get("firstname"),
                        lastname=session.get("lastname"),
                        username=username,
                        subjects=sorted(session["subjects"].split("&")),
                        links=SUBJECTS_NAME_TO_LINK,
                        school_class=session.get("school_class"),
                        question_add_value=15,
                        modal_success="rc"
                    )
            return get_teacher_panel_main(username=username, input_subject="reading_comprehension")

        return redirect(url_for("login"))

    @main.route("/teacher_panel/<username>/english", methods=["GET", "POST"])
    def english_panel(username: str):
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            if request.method == "POST":
                clicked_button: str = request.form.get("button")
                is_test_view: bool = not clicked_button.isdigit()
                _english: EnglishDB = connect_database_subject("english")
                if _english:
                    block_data: str | dict[str, list[str] | str | int | None] | dict[
                        str, str | int] = get_block_data_english(username=username, test=is_test_view)
                    if isinstance(block_data, str):
                        return block_data
                    elif is_test_view:
                        for block in block_data:
                            TEST_DATA_ENGLISH[block] = block_data[block]
                        return redirect(url_for("test_view_english", username=username))

                    _english.add_block(block_data)
                    questions_ids: list[str] = [f"{_english.session.query(English).all()[-1].id}"]
                    questions_value: int = 0
                    for block in block_data:
                        if all((block_data[block], block.split("_")[1].isdigit())):
                            questions_value += 1

                    add_statistics_and_log(
                        input_subject="english",
                        username=username,
                        questions_id=questions_ids,
                        questions_value=questions_value
                    )

                    return render_template(
                        "/teacher_panel/teacher_panel.html",
                        firstname=session.get("firstname"),
                        lastname=session.get("lastname"),
                        username=username,
                        subjects=sorted(session["subjects"].split("&")),
                        links=SUBJECTS_NAME_TO_LINK,
                        school_class=request.args.get("school_class"),
                        modal_success="en"
                    )

            return get_teacher_panel_main(username=username, input_subject="english")

        return redirect(url_for("login"))
