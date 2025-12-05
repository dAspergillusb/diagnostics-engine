from datetime import datetime
from flask import (
    Flask,
    Response,
    request,
    redirect,
    render_template,
    url_for,
    session
)
from ..databases import Users, UsersDB
from ..email_engine import EmailSender
from ..log import LogingLog
from ..functions import (
    connect_database_users,
    check_session_login_failed,
    made_login,
    get_registration_args,
    is_data_correct,
    encoding_password,
    add_user_log_email_send,
    check_link_time,
    create_date_stamp,
    is_correct_password
)
from ..config import (
    SUBJECTS_NAME_TO_LINK,
    ICON_BLACK,
    HOST
)


def register_main_pages(main: Flask) -> None:
    """
    A function that register endpoints to main pages.
    :param main: Flask
    :return: None
    """
    @main.route("/")
    def home_page() -> Response:
        """
        Function redirects to login page.
        :return: None
        """
        return redirect(url_for("login"))

    @main.route("/login", methods=["GET", "POST"])
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

    @main.route("/registration", methods=["GET", "POST"])
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

    @main.route("/register_teacher", methods=["GET", "POST"])
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

            registration_args: dict[str, str] = get_registration_args()

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

    @main.route("/restore_password", methods=["GET", "POST"])
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
                message: str = (
                            f"Здравствуйте, {firstname} {lastname}!\nВы запросили восстановление пароля для системы" +
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

    @main.route("/new_password", methods=["GET", "POST"])
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

    @main.route("/delete_user_submit")
    def delete_user_submit():
        username = session.get("username", None)
        return render_template("delete_user_submit.html", username=username)

    @main.route("/logout")
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

