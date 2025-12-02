from collections import defaultdict
from typing import Type
from time import time
from datetime import date, datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Response
)
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import Query
from werkzeug import Request
from werkzeug.datastructures import FileStorage

from modules import add_statistics_and_log
from modules import (
    is_correct_firstname,
    is_correct_lastname,
    is_correct_class,
    is_correct_email,
    is_correct_username,
    is_correct_password,
    encoding_password,
    create_date_stamp,
    check_link_time
)
from modules import (
    check_session_login_failed,
    made_login,
    get_registration_args,
    is_data_correct,
    add_user_log_email_send
)
from modules import (
    choose_student_grade,
    get_test_attempt_page,
    get_teacher_panel_main
)
from modules import (
    connect_database_users,
    connect_database_subject,
    connect_database_statistics
)
from modules import (
    get_questions_range,
    get_answers,
    get_right_answers_and_answers,
    save_one_question,
    save_all_questions,
    get_datas_rc,
    get_block_data_english,
    get_teacher_questions,
    get_data_question_to_change
)
from modules import (
    get_filepath,
    write_audio_file,
    write_test_image,
    write_image_file
)
from modules import (
    SECRET_KEY,
    HOST,
    PORT,
    ICON_BLACK,
    MAX_FORM_MEMORY_SIZE,
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_AUDIO_TYPES,
    SUBJECTS,
    STATISTICS,
    SUBJECTS_NAME_TO_LINK,
    SUBJECTS_RANGES_FOR_CLASS,
    ELEMENTARY_SCHOOL,
    UNIQUE_SUBJECTS,
    TEST_DATA,
    TEST_DATA_FULL_TEST,
    TEST_DATA_READING_COMPREHENSION,
    TEST_DATA_ENGLISH,
    MATHEMATICS_TESTS_TOPICS
)
from modules import ranks
from modules import BaseTable, DataBase
from modules import QuestionsRange
from modules import TestsGenerator
from modules import TestsChecker
from modules import EmailSender
from modules import (
    TeacherStatistics,
    TeacherStatisticsDB,
    Users,
    UsersDB,
    UsersStatistics,
    UsersStatisticsDB,
    ReadingComprehension,
    ReadingComprehensionDB,
    English,
    EnglishDB
)
from modules import (
    LogingLog,
    AddQuestionLog,
    UsersRegisterLog,
    StudentsStatisticsLog,
    EmailSenderLog
)


MAIN: Flask = Flask(import_name=__name__)
MAIN.config["SECRET_KEY"] = SECRET_KEY
MAIN.config["MAX_FORM_MEMORY_SIZE"] = MAX_FORM_MEMORY_SIZE
MAIN.config["MAX_CONTENT_LENGTH"] = MAX_FORM_MEMORY_SIZE
MAIN.config["MAX_FORM_PARTS"] = MAX_FORM_MEMORY_SIZE


@MAIN.route("/")
def home_page() -> Response:
    """
    Function redirects to login page.
    :return: None
    """
    return redirect(url_for("login"))


@MAIN.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """

    :return:
    """
    session.permanent = True
    users = connect_database_users()
    registered_users: dict[str, Users] = {
        f"{user.username}": user for user in users.session.query(Users).all()
    }
    if request.method == "POST":
        confirmed: str = request.form.get("confirm")
        if confirmed:
            match confirmed:
                case "registration":
                    return redirect(url_for("registration"))
                case "restore":
                    return redirect(url_for("restore_password"))

        username: str = request.form["username"]
        password: str = request.form["password"]
        if not all((username, password)):
            return check_session_login_failed(message="Введите имя пользователя и пароль")

        elif username in registered_users and encoding_password(password) == registered_users[username].password:
            user: Users = registered_users[username]
            return made_login(user)

        else:
            return check_session_login_failed(message="Неправильные имя пользователя или пароль")

    if request.args.get("registration_success"):
        return render_template("sign_in.html", registration_success="Успешная регистрация!")

    if request.args.get("delete_user"):
        user: Users = registered_users.get(request.args.get("username"))
        users.delete_instance(_user=user)
        session.clear()
        return render_template("sign_in.html", deleted_success="Пользователь успешно удалён.")

    return render_template("sign_in.html", icon=ICON_BLACK)


