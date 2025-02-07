from os import path, mkdir
from sqlalchemy import Column, String
from diagnostics.modules.databases.UsersDB import Users, UsersDB
from diagnostics.modules.databases.ReadingComprehensionDB import ReadingComprehensionDB
from diagnostics.modules.databases.EnglishDB import EnglishDB
from diagnostics.modules.databases.TeacherStatisticsDB import TeacherStatisticsDB
from diagnostics.modules.databases.UsersStatisticsDB import UsersStatisticsDB
from diagnostics.modules.types.Types import DataBase
from diagnostics.modules.config import SUBJECTS, STATISTICS
from diagnostics.modules.ranks import ranks



def connect_database_users() -> UsersDB:
    """
    Function connects users database who registered in system.
    :return: UsersDB object with all users
    """
    if not path.exists("database"):
        mkdir("database")
    users: UsersDB = UsersDB()
    return users


def connect_database_subject(subject: str) -> DataBase | ReadingComprehensionDB | EnglishDB | None:
    """
    Function connects to subject database with questions or questions blocks or tests. It depends on current subject.
    :param subject: This is subject like mathematics or english or physics etc.
    :return: Database Object or None if there is no connection.
    """
    connection: DataBase | ReadingComprehensionDB | EnglishDB | None = None
    if subject in SUBJECTS:
        connection = SUBJECTS[subject]["db"]()
    return connection if connection else None


def connect_database_statistics(rank: Column[String]) -> TeacherStatisticsDB | UsersStatisticsDB | None:
    connection: TeacherStatisticsDB | UsersStatisticsDB | None = None
    if rank in ranks:
        connection = STATISTICS[f"{rank}"]["db"]()
    return connection
