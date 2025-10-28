from base64 import b64encode
from flask import request, session, render_template, redirect, url_for, Response
from werkzeug.datastructures import FileStorage
from ..config import (
    SUBJECTS_NAME_TO_LINK,
    SUBJECTS_RANGES_FOR_CLASS,
    FOR_CARDS_ELEMENTARY,
    FOR_CARDS_JUNIOR,
    FOR_CARDS_MIDDLE,
    FOR_CARDS_SENIOR,
    FOR_CARDS_NINTH,
    TEST_DATA,
    MATHEMATICS_TESTS_TOPICS
)
from ..tests_engine.QuestionsRange import QuestionsRange
from .files_operations import get_test_filepath


# Functions for students
def choose_student_grade(school_class: str) -> tuple[str, dict[int, tuple[str, str, str, str]]]:
    school_class = int(school_class)
    students_grades: dict[bool, tuple[str, dict[int, tuple[str, str, str, str]]]] = {
        school_class < 5: ("student_elementary.html", FOR_CARDS_ELEMENTARY),
        5 <= school_class <= 6: ("student_junior.html", FOR_CARDS_JUNIOR),
        7 <= school_class < 9: ("student_middle.html", FOR_CARDS_MIDDLE),
        school_class == 9: ("student_middle.html", FOR_CARDS_NINTH),
        school_class > 9: ("student_senior.html", FOR_CARDS_SENIOR)
    }
    return students_grades[True]


# Functions for teacher
def get_test_attempt_page(
        username: str,
        firstname: str,
        lastname: str,
        subjects: list[str],
        q_number: str | int = ""
) -> str | Response | None:
    title: str = request.form.get(f"q_title_{q_number}") if q_number else request.form.get("title")
    text: str = request.form.get(f"q_text_{q_number}") if q_number else request.form.get("text")
    answer_variants: list[str] = request.form.getlist(f"q_answer_variants_{q_number}") if q_number else request.form.getlist("answer_variants")
    right_answer: list[str] = request.form.getlist(f"q_right_answer_{q_number}") if q_number else request.form.getlist("right_answer")
    image: FileStorage = request.files.get(f"q_image_{q_number}") if q_number else request.files.get("image")
    image_type: str = f"data:image/{image.filename.split('.')[-1]};base64," if image else ""
    #filepath: str = get_test_filepath()
    if all((title, text,
            any(
                (
                        len(answer_variants) == 1 and not right_answer,
                        len(answer_variants) > 1 and right_answer
                )))):
        TEST_DATA["title"] = title
        TEST_DATA["text"] = text
        TEST_DATA["image"] = b64encode(image.read()).decode()
        TEST_DATA["image_type"] = image_type
        TEST_DATA["answer_variants"] = "&".join(answer_variants) if right_answer else ""
        TEST_DATA["right_answer"] = "&".join(right_answer) if right_answer else "&".join(answer_variants)
        if all((q_number, isinstance(q_number, str))):
            return redirect(url_for("test_view", username=username))
        elif all((q_number, isinstance(q_number, int))):
            return None
        return render_template(
            "/teacher_panel/teacher_panel.html",
            firstname=firstname,
            lastname=lastname,
            username=username,
            subjects=subjects,
            links=SUBJECTS_NAME_TO_LINK,
            modal_success_train=True
        )
    else:
        return render_template(
            "/teacher_panel/teacher_panel.html",
            firstname=firstname,
            lastname=lastname,
            username=username,
            subjects=subjects,
            links=SUBJECTS_NAME_TO_LINK,
            title=title,
            text=text,
            modal_failed_train=True
        )


def get_teacher_panel_main(username: str, input_subject: str) -> str:
    subjects: list[str] = sorted(subject for subject in session["subjects"].split("&"))
    subjects_names: dict[str, str] = {SUBJECTS_NAME_TO_LINK[subject]: "".join((subject[0].title(), subject[1:])) for
                                      subject in
                                      SUBJECTS_NAME_TO_LINK}
    topics_for_math: list[str] = MATHEMATICS_TESTS_TOPICS if input_subject =="mathematics" else None
    firstname: str = session["firstname"]
    lastname: str = session["lastname"]
    session["school_class"] = request.args.get("school_class")
    template: str = "common" if input_subject not in ["english", "reading_comprehension"] else input_subject
    session["topic_for_math"] = request.args.get("topic_for_math")
    return render_template(
        f"/teacher_panel/subjects/teacher_{template}.html",
        firstname=firstname,
        lastname=lastname,
        username=username,
        subjects=subjects,
        links=SUBJECTS_NAME_TO_LINK,
        school_class=session["school_class"],
        subject=subjects_names[input_subject],
        topic_for_math=session["topic_for_math"],
        topics_for_math=topics_for_math,
        session_input=request.form,
        session_files=request.files,
        _range=QuestionsRange(input_subject, session["school_class"]).get_range(),
        _range_classes=SUBJECTS_RANGES_FOR_CLASS
    )