@MAIN.route("/registration", methods=["GET", "POST"])
def registration() -> str | Response:
    users = connect_database_users()
    if request.method == "POST":
        if request.form.get("confirm") == "back":
            return redirect(url_for("login"))
        username: str = request.form.get("username")
        email: str = request.form.get("email")
        if any((users.exist_username(username=username), users.exist_email(email=email))):
            return render_template(
                "registration.html",
                registration_failed="Такое имя пользователя или/и почта уже существуют."
            )

        registration_args: dict[str, str] = get_registration_args()

        if is_data_correct(**registration_args):
            add_user_log_email_send(**registration_args)

            return redirect(url_for(
                "login",
                registration_success=True
            ))

        return render_template(
            template_name_or_list="registration.html",
            modal_failed=True
        )
    return render_template("registration.html", registration_failed="")


@MAIN.route("/register_teacher", methods=["GET", "POST"])
def register_teacher() -> str | Response:
    users = connect_database_users()
    subjects_list: list[str] = sorted(SUBJECTS_NAME_TO_LINK.keys())
    if request.method == "POST":
        if request.form.get("confirm") == "back":
            return redirect(url_for("login"))
        username: str = request.form["username"]
        email: str = request.form["email"].lower()
        if any((users.exist_username(username=username), users.exist_email(email=email))):
            return render_template(
                "registration_teacher.html",
                subjects=subjects_list,
                registration_failed="Такое имя пользователя или/и почта уже существуют."
            )

        registration_args: dict[str, str] =  get_registration_args()

        if is_data_correct(**registration_args):
            add_user_log_email_send(**registration_args)

            return redirect(url_for(
                "login",
                registration_success=True
            ))

        return render_template(
            template_name_or_list="registration_teacher.html",
            subjects=subjects_list,
            modal_failed=True
        )
    return render_template(
        "registration_teacher.html",
        subjects=subjects_list
    )


@MAIN.route("/student/<username>")
def student(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "student")):
        firstname: str = session["firstname"]
        lastname: str = session["lastname"]
        school_class: str = session["school_class"].split("-")[0]
        grade, cards = choose_student_grade(school_class=school_class)
        return render_template(
            grade,
            HOST="/login",
            firstname=firstname,
            lastname=lastname,
            school_class=school_class,
            cards=cards
        )

    return redirect(url_for("login"))


@MAIN.route("/<subject>/topics_for_mathematics", methods=["GET", "POST"])
def get_topics_math(subject: str):
    if all((session.get("user_id"), session.get("rank") in ("student", "teacher"))):
        return render_template(
            "topics_math/topics_math.html",
            firstname=session.get("firstname"),
            lastname=session.get("lastname"),
            topics=MATHEMATICS_TESTS_TOPICS
        )


@MAIN.route("/teacher/<username>", methods=["GET", "POST"])
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


@MAIN.route("/teacher_menu/<username>", methods=["GET", "POST"])
def teacher_menu(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))

        if request.method == "POST":
            password: str = request.form.get("password")
            password_repeat: str = request.form.get("password_repeat")
            if len(password) < 8:
                return render_template(
                    "teacher_menu/teacher_menu.html",
                    user=user,
                    subjects_links=SUBJECTS_NAME_TO_LINK,
                    modal="length"
                )
            elif all((password == password_repeat, encoding_password(password) != user.password)):
                UsersDB().change_instance(username=user.username, password=encoding_password(password))
                return render_template(
                    "teacher_menu/teacher_menu.html",
                    user=user,
                    subjects_links=SUBJECTS_NAME_TO_LINK,
                    modal="success"
                )
            else:
                return render_template(
                        "teacher_menu/teacher_menu.html",
                        user=user,
                        subjects_links=SUBJECTS_NAME_TO_LINK,
                        modal="failed"
                    )

        return render_template(
            "teacher_menu/teacher_menu.html",
            user=user,
            subjects_links=SUBJECTS_NAME_TO_LINK
        )
    return redirect(url_for("login"))


