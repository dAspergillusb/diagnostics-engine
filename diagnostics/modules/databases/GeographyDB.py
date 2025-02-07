from sqlalchemy import (
    create_engine,
    Engine,
    Column,
    Integer,
    String,
    Connection
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from diagnostics.modules.types.Types import DataBase


BASE: declarative_base = declarative_base()


class Geography(BASE):
    """
    class base of table for database with questions for geography subject.
    """
    __tablename__: str = "geography"
    id: Column[Integer] = Column(Integer, primary_key=True)
    q_number: Column[Integer] = Column(Integer, nullable=False)
    school_class: Column[String] = Column(String(4), nullable=False)
    q_title: Column[String] = Column(String(30), nullable=False)
    q_text: Column[String] = Column(String(250))
    q_image: Column[String] = Column(String(100))
    q_answer_variants: Column[String] = Column(String(1000), nullable=False)
    q_right_answer: Column[String] = Column(String(50), nullable=False)

    def __str__(self):
        return f"Geography(\nid={self.id},\nnumber={self.q_number},\nclass={self.school_class}\n,title={self.q_title}\n)\n"

    def __repr__(self):
        return f"Geography(\nid={self.id},\nq_number={self.q_number},\n" + \
                f"school_class={self.school_class}\n)\n"

    def get_question(self) -> dict[str, Column[String] | Column[Integer]]:
        return {
            "id": self.id,
            "q_number": self.q_number,
            "q_title": self.q_title,
            "q_text": self.q_text,
            "q_class": self.school_class,
            "q_image": self.q_image,
            "q_answer_variants": self.q_answer_variants,
            "q_right_answer": self.q_right_answer
        }


class GeographyDB(DataBase):
    """
    Class creates or connects to database with questions for tests with geography subject. Class can create new question
    in database.
    """
    def __init__(self, db_name: str = "geography_db"):
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

    def add_question(self, *, q_number: int, q_title: str, q_text: str, school_class: str,
                     q_image: str, q_answer_variants: str,  q_right_answer: str) -> None:
        question: Geography = Geography(
            q_number=q_number,
            q_title=q_title,
            q_text=q_text,
            school_class=school_class,
            q_answer_variants=q_answer_variants,
            q_image=q_image,
            q_right_answer=q_right_answer
        )
        self.session.add(question)
        self.session.commit()


if __name__ == '__main__':
    _question = GeographyDB()
    #for num in range(100):
    #    _question.add_question(
    #        question_number=num,
    #        question_name=f"Problem_{num}",
    #        question_text=f"Solute_problem_{num}",
    #        question_class="9-Б",
    #        question_image="",
    #    )
    for question_num in range(21):
        print(_question.session.query(Geography).all()[question_num].question_name)
