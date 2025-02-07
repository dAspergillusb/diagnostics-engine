#from sqlalchemy.orm import co
from diagnostics.modules.databases.EnglishDB import EnglishDB, English
from diagnostics.modules.databases.GeographyDB import GeographyDB, Geography
from diagnostics.modules.databases.InformaticsDB import InformaticsDB, Informatics
from diagnostics.modules.databases.ReadingComprehensionDB import ReadingComprehensionDB
from diagnostics.modules.databases.SocialScienceDB import SocialScienceDB, SocialScience
from diagnostics.modules.types.Types import DataBase
from modules.config import STATISTICS, SUBJECTS
from diagnostics.modules.databases.TeacherStatisticsDB import TeacherStatistics, TeacherStatisticsDB
from diagnostics.modules.databases.UsersStatisticsDB import UsersStatisticsDB
from diagnostics.modules.databases.TeacherStatisticsDB_old import TeacherStatisticsDB as TeacherStatisticsDB_old


def connect_database_subject(subject: str) -> GeographyDB | SocialScienceDB | InformaticsDB | ReadingComprehensionDB | EnglishDB | None:
    """
    Function connects to subject database with questions or questions blocks or tests. It depends on current subject.
    :param subject: This is subject like mathematics or english or physics etc.
    :return: Database Object or None if there is no connection.
    """
    connection: DataBase | ReadingComprehensionDB | EnglishDB | None = None
    if subject in SUBJECTS:
        connection = SUBJECTS[subject]["db"]()
    return connection if connection else None


def connect_database_statistics(base: str) -> TeacherStatisticsDB | UsersStatisticsDB | None:
    connection: TeacherStatisticsDB | UsersStatisticsDB | None = None
    connection = STATISTICS[f"{base}"]["db"]()
    return connection


def migrate_to_new_database_stat(*,
                                 new_base: TeacherStatisticsDB,
                                 old_stat: TeacherStatistics,
                                 question_id: int,
                                 question_value: int = 0
                                 ) -> bool:
    if new_base:
        new_base.add_statistics(
            subject=old_stat.subject,
            questions_value=question_value if question_value else old_stat.questions_value,
            questions_id=question_id,
            firstname=old_stat.firstname,
            lastname=old_stat.lastname,
            date=old_stat.date,
            username=old_stat.username
        )
        return True
    return False


if __name__ == "__main__":
    stat_database: TeacherStatisticsDB = TeacherStatisticsDB_old()
    new_database: TeacherStatisticsDB = TeacherStatisticsDB("teacher_statistics_db_new")
    geo_database: GeographyDB = connect_database_subject("geography")
    social_database: SocialScienceDB = connect_database_subject("social_science")
    inf_database: InformaticsDB = connect_database_subject("informatics")
    english_database: EnglishDB = connect_database_subject("english")
    subjects_list = [
        geo_database.session.query(Geography).all(),
        social_database.session.query(SocialScience).all(),
        inf_database.session.query(Informatics).all(),
        english_database.session.query(English).all()
    ]

    """geography: int = 1
    social_science: int = 1
    informatics: int = 1
    english: int = 1

    for stat in stat_database.session.query(TeacherStatistics_old).all():
        match stat.subject:
            case "geography":
                migrate_to_new_database_stat(new_base=new_database, old_stat=stat, question_id=geography)
                geography += 1
            case "social_science":
                migrate_to_new_database_stat(new_base=new_database, old_stat=stat, question_id=social_science)
                social_science += 1
            case "informatics":
                migrate_to_new_database_stat(new_base=new_database, old_stat=stat, question_id=informatics)
                informatics += 1
            case "english":
                migrate_to_new_database_stat(new_base=new_database, old_stat=stat, question_id=english, question_value=5)
                english += 1"""

    for stat in new_database.session.query(TeacherStatistics).all():
        print(stat.questions_id.split("&"))