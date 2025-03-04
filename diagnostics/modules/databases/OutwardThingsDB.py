from sqlalchemy import (
    create_engine,
    Engine,
    Column,
    Integer,
    String,
    Connection
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from .._types.Types import DataBase


BASE: declarative_base = declarative_base()


class OutwardThings(BASE):
    """
    class base of table for database with questions for outward things subject.
    """
    __tablename__: str = "outward_things"
    id: Column[Integer] = Column(Integer, primary_key=True)
    q_number: Column[Integer] = Column(Integer, nullable=False)
    school_class: Column[String] = Column(String(4), nullable=False)
    q_title: Column[String] = Column(String(30), nullable=False)
    q_text: Column[String] = Column(String(250))
    q_image: Column[String] = Column(String(100))
    q_answer_variants: Column[String] = Column(String(1000), nullable=False)
    q_right_answer: Column[String] = Column(String(50), nullable=False)

    def __str__(self):
        return f"OutwardThings(\nid={self.id},\nnumber={self.q_number},\nclass={self.school_class}\n,title={self.q_title}\n)\n"

    def __repr__(self):
        return f"OutwardThings(\nid={self.id},\nq_number={self.q_number},\n" + \
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


class OutwardThingsDB(DataBase):
    """
    Class creates or connects to database with questions for tests with outward things subject. Class can create new
    question in database.
    """
    def __init__(self, db_name: str = "outward_things_db"):
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
        question: OutwardThings = OutwardThings(
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
    _question = OutwardThingsDB("../database/mathematics_db")
    #for num in range(100):
    _question.add_question(
            q_number=9,
            q_title="Вычислите значение выражения",
            q_text="21,3 - 2,07",
            school_class="5",
            q_image="",
            q_answer_variants="",
            q_right_answer="19,23"
    )
    _question.add_question(
        q_number=10,
        q_title="Вычислите",
        q_text="Сколько квадратных сантиметров в 4 м^2?",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="40000"
    )
    _question.add_question(
        q_number=11,
        q_title="Вычислите",
        q_text="Ручка стоит 42 рубля. Какое наибольшее количество ручек можно купить на 500 рублей?",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="11"
    )
    _question.add_question(
        q_number=12,
        q_title="Вычислите значание выражения",
        q_text="305 ∙ 14 + 3690 : 18",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="4475"
    )
    _question.add_question(
        q_number=13,
        q_title="Решите задачу",
        q_text="Туристы за 4 дня прошли расстояние от города А до города Б. Каждый день они проходили на 4 км меньше, чем в предыдущий день." +
                " Найдите расстояние между городами А и Б, если в третий день туристы прошли 22 км." +
                " Ответ дайте в километрах.",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="96"
    )
    _question.add_question(
        q_number=14,
        q_title="Решите задачу",
        q_text="В школе 60 пятиклассников, каждый из которых изучает ровно один иностранный язык." +
               " Пятая часть из них изучает французский язык, четвёртая часть – испанский язык." +
               " Остальные пятиклассники изучают английский язык." +
               " Сколько пятиклассников изучает английский язык?",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="33"
    )
    _question.add_question(
        q_number=15,
        q_title="Решите задачу",
        q_text="Расстояние между городами 360 км. Из этих городов одновременно навстречу друг другу выехали два" +
               " автомобиля. Ровно через 2 часа 40 минут после выезда автомобили встретились." +
               " Найдите скорость первого автомобиля (в км/ч), если скорость второго равна 70 км/ч.",
        school_class="5",
        q_image="",
        q_answer_variants="",
        q_right_answer="65"
    )
    _question.add_question(
        q_number=16,
        q_title="Решите задачу",
        q_text="Квадрат разрезали на два равных прямоугольника." +
               "Найдите площадь квадрата, если периметр прямоугольника равен 48 см. Ответ дайте в квадратных сантиметрах.",
        school_class="5",
        q_image="",
        q_answer_variants="256&512&312&45",
        q_right_answer="256&512"
    )
    for question_num in range(17):
        print(_question.session.query(OutwardThings).all())
