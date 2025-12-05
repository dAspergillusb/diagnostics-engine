from flask import (
    Flask,
    Response,
    session,
    redirect,
    url_for,
    render_template,
)
from ..functions import choose_student_grade
from ..config import MATHEMATICS_TESTS_TOPICS


def register_student_pages(main: Flask) -> None:
    """
    Functions registers endpoints to student pages.
    :param main: Flask
    :return: None
    """
    @main.route("/student/<username>")
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

    @main.route("/<subject>/topics_for_mathematics", methods=["GET", "POST"])
    def get_topics_math(subject: str):
        if all((session.get("user_id"), session.get("rank") in ("student", "teacher"))):
            return render_template(
                "topics_math/topics_math.html",
                firstname=session.get("firstname"),
                lastname=session.get("lastname"),
                topics=MATHEMATICS_TESTS_TOPICS
            )

    @main.route("/testing_result", methods=["GET", "POST"])
    def testing_result():
        if session.get("rank", None) == "student":
            return render_template("testing_result.html",
                                   firstname=session.get("firstname", None),
                                   lastname=session.get("lastname", None)
                                   )
        return redirect(url_for("login"))