from typing import Type
from sqlalchemy import (
    create_engine,
    Engine,
    Column,
    Integer,
    String,
    Connection
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session


BASE: declarative_base = declarative_base()


class English(BASE):
    """
    class base of table for database with questions for english subject.
    """
    __tablename__: str = "english"
    id: Column[Integer] = Column(Integer, primary_key=True)
    q_block: Column[Integer] = Column(Integer, nullable=False)
    school_class: Column[String] = Column(String(4), nullable=False)
    q_title: Column[String] = Column(String(30), nullable=False)
    q_audio: Column[String] = Column(String())
    q_text: Column[String] = Column(String(250))
    q_i_1: Column[String] = Column(String(100))
    q_i_2: Column[String] = Column(String(100))
    q_i_3: Column[String] = Column(String(100))
    q_i_4: Column[String] = Column(String(100))
    q_i_5: Column[String] = Column(String(100))
    q_i_6: Column[String] = Column(String(100))
    q_i_7: Column[String] = Column(String(100))
    q_i_8: Column[String] = Column(String(100))
    q_i_9: Column[String] = Column(String(100))
    q_i_10: Column[String] = Column(String(100))
    q_1: Column[String] = Column(String(100))
    q_2: Column[String] = Column(String(100))
    q_3: Column[String] = Column(String(100))
    q_4: Column[String] = Column(String(100))
    q_5: Column[String] = Column(String(100))
    q_6: Column[String] = Column(String(100))
    q_7: Column[String] = Column(String(100))
    q_8: Column[String] = Column(String(100))
    q_9: Column[String] = Column(String(100))
    q_10: Column[String] = Column(String(100))
    q_ans_var_1: Column[String] = Column(String(1000))
    q_ans_var_2: Column[String] = Column(String(1000))
    q_ans_var_3: Column[String] = Column(String(1000))
    q_ans_var_4: Column[String] = Column(String(1000))
    q_ans_var_5: Column[String] = Column(String(1000))
    q_ans_var_6: Column[String] = Column(String(1000))
    q_ans_var_7: Column[String] = Column(String(1000))
    q_ans_var_8: Column[String] = Column(String(1000))
    q_ans_var_9: Column[String] = Column(String(1000))
    q_ans_var_10: Column[String] = Column(String(1000))
    q_right_ans_1: Column[String] = Column(String(50), nullable=False)
    q_right_ans_2: Column[String] = Column(String(50), nullable=False)
    q_right_ans_3: Column[String] = Column(String(50), nullable=False)
    q_right_ans_4: Column[String] = Column(String(50), nullable=False)
    q_right_ans_5: Column[String] = Column(String(50), nullable=False)
    q_right_ans_6: Column[String] = Column(String(50), nullable=False)
    q_right_ans_7: Column[String] = Column(String(50), nullable=False)
    q_right_ans_8: Column[String] = Column(String(50), nullable=False)
    q_right_ans_9: Column[String] = Column(String(50), nullable=False)
    q_right_ans_10: Column[String] = Column(String(50), nullable=False)

    def __str__(self):
        return f"English(\nid={self.id},\nnumber={self.q_block},\nclass={self.school_class}\n,title={self.q_title}\n)\ntext={self.q_text}\n"

    def __repr__(self):
        return f"English(\nid={self.id},\nq_block={self.q_block},\n" + \
                f"school_class={self.school_class}\nq_title={self.q_title})\ntext={self.q_text}\n"


class EnglishDB:
    """
    Class creates or connects to database with question blocks for tests with English subject. Class can create new
    question block in database.
    """
    def __init__(self, db_name: str = "english_db", database_path: str = "database"):
        self.db_name = db_name
        self.database_path = database_path
        self.engine = self._create_engine()
        BASE.metadata.create_all(self.engine)
        BASE.metadata.bind = self.engine
        self.db_session: sessionmaker[[Session]] = sessionmaker(bind=self.engine)
        self.session: Session = self.db_session()

    def _create_engine(self) -> Engine:
        db: Engine = create_engine(f"sqlite:///{self.database_path}/{self.db_name}.db")
        return db

    def _connect(self) -> Connection:
        db_connect: Connection = self.engine.connect()
        return db_connect

    def add_block(self, datas: dict[str, str | int]) -> None:
        question: English = English(
            q_block=datas.get("q_block"),
            school_class=datas.get("school_class"),
            q_title=datas.get("q_title"),
            q_audio=datas.get("q_audio"),
            q_text=datas.get("q_text"),
            q_i_1=datas.get("q_i_1"),
            q_i_2=datas.get("q_i_2"),
            q_i_3=datas.get("q_i_3"),
            q_i_4=datas.get("q_i_4"),
            q_i_5=datas.get("q_i_5"),
            q_i_6=datas.get("q_i_6"),
            q_i_7=datas.get("q_i_7"),
            q_i_8=datas.get("q_i_8"),
            q_i_9=datas.get("q_i_9"),
            q_i_10=datas.get("q_i_10"),
            q_1=datas.get("q_1"),
            q_2=datas.get("q_2"),
            q_3=datas.get("q_3"),
            q_4=datas.get("q_4"),
            q_5=datas.get("q_5"),
            q_6=datas.get("q_6"),
            q_7=datas.get("q_7"),
            q_8=datas.get("q_8"),
            q_9=datas.get("q_9"),
            q_10=datas.get("q_10"),
            q_ans_var_1="&".join(datas.get("q_ans_var_1")) if datas.get("q_right_ans_1") else "",
            q_ans_var_2="&".join(datas.get("q_ans_var_2")) if datas.get("q_right_ans_2") else "",
            q_ans_var_3="&".join(datas.get("q_ans_var_3")) if datas.get("q_right_ans_3") else "",
            q_ans_var_4="&".join(datas.get("q_ans_var_4")) if datas.get("q_right_ans_4") else "",
            q_ans_var_5="&".join(datas.get("q_ans_var_5")) if datas.get("q_right_ans_5") else "",
            q_ans_var_6="&".join(datas.get("q_ans_var_6")) if datas.get("q_right_ans_6") else "",
            q_ans_var_7="&".join(datas.get("q_ans_var_7")) if datas.get("q_right_ans_7") else "",
            q_ans_var_8="&".join(datas.get("q_ans_var_8")) if datas.get("q_right_ans_8") else "",
            q_ans_var_9="&".join(datas.get("q_ans_var_9")) if datas.get("q_right_ans_9") else "",
            q_ans_var_10="&".join(datas.get("q_ans_var_10")) if datas.get("q_right_ans_10") else "",
            q_right_ans_1="&".join(datas.get("q_right_ans_1")) if datas.get("q_right_ans_1") else "&".join(datas.get("q_ans_var_1")),
            q_right_ans_2="&".join(datas.get("q_right_ans_2")) if datas.get("q_right_ans_2") else "&".join(datas.get("q_ans_var_2")),
            q_right_ans_3="&".join(datas.get("q_right_ans_3")) if datas.get("q_right_ans_3") else "&".join(datas.get("q_ans_var_3")),
            q_right_ans_4="&".join(datas.get("q_right_ans_4")) if datas.get("q_right_ans_4") else "&".join(datas.get("q_ans_var_4")),
            q_right_ans_5="&".join(datas.get("q_right_ans_5")) if datas.get("q_right_ans_5") else "&".join(datas.get("q_ans_var_5")),
            q_right_ans_6="&".join(datas.get("q_right_ans_6")) if datas.get("q_right_ans_6") else "&".join(datas.get("q_ans_var_6")),
            q_right_ans_7="&".join(datas.get("q_right_ans_7")) if datas.get("q_right_ans_7") else "&".join(datas.get("q_ans_var_7")),
            q_right_ans_8="&".join(datas.get("q_right_ans_8")) if datas.get("q_right_ans_8") else "&".join(datas.get("q_ans_var_8")),
            q_right_ans_9="&".join(datas.get("q_right_ans_9")) if datas.get("q_right_ans_9") else "&".join(datas.get("q_ans_var_9")),
            q_right_ans_10="&".join(datas.get("q_right_ans_10")) if datas.get("q_right_ans_10") else "&".join(datas.get("q_ans_var_10"))
        )
        self.session.add(question)
        self.session.commit()

    def change_question(self, new_block: int,  q_id: int = None, q_block: int = None) -> bool | None:
        if q_id:
            question: English = self.session.query(English).get(q_id)
        elif q_block:
            question: Type[English] = [q for q in self.session.query(English).all() if q.q_block == q_block][0]
        else:
            return False

        question.q_block = new_block
        self.session.commit()


if __name__ == '__main__':
    _questions = EnglishDB(database_path="../../../database")
    #for num in range(100):
    #    _question.add_question(
    #        question_number=num,
    #        question_name=f"Problem_{num}",
    #        question_text=f"Solute_problem_{num}",
    #        question_class="9-Б",
    #        question_image="",
    #    )
    """for block in _question.session.query(English).all():
        if block.id <= 26:
            _question.session.delete(block)
            _question.session.commit()"""

    _questions.change_question(
        new_block=3,
        q_id=19
    )

    print(_questions.session.query(English).get(19))