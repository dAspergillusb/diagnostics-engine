from typing import Type
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
from .TestQuestionsDB import TestQuestions, TestQuestionsDB
from random import randint

BASE = declarative_base()


class Tests(BASE):
    __tablename__: str = "tests"
    test_id: Column[Integer] = Column(Integer, primary_key=True)
    test_class: Column[String] = Column(String(4), nullable=False)
    test_subject: Column[String] = Column(String(15), nullable=False)
    test_name: Column[String] = Column(String(25), nullable=False)
    test_description: Column[String] = Column(String(150))  # Description of test
    test_image: Column[String] = Column(String(100))  # Path to an image for test in static folder

    def __str__(self):
        return f"Tests(id={self.test_id}, class={self.test_class}, subject={self.test_subject}, " + \
            f"name={self.test_name})"

    def __repr__(self):
        return f"Tests(test_id={self.test_id}, test_class={self.test_class}, test_subject={self.test_subject}" + \
            f"test_name={self.test_name})"


class TestsDB:

    def __init__(self, db_name: str = "tests_db"):
        self.db_name = db_name
        self.engine = self._create_engine()
        BASE.metadata.create_all(self.engine)
        BASE.metadata.bind = self.engine
        self.db_session: sessionmaker[[Session]] = sessionmaker(bind=self.engine)
        self.session: Session = self.db_session()
        self.questions: TestQuestionsDB = TestQuestionsDB()

    def _create_engine(self) -> Engine:
        db: Engine = create_engine(f"sqlite:///database/{self.db_name}.db")
        return db

    def _connect(self) -> Connection:
        db_connect: Connection = self.engine.connect()
        return db_connect

    def generate_test_variant(self, _class: str):
        question_number: int = 1
        questions: list[Type[TestQuestions]] = self.questions.session.query(TestQuestions).all()
        while question_number <= 20:
            question_variants: list[Type[TestQuestions]] = [question for question in questions if
                                                            question.question_name == question_number and
                                                            question.question_class[0] == _class]
            yield question_variants[randint(0, len(question_variants) - 1)]
            question_number += 1

    """def exist_username(self, username: str) -> bool:
        db_users = set(user.username for user in self.session.query(Users).all())
        if username in db_users:
            return True
        return False

    def add_instance(self, *, firstname: str, lastname: str, sex: str, email: str, school_class: str, username: str, password: str) -> None:
        user = Users(
            firstname=firstname,
            lastname=lastname,
            sex=sex,
            email=email,
            school_class=school_class,
            username=username,
            password=password
        )
        self.session.add(user)
        self.session.commit()"""
