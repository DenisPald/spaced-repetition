from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

from app import metadata

Base = declarative_base(metadata=metadata)
class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    n_of_box = Column(Integer)

    def __init__(self, question, answer, n_of_box):
        self.question = question
        self.answer = answer
        self.n_of_box = n_of_box
