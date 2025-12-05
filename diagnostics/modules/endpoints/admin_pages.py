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
    render_template
)
from ..config import SUBJECTS
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
    connect_database_subject
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
        statistics: list[Type[TeacherStatistics]] = TeacherStatisticsDB().session.query(TeacherStatistics).all()
        _teacher_statistics: dict[str, defaultdict[str, int]] = {
            f"{statistic.firstname} {statistic.lastname}": defaultdict(int) for statistic in statistics}
        _teacher_questions_subjects_count: dict[str, dict[str, defaultdict[str, int]]] = {
            f"{statistic.subject}": {_class: defaultdict(int) for _class in
                                     QuestionsRange(f"{statistic.subject}", "").get_all_ranges()} for statistic in
            statistics
        }
        _subjects_classes_questions: defaultdict[str, list] = defaultdict(list)
        for statistic in statistics:
            subject: Query[BaseTable] = connect_database_subject(f"{statistic.subject}").session.query(
                SUBJECTS[f"{statistic.subject}"]["base"])
            _teacher_statistics[f"{statistic.firstname} {statistic.lastname}"][f"{statistic.subject}"] += int(
                f"{statistic.questions_value}")

            match f"{statistic.subject}":
                case "english":
                    _subjects_classes_questions[f"{statistic.subject}"].extend(
                        (subject.get(_id).school_class, subject.get(_id).q_block) for _id in
                        statistic.questions_id.split("&") if subject.get(_id)
                    )
                case "reading_comprehension":
                    _subjects_classes_questions[f"{statistic.subject}"].extend(
                        (subject.get(_id).school_class, 1) for _id in statistic.questions_id.split("&") if
                        subject.get(_id)
                    )
                case _:
                    _subjects_classes_questions[f"{statistic.subject}"].extend(
                        (subject.get(_id).school_class, subject.get(_id).q_number) for _id in
                        statistic.questions_id.split("&") if subject.get(_id)
                    )

            # _teacher_questions_subjects_count[f"{statistic.subject}"].extend(map(int, statistic.questions_id.split("&")))

        for _subject in _subjects_classes_questions:
            for pair in _subjects_classes_questions[_subject]:
                _teacher_questions_subjects_count[_subject][pair[0]][pair[1]] += 1

        return render_template(
            "/admin_panel/common_statistics.html",
            len=len,
            teacher_statistics=_teacher_statistics
        )