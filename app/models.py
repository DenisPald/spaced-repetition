import datetime

from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

from app import metadata

Base = declarative_base(metadata=metadata)


class Box(Base):
    __tablename__ = 'boxes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    next_repetition = Column(Date)
    repeat_time = Column(Integer, unique=True)

    def __init__(self, name: str, repeat_time: int):
        self.name = name
        self.next_repetition = datetime.date.today() + datetime.timedelta(days=repeat_time)
        self.repeat_time = repeat_time


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    id_of_box = Column(Integer)

    def __init__(self, question, answer, box: Box):
        self.question = question
        self.answer = answer
        self.id_of_box = box.id
