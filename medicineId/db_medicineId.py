from sqlalchemy.orm import sessionmaker
from ..resources.db_connection import db_connect
from ..resources.models import Medicine


# update medicine in db
def put_medicine(id, name, image_path, intake_instruction):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Medicine)
        medicine = query.filter(Medicine.medicine_id == id).first()
        medicine.name = name
        medicine.image_path = image_path
        medicine.description = intake_instruction
        session.commit()
        return True
    except:
        return None


# Get medicine by id
def get_medicine_by_id(id):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Medicine)
    query = query.filter(Medicine.medicine_id == id)

    return query.all()


# delete medicine from db
def delete_medicine(id):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Medicine)
        query = query.filter(Medicine.medicine_id == id)
        query.delete()
        session.commit()
        return True
    except:
        return None
