from sqlalchemy import *
from sqlalchemy.orm import *
import datetime

engine = create_engine('sqlite:///app/main.db')

metadata = MetaData()

from .models import *
metadata.create_all(engine)
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)
session = Session()
