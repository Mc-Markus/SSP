import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer, Load
from ..resources.models import MedicinePerPatient, Medicine, Patient, User
from ..resources.db_connection import request_session

# Function to fetch medicine list belonging to the supplied patient's patient_user_id
def fetch_medicine_list(p_id):
    try:
        session = request_session()
        query = session.query(MedicinePerPatient)
        query = query.filter(MedicinePerPatient.patient_user_id == p_id)
        query = query.options(defer(MedicinePerPatient.intake_state), defer(MedicinePerPatient.intake_time))
        # query = query.filter(Patient.patient_user_id == MedicinePerPatient.patient_user_id).filter(Medicine.medicine_id == MedicinePerPatient.medicine_id)
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False


def insert_medicine_per_patient(mpp):
    try:
        session = request_session()
        session.add(mpp)
        session.commit()
        session.close()
    except SQLAlchemyError:
        return False


# Remove coach from db
def delete_medicine_per_patient(mpp_id, p_id):
    try:
        session = request_session()
        query = session.query(MedicinePerPatient).filter(MedicinePerPatient.id==mpp_id).filter(MedicinePerPatient.patient_user_id==p_id)
        query.delete()
        session.commit()
        session.close()
    except SQLAlchemyError:
        return False