from sqlalchemy import *
from sqlalchemy.orm import *
import datetime

engine = create_engine('sqlite:///app/main.db')

metadata = MetaData()

from .models import *
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
