from datetime import datetime
from flask import (
    render_template,
    url_for,
    request,
    redirect,
    session,
    Response
)
from sqlalchemy import Column, String, Integer
from diagnostics.modules.config import ELEMENTARY_SCHOOL
from .is_correct_check import (
    is_correct_firstname,
    is_correct_lastname,
    is_correct_class,
    is_correct_email,
    is_correct_username,
    is_correct_password,
    encoding_password
)
from diagnostics.modules.ranks import ranks
from diagnostics.modules.databases.UsersDB import Users, UsersDB
from diagnostics.modules.email_engine.EmailSender import EmailSender
from diagnostics.modules.logging.LogEngine import LogingLog
from diagnostics.modules.logging.LogEngine import UsersRegisterLog
from diagnostics.modules.logging.LogEngine import EmailSenderLog


# Functions for login operations
def made_login(user: Users) -> str | Response:
    rank: Column[String] = user.rank
    if not user.active:
        return blocked_user(message="Пользователь заблокирован. Обратитесь к администратору.")

    elif rank in ranks:
        add_log_login(user=user)

        return login(user=user)


def blocked_user(message: str) -> str:
    return render_template(
            "sign_in.html",
            registration_needed=message
        )


def add_log_login(user: Users) -> None:
    LogingLog(
        _date=datetime.now(),
        user_id=user.user_id,
        username=f"{user.username}",
        rank=f"{user.rank}",
        school_class=f"{user.school_class}"
    ).add_log_login()


def login(user: Users) -> Response:
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["rank"] = user.rank
    session["firstname"] = user.firstname
    session["lastname"] = user.lastname
    if user.school_class:
        school_class: Column[String] = user.school_class.split("-")[0]
        session["school_class"] = school_class
        session["school_class_full"] = user.school_class
        return redirect(url_for(ranks[f"{user.rank}"], username=user.username, school_class=school_class))
    elif user.subject:
        session["subjects"] = user.subject
        return redirect(url_for(ranks[f"{user.rank}"], username=user.username))


def check_session_login_failed(message: str) -> str:
    if session.get("login_failed"):
        session["login_failed"] += 1
    else:
        session["login_failed"] = 1
    return render_template(
        "sign_in.html",
        registration_needed=message,
        login_failed=0 if session["login_failed"] <= 3 else 1
    )


# Functions for registration operations
def get_registration_args() -> dict[str, str]:
    subject: list[str] = request.form.getlist("subject")
    rank: str = "teacher" if subject else "student"
    if subject:
        subject = subject if "начальная школа" not in subject else ELEMENTARY_SCHOOL
    return {
        "firstname": request.form.get("firstname"),
        "lastname": request.form.get("lastname"),
        "sex": request.form.get("sex"),
        "email": request.form.get("email"),
        "school_class": request.form.get("school_class"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "rank": rank,
        "subject": subject,
    }


def is_data_correct(
        *,
        firstname: str,
        lastname: str,
        sex: str,
        email: str,
        school_class: str,
        username: str,
        password: str,
        rank: str,
        subject: list[str],
) -> bool:
    print([
        f"{is_correct_firstname(firstname)=}\n",
        f"{is_correct_lastname(lastname)=}\n",
        f"{is_correct_email(email)=}\n",
        f"{is_correct_username(username)=}\n",
        f"{is_correct_class(school_class)=}\n",
        f"{subject=}\n",
        f"{is_correct_password(password)=}\n",
        f"{sex=}\n",
        f"{rank=}"
    ])
    return all(
        (
            is_correct_firstname(firstname),
            is_correct_lastname(lastname),
            is_correct_email(email),
            is_correct_username(username),
            any(
                (
                    is_correct_class(school_class),
                    subject
                )
            ),
            is_correct_password(password),
            sex,
            rank
        )
    )


def add_user_log_email_send(
        *,
        firstname: str,
        lastname: str,
        sex: str,
        email: str,
        school_class: str,
        username: str,
        password: str,
        rank: str,
        subject: list[str],
) -> None:
    rank_to_words: dict[str, str] = {
        "student": "ученик",
        "teacher": "учитель"
    }
    UsersDB().add_instance(
        firstname=firstname,
        lastname=lastname,
        sex=sex,
        email=email,
        school_class=school_class,
        username=username,
        rank=rank,
        subject=subject,
        password=encoding_password(password)
    )
    user_id: Column[Integer] = UsersDB().session.query(Users).all()[-1].user_id
    UsersRegisterLog(
        _date=datetime.now(),
        user_id=user_id,
        username=username,
        rank=rank,
        active=True
    ).add_log_register()

    class_or_subjects: str = f"Ваш класс: {school_class}" if school_class else f"Ваши предметы: {' '.join(subject)}"

    message: str = (
            f"Здравствуйте, {firstname} {lastname}!\nПоздравляем вас с успешной регистрацией в системе диагностик!" +
            f" Вы зарегистрировались в системе с правами {rank_to_words.get(rank)}.\n" +
            "Ваши данные, которые были указаны в форме регистрации:\n\n" +
            f"Имя пользователя: {username}\n" +
            f"Пароль: {password}\n" +
            f"{class_or_subjects}\n\n" +
            "Учтите пожалуйста, что мы не храним ваши пароли в базе в открытом виде,\n" +
            "поэтому рекомендуем вам сохранить это письмо или запомнить ваш пароль."
    )
    successful_registration = EmailSender(
        subject="Успешная регистрация в системе диагностик",
        recipient=email,
        message=message
    )
    successful_registration.send_mail()
    successful_registration.close_connection()

    EmailSenderLog(
        _date=datetime.now(),
        user_id=user_id,
        username=username,
        rank=rank,
        register=True
    ).add_log_send_email()




