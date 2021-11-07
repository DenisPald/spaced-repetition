from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
import time
from threading import Thread

engine = create_engine('sqlite:///app/main.db')

metadata = MetaData()

from .models import *
metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

def update_data():
    boxes = session.query(Box)
    for box in boxes:
        if box.next_repetition < datetime.date.today():
            box.next_repetition += datetime.timedelta(days=box.repeat_time)
            session.commit()
    time.sleep(3600)

update_data_thread = Thread(target=update_data)
update_data.start()