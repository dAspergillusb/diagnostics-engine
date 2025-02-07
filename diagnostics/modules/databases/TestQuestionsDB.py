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


BASE: declarative_base = declarative_base()


class TestQuestions(BASE):

    __tablename__: str = "questions"
    question_id: Column[Integer] = Column(Integer, primary_key=True)
    question_number: Column[Integer] = Column(Integer, nullable=False)
    question_class: Column[String] = Column(String(4), nullable=False)
    question_subject: Column[String] = Column(String(20), nullable=False)
    question_name: Column[String] = Column(String(30), nullable=False)
    question_text: Column[String] = Column(String(250))
    question_image: Column[String] = Column(String(100))
    question_right_answer: Column[String] = Column(String(50), nullable=False)

    def __str__(self):
        return f"TestQuestions(\nid={self.question_id},\nnumber={self.question_number},\nclass={self.question_class}\n)\n"

    def __repr__(self):
        return f"TestQuestions(\nquestion_id={self.question_id},\nquestion_number={self.question_number},\n" + \
                f"question_class={self.question_class}\n)\n"

    def get_question(self) -> dict[str, Column[String] | Column[Integer]]:
        return {
            "question_id": self.question_id,
            "question_number": self.question_number,
            "question_name": self.question_name,
            "question_text": self.question_text,
            "question_class": self.question_class,
            "question_image": self.question_image,
            "question_right_answer": self.question_right_answer
        }


class TestQuestionsDB:

    def __init__(self, db_name: str = "test_questions_db"):
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

    """def exist_username(self, username: str) -> bool:
        db_users = set(user.username for user in self.session.query(Users).all())
        if username in db_users:
            return True
        return False"""

    def add_question(self, *, question_number: int, question_name: str, question_text: str, question_class: str,
                     question_subject: str, question_image: str, question_right_answer: str) -> None:
        question = TestQuestions(
            question_number=question_number,
            question_name=question_name,
            question_text=question_text,
            question_class=question_class,
            question_subject=question_subject,
            question_image=question_image,
            question_right_answer=question_right_answer
        )
        self.session.add(question)
        self.session.commit()


if __name__ == '__main__':
    _question = TestQuestionsDB()
    #for num in range(100):
    #    _question.add_question(
    #        question_number=num,
    #        question_name=f"Problem_{num}",
    #        question_text=f"Solute_problem_{num}",
    #        question_class="9-Б",
    #        question_image="",
    #    )
    for question_num in range(21):
        print(_question.session.query(TestQuestions).all()[question_num].question_name)
