from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session


BASE: declarative_base = declarative_base()


class DataBase(ABC):
    session: Session

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def _create_engine(self): pass

    @abstractmethod
    def _connect(self): pass

    @abstractmethod
    def add_question(self, *, q_number: int, q_title: str, q_text: str, school_class: str,
                     q_image: str, q_answer_variants: str,  q_right_answer: str) -> None: pass


class BaseTable(BASE):

    __tablename__ = "base_table"
    id: Column[Integer] = Column(Integer, primary_key=True)
    q_number: Column[Integer] = Column(Integer, nullable=False)
    school_class: Column[String] = Column(String(4), nullable=False)
    q_title: Column[String] = Column(String(30), nullable=False)
    q_text: Column[String] = Column(String(250))
    q_image: Column[String] = Column(String(100))
    q_answer_variants: Column[String] = Column(String(1000), nullable=False)
    q_right_answer: Column[String] = Column(String(50), nullable=False)

    def __str__(self): pass

    def __repr__(self): pass

    def get_question(self): pass

