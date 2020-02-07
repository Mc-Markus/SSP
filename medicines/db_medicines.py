from sqlalchemy.orm import sessionmaker
from ..resources.db_connection import db_connect
from ..resources.models import Medicine

# Get all the medicine in the db with sqlalchemy
def get_all_medicines():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Medicine)

    return query.all()


# Post medicine to db
def post_medicine(name, image_path, intake_instruction):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        medicine = Medicine(name=name, image_path=image_path, description=intake_instruction)
        session.add(medicine)
        session.commit()
        return True
    except:
        return None