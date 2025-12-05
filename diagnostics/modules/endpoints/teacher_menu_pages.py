from datetime import datetime
from collections import defaultdict
from sqlalchemy import (
    Column,
    String
)
from flask import (
    Flask,
    session,
    Response,
    render_template,
    request,
    redirect,
    url_for
)
from .._types import DataBase, BaseTable
from ..databases import (
    Users,
    UsersDB,
    ReadingComprehension,
    ReadingComprehensionDB,
    English,
    EnglishDB,
    TeacherStatisticsDB,
    TeacherStatistics,
    UsersStatisticsDB
)
from ..functions import (
    connect_database_users,
    connect_database_subject,
    connect_database_statistics,
    encoding_password,
    get_data_question_to_change,
    get_teacher_questions
)
from ..config import SUBJECTS_NAME_TO_LINK


def register_teacher_menu_pages(main: Flask) -> None:
    """
    Function register endpoints to teacher menu pages.
    :param main: Flask
    :return: None
    """
    @main.route("/teacher_menu/<username>", methods=["GET", "POST"])
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

    @main.route("/teacher_questions/<username>", methods=["GET", "POST"])
    def teacher_questions(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
            # subjects: list[str] = session.get("subjects").split("&")
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

            _teacher_questions: dict[
                Column[String], list[BaseTable | English | ReadingComprehension]] = get_teacher_questions(
                username=username
            )
            # print(_teacher_questions)

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

    @main.route("/teacher_statistics/<username>")
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
                f"{subject[0].upper()}{subject[1:]}": sum(
                    (sum(statistics.get(subject).get(_date)) for _date in statistics[subject])) for subject in
                statistics
            }

            last_month_statistics: dict[str, dict[str, int]] = {
                subject: {_date: sum(statistics[subject].get(_date, 0)) for _date in statistics.get(subject) if
                          _date and _date.split("-")[1] == datetime.now().month} for subject in statistics
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

    @main.route("/teacher_subject_statistics/<username>/<subject>")
    def teacher_subject_statistics(username: str, subject: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
            return render_template(
                "/teacher_menu/teacher_menu_subject_stat.html",
                user=user,
                subjects_links=SUBJECTS_NAME_TO_LINK
            )

        return redirect(url_for("login"))

    @main.route("/teacher_subject_statistics_for_student/<username>")
    def teacher_subject_statistics_for_student(username: str) -> str | Response:
        if all((session.get("user_id"), session.get("rank") == "teacher")):
            user: Users = connect_database_users().session.query(Users).get(session.get("user_id"))
            return render_template(
                "/teacher_menu/teacher_menu_subject_student_stat.html",
                user=user,
                subjects_links=SUBJECTS_NAME_TO_LINK
            )

        return redirect(url_for("login"))