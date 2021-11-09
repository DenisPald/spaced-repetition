import datetime
from typing import Union

from sqlalchemy import Column, Date, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

from app import metadata

Base = declarative_base(metadata=metadata)


class Box(Base):
    __tablename__ = 'boxes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    next_repetition = Column(Date, nullable=False)
    repeat_time = Column(Integer, nullable=False, unique=True)

    def __init__(self, repeat_time: int, custom_name: Union[str, None] = None):
        if custom_name is not None:
            self.name = custom_name
        else:
            self.name = f'Раз в {repeat_time} дней'
        self.next_repetition = datetime.date.today() + datetime.timedelta(days=repeat_time)
        self.repeat_time = repeat_time


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    id_of_box = Column(Integer, nullable=False)

    def __init__(self, question, answer, box: Box):
        self.question = question
        self.answer = answer
        self.id_of_box = box.id

    def update_box(self, box: Box):
        self.id_of_box = box.id

    def update_answer(self, answer: str):
        self.answer = answer

    def update_question(self, question: str):
        self.question = question
