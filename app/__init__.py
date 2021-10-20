from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('sqlite:///app/main.db')

metadata = MetaData()

from .models import *
metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
