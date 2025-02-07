from sys import argv
from os import path, mkdir
from diagnostics.modules.databases.UsersDB import UsersDB, Users
from diagnostics.modules.functions.is_correct_check import encoding_password
from diagnostics.modules.errors.Errors import ErrorCreateUser


def get_arguments_commandline() -> dict[str, str] | None:
    """
    Function iterates for arguments and generates a variables with needed information about user from commandline
    :return: dictionary with variables needed to create new user at users database
    Args is:
    database_path - is path of database file. Looks like 'database/users...'
    firstname - name of man
    lastname - lastname of man
    sex - male of female
    email - email address (required)
    school_class - school class with format class-char (example 5-А, 8-Б)
    username - unique username (required)
    password - strong password with upper and lower case of chars and digits and special characters !@#$%^&*() (required)
    rank - one of next: student, teacher, admin, visor (required)
    subject - what of subject teacher leads
    """
    if len(argv) == 1:
        return get_minimal_help()
    check_args: str = "".join(argv)
    # check if help needed
    if "help" in check_args:
        return get_help()
    # checks the argv parameters
    assert "username" in check_args, "username parameter is needed to create new user"
    assert "email" in check_args, "email parameter is needed to create new user"
    assert "rank" in check_args, "rank parameter is needed to create new user"
    assert "password" in check_args, "password parameter is needed to create new user"
    args: list[tuple[str, ...]] = [tuple(arg.split("=")) for arg in argv[1:]]

    return {key: value for key, value in args}


def create_user() -> bool | None:
    """
    The function creates the user with rank. For different users ranks may be: teacher, admin, visor, student.

    :return: True if user created successfully, else - raise ErrorCreateUser.
    """
    data: dict[str, str] = get_arguments_commandline()

    if data:
        if data.get("database_path"):
            _path: str = data.get("database_path")
            if not path.exists(_path):
                long_path: list[str] = []
                for _dir in _path.split("/"):
                    long_path.append(_dir)
                    mkdir("/".join(long_path))
            db = UsersDB(database_path=data.get("database_path"))
        else:
            db = UsersDB()
            for user in db.session.query(Users).all():
                if user.username == data.get("username"):
                    print(f"Instance with {data.get('username')} username already exists in users database")
                    return False
        subject: str | None = data.get("subject")
        add: bool = db.add_instance(
            firstname=data.get("username", "User"),
            lastname=data.get("lastname", "User"),
            sex=data.get("sex", "Без пола"),
            email=data.get("email"),
            school_class=data.get("school_class"),
            username=data.get("username"),
            password=encoding_password(data.get("password")),
            rank=data.get("rank"),
            subject=subject.split("#") if subject else None
        )
        if add:
            print("User successfully added to database")
            return True
        raise ErrorCreateUser("There is some problems with adding new user")


def get_help():
    print("""
                         -------It's help string about using add-user-script-------
    
    Script creates an user instance in users database without any checks of validity. To create new user, you need
    to set some parameters:
    
    database_path - is path of database file. Looks like 'database/users/...'
    firstname - name of man
    lastname - lastname of man
    sex - male of female
    email - email address (required)
    school_class - school class with format class-char (example 5-А, 8-Б)
    username - unique username (required)
    password - strong password with upper and lower case of chars and digits and special characters !@#$%^&*() (required)
    rank - one of next: student, teacher, admin, visor (required)
    subject - what of subject teacher leads. subjects is: algebra, geometry, mathematics, biology, chemistry, geography,
              english, history, social_science, russian, reading_comprehension, informatics, physics, literature.
              You need to enter this subjects in russian language, for example математика, русский язык...
    
    The order of parameters doesn't matter. If parameter 'school_class' isn't empty, than the subject parameter must
    be empty! And vice versa. If there is 'school_class' you need to enter the 'student' rank, if 'subject' - teacher
    rank. if rank is 'admin' or 'visor' then doesn't matter what of 'subject' or school_class is. Is count of subjects
    more than one enter subjects separated by '#' sign. For example: geometry#mathematics.
    Required parameters is needed and without its user can't be created in database. Also you can set the database
    filepath using the database_path parameter.
    
    Example of strings:
    add_user.py username=user password=pass13 rank=student email=slim@book.com
    add_user.py database_path=database/users username=user password=pass13 rank=student email=slim@book.com
    add_user.py database_path=database/users firstname=Nikita lastname=Brook sex=Женский school_class=5-Б username=user password=pass13 rank=student email=slim@book.com
    """)


def get_minimal_help():
    print("""
    You need to enter a 'help' parameter to get information about using this script.
    Such as: 'add_user.py help'
    """)


if __name__ == '__main__':
    create_user()
