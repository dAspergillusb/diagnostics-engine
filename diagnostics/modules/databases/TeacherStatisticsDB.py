from sqlalchemy import (
    create_engine,
    Engine,
    Column,
    Integer,
    String,
    Boolean,
    Connection
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from random import randint, choice


BASE = declarative_base()


class TeacherStatistics(BASE):
    __tablename__: str = "teacher_statistics"
    id: Column[Integer] = Column(Integer, primary_key=True)
    subject: Column[String] = Column(String(15), nullable=False)
    username: Column[String] = Column(String(15), nullable=False)
    firstname: Column[String] = Column(String(15))
    lastname:  Column[String] = Column(String(15))
    questions_value: Column[Integer] = Column(Integer)
    questions_id: Column[String] = Column(String)
    date: Column[String] = Column(String(20))

    def __str__(self):
        return (
            f"TeacherStatistics(id={self.id},"
            f" username={self.username},"
            f" subject={self.subject},"
            f" firstname={self.firstname},"
            f" lastname={self.lastname},"
            f" question_value={self.questions_value},"
            f" question_id={self.questions_id}"
            f" date={self.date})"
            )

    def __repr__(self):
        return (
            f"TeacherStatistics(id={self.id},"
            f" username={self.username},"
            f" subject={self.subject},"
            f" firstname={self.firstname},"
            f" lastname={self.lastname},"
            f" question_value={self.questions_value},"
            f" question_id={self.questions_id}"
            f" date={self.date})"
            )


class TeacherStatisticsDB:
    """
    Class creates or connects to database with statistics of teachers questions creation.
    """

    def __init__(self, db_name: str = "teachers_statistics_db"):
        self.db_name = db_name
        self.engine = self._create_engine()
        BASE.metadata.create_all(self.engine)
        BASE.metadata.bind = self.engine
        self.db_session: sessionmaker[[Session]] = sessionmaker(bind=self.engine)
        self.session: Session = self.db_session()

    def _create_engine(self) -> Engine:
        db: Engine = create_engine(f"sqlite:///database/{self.db_name}.db")
        return db

    def _connect(self) -> Connection:
        db_connect: Connection = self.engine.connect()
        return db_connect

    def add_statistics(self, *, subject: str, questions_value: int, questions_id: list[str], firstname: str, lastname: str,
                       date: str, username: str) -> None:
        statistics: TeacherStatistics = TeacherStatistics(
            subject=subject,
            username=username,
            firstname=firstname,
            lastname=lastname,
            questions_value=questions_value,
            questions_id="&".join(questions_id),
            date=date
        )
        self.session.add(statistics)
        self.session.commit()


if __name__ == '__main__':
    _statistics: TeacherStatisticsDB = TeacherStatisticsDB()
    subjects: list[str] = ["informatics", "physics"]
    months: list[str] = [f"{month}" for month in range(1, 13)]
    days: list[str] = [f"{day}" for day in range(1, 28)]
    _teacher_statistics: dict[str, list[int]] = {
        f"2024-" + f"0{month}"[-2:] + "-" + f"0{day}"[-2:]: [randint(1, 15) for _ in range(randint(1, 25))] for month in months for day in days
    }

    for _date in _teacher_statistics:
        for stat in _teacher_statistics[_date]:
            _statistics.add_statistics(
                username="zelentsovna",
                firstname="Никита",
                lastname="Зеленцов",
                subject=choice(subjects),
                questions_value=stat,
                questions_id=["1"],
                date=_date
            )

