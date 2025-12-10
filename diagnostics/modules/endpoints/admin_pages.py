from pprint import pprint
from typing import Type
from collections import defaultdict
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)
from sqlalchemy.orm import Query
from flask import (
    Flask,
    request,
    render_template,
    send_file
)
from openpyxl import (
    Workbook
)
from ..config import SUBJECTS, SUBJECTS_NAME_TO_LINK
from .._types import BaseTable
from ..databases import (
    Users,
    UsersStatistics,
    UsersStatisticsDB,
    TeacherStatistics,
    TeacherStatisticsDB,
)
from ..tests_engine import QuestionsRange
from ..functions import (
    connect_database_users,
    connect_database_subject,
    get_common_teacher_statistics,
    get_common_students_statistics
)


def register_admin_pages(main: Flask) -> None:
    """
    Function registers endpoints to admin pages.
    :param main: Flask
    :return: None
    """

    @main.route("/admin_panel/<username>/main", methods=["GET", "POST"])
    def admin_panel(username: str):
        # if session.get("rank", None) == "admin":
        users = connect_database_users()
        _users: enumerate = enumerate(users.session.query(Users).all(), start=1)
        _teacher_statistics: dict[Column[Integer], Type[TeacherStatistics]] = {
            _teacher.id: _teacher for _teacher
            in TeacherStatisticsDB().session.query(TeacherStatistics).all()
        }
        if request.method == "POST":
            clicked_button: str = request.form["save"]
            is_changed: bool = False
            users_active_before: dict[Column[String], Column[Boolean]] = {user.username: user.active for user in
                                                                          users.session.query(Users).all() if
                                                                          user.subject}
            users_active_after: dict[str, bool] = {username: bool(username) for user in request.form.getlist("isActive")
                                                   for active, username in (user.split(),)}
            print(users_active_before)
            print(users_active_after)

        return render_template(
            "/admin_panel/admin_main.html",
            users=_users,
            teacher_statistics=_teacher_statistics
        )
        # return redirect(url_for("login"))

    @main.route("/admin_panel/test")
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

    @main.route("/admin_panel/<username>/users", methods=["GET", "POST"])
    def admin_users(username: str):
        users_stat: UsersStatisticsDB = UsersStatisticsDB()
        labels_dates: list[str] = []
        labels_class: list[str] = []
        data: list[float] = []
        datas_all = defaultdict(list)
        datas_all_mist = defaultdict(list)
        datas_for_class = defaultdict(list)
        datas_for_class_mist = defaultdict(list)

        db = sorted(users_stat.session.query(UsersStatistics).all(),
                    key=lambda item: int(item.test_date.replace("-", "")))
        for stat in db:
            datas_all[int(stat.test_date.split("-")[2])].append(stat.common_value)

        labels_dates = list(datas_all.keys())
        data_all = [sum(lst) / len(lst) for lst in datas_all.values()]

        return render_template(
            "/admin_panel/admin_users.html",
            labels_dates=labels_dates,
            data_all=data_all
        )

    @main.route("/admin_panel/<username>/common_statistics", methods=["GET"])
    def admin_panel_common_statistics(username: str):
        statistics_teachers: list[Type[TeacherStatistics]] = TeacherStatisticsDB().session.query(TeacherStatistics).all()
        statistics_students: list[Type[UsersStatistics]] = UsersStatisticsDB().session.query(UsersStatistics).all()
        common_statistics_teachers: tuple[dict[str, defaultdict[str, int]], dict[str, dict[str, defaultdict[str, int]]]] = get_common_teacher_statistics(statistics=statistics_teachers)
        _teacher_statistics: dict[str, defaultdict[str, int]] = common_statistics_teachers[0]
        _teacher_questions_subjects_count: dict[str, dict[str, defaultdict[str, int]]] = common_statistics_teachers[1]
        common_students_statistics: dict[str, dict[str, str | int]] = get_common_students_statistics(statistics=statistics_students)
        #pprint(common_students_statistics)

        return render_template(
            "/admin_panel/common_statistics.html",
            len=len,
            str=str,
            username=username,
            teacher_statistics=_teacher_statistics,
            teacher_questions_subjects_count=_teacher_questions_subjects_count,
            common_students_statistics=common_students_statistics,
            questions_range=QuestionsRange,
            subjects_names={value: key for key, value in SUBJECTS_NAME_TO_LINK.items()}
        )

    @main.route("/admin_panel/<username>/common_statistics/<subject>/<data>", methods=["GET"])
    def admin_panel_common_statistics_get_xlsx(username: str, subject: str, data: dict[str, defaultdict[str, int]]):
        excel_file: Workbook = Workbook()
        sheet = excel_file.active
        sheet.title = subject
        data_to_excel: dict[str, str | int] = {}
        print(request.form.to_dict())
        return None


