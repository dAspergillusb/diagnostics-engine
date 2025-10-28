from sys import path

from flask import session

path.insert(0, "/home/nikita/PycharmProjects/diagnostics/diagnostics")

from diagnostics.modules.databases import UsersDB, Users


if __name__ == '__main__':
    users = UsersDB()

    for user in users.session.query(Users).all():
        if user.subject:
            if user.username == "zelentsovna":
                user.subject = "информатика&физика&математика"

    users.session.commit()

    print([(user.username, user.subject) for user in users.session.query(Users).all() if user.subject])