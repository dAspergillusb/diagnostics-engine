from diagnostics.modules.databases.UsersDB import UsersDB, Users
from diagnostics.modules.functions.is_correct_check import encoding_password


users = UsersDB()


for num in range(1000):
    school_class = "5-А"
    firstname = f"Name {num}"
    lastname = f"Lastname {num}"
    sex = "Женский"
    email = f"email_{num}@mail.ru"
    username = f"username_{num}"
    password = "Password123$"
    rank = "student"

    users.add_instance(
        firstname=firstname,
        lastname=lastname,
        sex=sex,
        email=email,
        school_class=school_class,
        username=username,
        password=encoding_password(password),
        rank=rank
    )


print(len(users.session.query(Users).all()))