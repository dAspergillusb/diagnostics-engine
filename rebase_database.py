from sys import path

path.insert(0, "/home/nikita/PycharmProjects/diagnostics/diagnostics")
path.insert(0, "C:/Users/zelentsovna/PycharmProjects/site/diagnostics")

from diagnostics.modules.databases.UsersStatisticsDB_old import UsersStatistics as U_old
from diagnostics.modules.databases.UsersStatisticsDB_old import UsersStatisticsDB as UDB_old
from diagnostics.modules.databases.UsersStatisticsDB import UsersStatistics as U_new
from diagnostics.modules.databases.UsersStatisticsDB import UsersStatisticsDB as UDB_new
from diagnostics.modules.databases.UsersDB import UsersDB, Users

udb_old = UDB_old(db_name="users_statistics_db_old")
udb_new = UDB_new()
users = {f"{user.username}": user for user in UsersDB().session.query(Users).all() if user.school_class}

for stat in udb_old.session.query(U_old).all():
    if users.get(f"{stat.username}"):
        udb_new.add_statistics(
            subject=stat.subject,
            common_value=stat.common_value,
            common_max_value=stat.common_max_value,
            school_class=stat.school_class,
            common_not_right=stat.common_not_right,
            common_percent=stat.common_percent,
            test_date=stat.test_date,
            user_id=users[f"{stat.username}"].user_id,
            firstname=users[f"{stat.username}"].firstname,
            lastname=users[f"{stat.username}"].lastname
        )
