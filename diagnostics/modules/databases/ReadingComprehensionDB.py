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


class ReadingComprehension(BASE):
    """
    class base of table for database with questions for Reading Comprehension subject.
    """
    __tablename__: str = "reading_comprehension"
    id: Column[Integer] = Column(Integer, primary_key=True)
    school_class: Column[String] = Column(String(2), nullable=False)
    test_title: Column[String] = Column(String(30), nullable=False)
    test_text: Column[String] = Column(String())
    q_1: Column[String] = Column(String())
    q_2: Column[String] = Column(String())
    q_3: Column[String] = Column(String())
    q_4: Column[String] = Column(String())
    q_5: Column[String] = Column(String())
    q_6: Column[String] = Column(String())
    q_7: Column[String] = Column(String())
    q_8: Column[String] = Column(String())
    q_9: Column[String] = Column(String())
    q_10: Column[String] = Column(String())
    q_11: Column[String] = Column(String())
    q_12: Column[String] = Column(String())
    q_13: Column[String] = Column(String())
    q_14: Column[String] = Column(String())
    q_15: Column[String] = Column(String())
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
    q_i_11: Column[String] = Column(String(100))
    q_i_12: Column[String] = Column(String(100))
    q_i_13: Column[String] = Column(String(100))
    q_i_14: Column[String] = Column(String(100))
    q_i_15: Column[String] = Column(String(100))
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
    q_ans_var_11: Column[String] = Column(String(1000))
    q_ans_var_12: Column[String] = Column(String(1000))
    q_ans_var_13: Column[String] = Column(String(1000))
    q_ans_var_14: Column[String] = Column(String(1000))
    q_ans_var_15: Column[String] = Column(String(1000))
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
    q_right_ans_11: Column[String] = Column(String(50), nullable=False)
    q_right_ans_12: Column[String] = Column(String(50), nullable=False)
    q_right_ans_13: Column[String] = Column(String(50), nullable=False)
    q_right_ans_14: Column[String] = Column(String(50), nullable=False)
    q_right_ans_15: Column[String] = Column(String(50), nullable=False)

    def __str__(self):
        return (f"ReadingComprehension(\n"
                f"id={self.id},\n"
                f"class={self.school_class},\n"
                f"title={self.test_title},\n"
                f")\n")

    def __repr__(self):
        return (f"ReadingComprehension(\n"
                f"id(test_num)={self.id},\n"
                f"school_class={self.school_class},\n"
                f"test_title={self.test_title},\n"
                f")\n")


class ReadingComprehensionDB:
    """
    Class creates or connects to database with questions for tests with Reading Comprehension subject. Class can create
    new question in database.
    """
    def __init__(self, db_name: str = "reading_comprehension_db", database_path: str = "database"):
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

    def add_test(self, datas: dict[str, str]) -> None:
        question: ReadingComprehension = ReadingComprehension(
            school_class=datas.get("school_class"),
            test_title=datas.get("test_title"),
            test_text=datas.get("test_text"),
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
            q_11=datas.get("q_11"),
            q_12=datas.get("q_12"),
            q_13=datas.get("q_13"),
            q_14=datas.get("q_14"),
            q_15=datas.get("q_15"),
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
            q_i_11=datas.get("q_i_11"),
            q_i_12=datas.get("q_i_12"),
            q_i_13=datas.get("q_i_13"),
            q_i_14=datas.get("q_i_14"),
            q_i_15=datas.get("q_i_15"),
            q_ans_var_1=datas.get("q_ans_var_1"),
            q_ans_var_2=datas.get("q_ans_var_2"),
            q_ans_var_3=datas.get("q_ans_var_3"),
            q_ans_var_4=datas.get("q_ans_var_4"),
            q_ans_var_5=datas.get("q_ans_var_5"),
            q_ans_var_6=datas.get("q_ans_var_6"),
            q_ans_var_7=datas.get("q_ans_var_7"),
            q_ans_var_8=datas.get("q_ans_var_8"),
            q_ans_var_9=datas.get("q_ans_var_9"),
            q_ans_var_10=datas.get("q_ans_var_10"),
            q_ans_var_11=datas.get("q_ans_var_11"),
            q_ans_var_12=datas.get("q_ans_var_12"),
            q_ans_var_13=datas.get("q_ans_var_13"),
            q_ans_var_14=datas.get("q_ans_var_14"),
            q_ans_var_15=datas.get("q_ans_var_15"),
            q_right_ans_1=datas.get("q_right_ans_1"),
            q_right_ans_2=datas.get("q_right_ans_2"),
            q_right_ans_3=datas.get("q_right_ans_3"),
            q_right_ans_4=datas.get("q_right_ans_4"),
            q_right_ans_5=datas.get("q_right_ans_5"),
            q_right_ans_6=datas.get("q_right_ans_6"),
            q_right_ans_7=datas.get("q_right_ans_7"),
            q_right_ans_8=datas.get("q_right_ans_8"),
            q_right_ans_9=datas.get("q_right_ans_9"),
            q_right_ans_10=datas.get("q_right_ans_10"),
            q_right_ans_11=datas.get("q_right_ans_11"),
            q_right_ans_12=datas.get("q_right_ans_12"),
            q_right_ans_13=datas.get("q_right_ans_13"),
            q_right_ans_14=datas.get("q_right_ans_14"),
            q_right_ans_15=datas.get("q_right_ans_15")
            )
        self.session.add(question)
        self.session.commit()


if __name__ == '__main__':
    rc = ReadingComprehensionDB(database_path="../../../database").session.query(ReadingComprehension).all()
    #for num in range(100):
    #    _question.add_question(
    #        question_number=num,
    #        question_name=f"Problem_{num}",
    #        question_text=f"Solute_problem_{num}",
    #        question_class="9-Б",
    #        question_image="",
    #    )
    """for attr in dir(rc):
        if not attr.startswith(("_", "reg", "meta")):
            print(attr, getattr(rc, attr))"""
    print(rc)
    for block in rc:
        print(block)