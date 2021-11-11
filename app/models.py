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
            output = self._conjugate_name(repeat_time)
            self.name = f'Раз в {repeat_time} {output}'
        self.next_repetition = datetime.date.today() + datetime.timedelta(days=repeat_time)
        self.repeat_time = repeat_time

    def _conjugate_name(self, repeat_time):
        n = repeat_time % 100
        if 5 <= n <= 20:
            return 'дней'
        n %= 10
        if n == 1:
            return 'день'
        if 2 <= n <= 4:
            return 'дня'

        return 'дней'

    def update_repetition(self):
        if self.repeat_time != 0:
            self.next_repetition += self.repeat_time
        else:
            self.next_repetition += 1



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