@MAIN.route("/teacher_questions/<username>", methods=["GET", "POST"])
def teacher_questions(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
        #subjects: list[str] = session.get("subjects").split("&")
        if request.method == "POST":
            subject, question_id = request.form.get("save_changes").split()
            database: DataBase | EnglishDB | ReadingComprehensionDB = connect_database_subject(subject)
            """question_to_change: BaseTable | ReadingComprehension | English = database.session.query(
                SUBJECTS[f"{subject}"]["base"]
            ).get(question_id)"""
            database.change_question(
                question_id=question_id,
                data=get_data_question_to_change(subject=subject)
            )

        _teacher_questions: dict[Column[String], list[BaseTable | English | ReadingComprehension]] = get_teacher_questions(
            username=username
        )
        #print(_teacher_questions)

        return render_template(
            template_name_or_list="/teacher_menu/teacher_menu_questions.html",
            user=user,
            subjects_links=SUBJECTS_NAME_TO_LINK,
            teacher_questions=_teacher_questions,
            subjects_names={value: key for key, value in SUBJECTS_NAME_TO_LINK.items()},
            len=len,
            enumerate=enumerate,
            getattr=getattr
        )
    return redirect(url_for("login"))


@MAIN.route("/teacher_statistics/<username>")
def teacher_statistics(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
        user_statistics: TeacherStatisticsDB | UsersStatisticsDB | None = connect_database_statistics(user.rank)
        subjects_names: dict[str, str] = {
            SUBJECTS_NAME_TO_LINK[subject]: subject for subject in SUBJECTS_NAME_TO_LINK
        }
        statistics: dict[str, defaultdict[str, list]] = {
            subject: defaultdict(list) for subject in user.subject.split("&")
        }

        for stat in user_statistics.session.query(TeacherStatistics).filter(
                TeacherStatistics.username == user.username).all():
            statistics[f"{subjects_names[f'{stat.subject}']}"][f"{stat.date}"].append(stat.questions_value)

        common_statistics: dict[str, int] = {
            f"{subject[0].upper()}{subject[1:]}": sum((sum(statistics.get(subject).get(_date)) for _date in statistics[subject])) for subject in statistics
        }

        last_month_statistics: dict[str, dict[str, int]] = {
            subject: {_date: sum(statistics[subject].get(_date, 0)) for _date in statistics.get(subject) if _date and _date.split("-")[1] == datetime.now().month} for subject in statistics
        }
        print(last_month_statistics)
        return render_template(
            "/teacher_menu/teacher_menu_statistics.html",
            user=user,
            statistics=statistics,
            common_statistics=common_statistics,
            last_month_statistics=last_month_statistics,
            subjects_links=SUBJECTS_NAME_TO_LINK,
            sum=sum
        )

    return redirect(url_for("login"))


@MAIN.route("/teacher_subject_statistics/<username>/<subject>")
def teacher_subject_statistics(username: str, subject: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
        return render_template(
            "/teacher_menu/teacher_menu_subject_stat.html",
            user=user,
            subjects_links=SUBJECTS_NAME_TO_LINK
        )

    return redirect(url_for("login"))


@MAIN.route("/teacher_subject_statistics_for_student/<username>")
def teacher_subject_statistics_for_student(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
        return render_template(
            "/teacher_menu/teacher_menu_subject_student_stat.html",
            user=user,
            subjects_links = SUBJECTS_NAME_TO_LINK
        )

    return redirect(url_for("login"))


@MAIN.route("/teacher/<username>/test_view")
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


@MAIN.route("/teacher/<username>/test_view_full")
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


@MAIN.route("/teacher/<username>/test_view_rc")
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


@MAIN.route("/teacher/<username>/test_view_en")
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


@MAIN.route("/teacher_panel/<username>/<input_subject>", methods=["GET", "POST"])
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


@MAIN.route("/teacher_panel/<username>/reading_comprehension", methods=["GET", "POST"])
def reading_comprehension(username: str) -> str | Response:
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        if request.method == "POST":
            clicked_button: str = request.form.get("button")
            _reading_comprehension: ReadingComprehensionDB = connect_database_subject("reading_comprehension")
            if _reading_comprehension:
                datas: str | dict[str, str] = get_datas_rc(test=True) if clicked_button == "test_view" else get_datas_rc()
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


@MAIN.route("/teacher_panel/<username>/english", methods=["GET", "POST"])
def english_panel(username: str):
    if all((session.get("user_id"), session.get("rank") == "teacher")):
        if request.method == "POST":
            clicked_button: str = request.form.get("button")
            is_test_view: bool = not clicked_button.isdigit()
            _english: EnglishDB = connect_database_subject("english")
            if _english:
                block_data: str | dict[str, list[str] | str | int | None] | dict[str, str | int] = get_block_data_english(username=username, test=is_test_view)
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


@MAIN.route("/admin_panel/<username>/main", methods=["GET", "POST"])
def admin_panel(username: str):
    #if session.get("rank", None) == "admin":
    users = connect_database_users()
    _users: enumerate = enumerate(users.session.query(Users).all(), start=1)
    _teacher_statistics: dict[Column[Integer], Type[TeacherStatistics]] = {
        _teacher.id: _teacher for _teacher
        in TeacherStatisticsDB().session.query(TeacherStatistics).all()
    }
    if request.method == "POST":
        clicked_button: str = request.form["save"]
        is_changed: bool = False
        users_active_before: dict[Column[String], Column[Boolean]] = {user.username: user.active for user in users.session.query(Users).all() if user.subject}
        users_active_after: dict[str, bool] = {username: bool(username) for user in request.form.getlist("isActive") for active, username in (user.split(),)}
        print(users_active_before)
        print(users_active_after)


    return render_template(
        "/admin_panel/admin_main.html",
        users=_users,
        teacher_statistics=_teacher_statistics
    )
    #return redirect(url_for("login"))


@MAIN.route("/admin_panel/test")
def admin_test():
    users = connect_database_users()
    _users: enumerate = enumerate(users.session.query(Users).all(), start=1)
    _teacher_statistics: dict[Column[Integer], Type[TeacherStatistics]] = {
        _teacher.id: _teacher for _teacher
        in TeacherStatisticsDB().session.query(TeacherStatistics).all()
    }
    return render_template(
        "/admin_panel/test.html",
        users=_users,
        teacher_statistics=_teacher_statistics
    )


@MAIN.route("/admin_panel/<username>/users", methods=["GET", "POST"])
def admin_users(username: str):
    users_stat: UsersStatisticsDB = UsersStatisticsDB()
    labels_dates: list[str] = []
    labels_class: list[str] = []
    data: list[float] = []
    datas_all = defaultdict(list)
    datas_all_mist = defaultdict(list)
    datas_for_class = defaultdict(list)
    datas_for_class_mist = defaultdict(list)

    db = sorted(users_stat.session.query(UsersStatistics).all(), key=lambda item: int(item.test_date.replace("-", "")))
    for stat in db:
        datas_all[int(stat.test_date.split("-")[2])].append(stat.common_value)

    labels_dates = list(datas_all.keys())
    data_all = [sum(lst) / len(lst) for lst in datas_all.values()]

    return render_template(
        "/admin_panel/admin_users.html",
        labels_dates=labels_dates,
        data_all=data_all
    )


@MAIN.route("/admin_panel/<username>/common_statistics", methods=["GET"])
def admin_panel_common_statistics(username: str):
    statistics: list[Type[TeacherStatistics]] = TeacherStatisticsDB().session.query(TeacherStatistics).all()
    _teacher_statistics: dict[str, defaultdict[str, int]] = {f"{statistic.firstname} {statistic.lastname}": defaultdict(int) for statistic in statistics}
    _teacher_questions_subjects_count: dict[str, dict[str, defaultdict[str, int]]] = {
        f"{statistic.subject}": {_class: defaultdict(int) for _class in QuestionsRange(f"{statistic.subject}", "").get_all_ranges()} for statistic in statistics
    }
    _subjects_classes_questions: defaultdict[str, list] = defaultdict(list)
    for statistic in statistics:
        subject: Query[BaseTable] = connect_database_subject(f"{statistic.subject}").session.query(SUBJECTS[f"{statistic.subject}"]["base"])
        _teacher_statistics[f"{statistic.firstname} {statistic.lastname}"][f"{statistic.subject}"] += int(f"{statistic.questions_value}")

        match f"{statistic.subject}":
            case "english":
                _subjects_classes_questions[f"{statistic.subject}"].extend(
                    (subject.get(_id).school_class, subject.get(_id).q_block) for _id in statistic.questions_id.split("&") if subject.get(_id)
                )
            case "reading_comprehension":
                _subjects_classes_questions[f"{statistic.subject}"].extend(
                    (subject.get(_id).school_class, 1) for _id in statistic.questions_id.split("&") if subject.get(_id)
                )
            case _:
                _subjects_classes_questions[f"{statistic.subject}"].extend(
                    (subject.get(_id).school_class, subject.get(_id).q_number) for _id in statistic.questions_id.split("&") if subject.get(_id)
                )

        #_teacher_questions_subjects_count[f"{statistic.subject}"].extend(map(int, statistic.questions_id.split("&")))

    for _subject in _subjects_classes_questions:
        for pair in _subjects_classes_questions[_subject]:
            _teacher_questions_subjects_count[_subject][pair[0]][pair[1]] += 1



    return render_template(
        "/admin_panel/common_statistics.html",
        len=len,
        teacher_statistics=_teacher_statistics
    )


@MAIN.route("/delete_user_submit")
def delete_user_submit():
    username = session.get("username", None)
    return render_template("delete_user_submit.html", username=username)


# Tests

@MAIN.route("/test", methods=["GET", "POST"])
def test():
    return render_template("test.html")


@MAIN.route("/generate_test/<subject>", methods=["GET", "POST"])
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
                username=session["username"],
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


#####################################################################################


@MAIN.route("/restore_password", methods=["GET", "POST"])
def restore_password():
    users = connect_database_users()
    if request.args.get("restore", None):
        if check_link_time(int(request.args.get("deadline", 1))):
            return render_template(
                "restore_password.html",
                time_is_up="Ссылка уже неактуальна. Пожалуйста создайте новый запрос.",
            )
        email: str = request.args.get("email", None)
        return redirect(url_for("new_password", email=email))
    if request.method == "POST":
        if request.form.get("confirm") == "back":
            return redirect(url_for("login"))
        if not request.form["email"]:
            return render_template(
                "restore_password.html",
                email_is_empty="Необходимо ввести почту, указанную при регистрации."
            )
        email: str = request.form["email"]
        """user_email: Column[String] | None = None
        firstname: Column[String] | None = None
        lastname: Column[String] | None = None"""
        for user in users.session.query(Users).all():
            if user.email == email:
                user_email = user.email
                firstname = user.firstname
                lastname = user.lastname
                break
        else:
            return render_template(
                "restore_password.html",
                email_wrong="Пользователь с такой почтой не найден!"
            )
        if user_email:
            send_time: int = create_date_stamp()
            message: str = (f"Здравствуйте, {firstname} {lastname}!\nВы запросили восстановление пароля для системы" +
                            " диагностик. Для восстановления пароля перейдите по ссылке ниже:\n\n" +
                            f"http://{HOST}/restore_password?email={email}&restore=True&deadline={send_time}\n" +
                            "Ссылка действительна в течение часа с момента запроса восстановления пароля.")
            send_email: EmailSender = EmailSender(
                subject="Восстановление пароля для сайта диагностик.",
                recipient=email,
                message=message
            )
            send_email.send_mail()
            send_email.close_connection()
            return render_template("message_sent.html")
    return render_template("restore_password.html")


@MAIN.route("/new_password", methods=["GET", "POST"])
def new_password():
    users = connect_database_users()
    email: str = request.args.get("email", None)
    correct_email: bool = any([user.email for user in users.session.query(Users).all() if user.email == email])
    if correct_email:
        if request.method == "POST":
            if request.form.get("confirm") == "back":
                return redirect(url_for("login"))
            password = request.form["password"]
            password_repeat = request.form["password_repeat"]
            if not password or not password_repeat:
                return render_template("new_password.html", password_needed="Заполните оба поля")
            elif password != password_repeat:
                return render_template(
                    "new_password.html",
                    password=password,
                    password_repeat=password_repeat,
                    passwords_not_equal="Пароли не совпадают"
                )
            elif not is_correct_password(password):
                return render_template("new_password.html", password_needed="Пароль не удовлетворяет требованиям")
            for user in users.session.query(Users).all():
                if user.email == email:
                    users.change_instance(
                        username=user.username,
                        password=encoding_password(password)
                    )
                    message: str = (
                            f"Здравствуйте, {user.firstname} {user.lastname}!\nВаш пароль успешно изменён на {password}." +
                            "Не забывайте свой пароль.")
                    send_email: EmailSender = EmailSender(
                        subject="Пароль успешно восстановлен.",
                        recipient=email,
                        message=message
                    )
                    send_email.send_mail()
                    send_email.close_connection()
                    return redirect(url_for("login", registration_success="Пароль успешно изменен."))
        return render_template("new_password.html")
    return redirect(url_for("login"))


@MAIN.route("/testing_result", methods=["GET", "POST"])
def testing_result():
    if session.get("rank", None) == "student":
        return render_template("testing_result.html",
                               firstname=session.get("firstname", None),
                               lastname=session.get("lastname", None)
                               )
    return redirect(url_for("login"))


@MAIN.route("/logout")
def logout():
    user: Users = UsersDB().session.query(Users).get(session.get("user_id"))
    LogingLog(
        _date=datetime.now(),
        user_id=user.user_id,
        username=f"{user.username}",
        rank=f"{user.rank}",
        school_class=f"{user.school_class}"
    ).add_log_logout()
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    MAIN.run(
        debug=True,
        host="127.0.0.1",
        port=PORT
    )
