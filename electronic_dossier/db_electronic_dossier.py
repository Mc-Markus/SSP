import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Load, load_only, defer
from ..resources.models import ElectronicDossier, Patient, User
from ..resources.db_connection import request_session

# Function to fetch electronic dossier belonging to the supplied patient's patient_user_id
def fetch_electronic_dossier(p_id):
    try:
        session = request_session()
        query = session.query(ElectronicDossier, Patient)
        query = query.filter(Patient.patient_user_id == p_id) # WHERE patient_user_id = p_id
        query = query.filter(ElectronicDossier.electronic_dossier_id == Patient.electronic_dossier_id) # JOIN on electronic_dossier_id
        query = query.options(Load(ElectronicDossier).load_only("electronic_dossier_id", "summary", "iq")) # only load id, summary and iq
        session.commit()
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False


# Function to update an existing electronic_dossier_id
def update_electronic_dossier(ed_id, new_iq, new_summary):
    try:
        session = request_session()
        query = session.query(ElectronicDossier).filter(ElectronicDossier.electronic_dossier_id == ed_id).first()
        if new_iq is not None:
            query.iq = new_iq
        if new_summary is not None:
            query.summary = new_summary
        session.commit()
        session.close()
        return True
    except SQLAlchemyError:
        return False


# Function to fetch a single patient belonging to the currently logged in coach, based on the supplied patient user id
# Has to be included here due to Python's (lack of) import logic
def fetch_coach_patient_by_id(p_id, c_id):
    try:
        session = request_session()
        query = session.query(Patient, User, ElectronicDossier)
        query = query.filter(Patient.patient_user_id == p_id).filter(Patient.coach_user_id == c_id) # WHERE patient_user_id = p_id AND coach_user_id = c_id
        query = query.filter(Patient.patient_user_id == User.id).filter(Patient.electronic_dossier_id == ElectronicDossier.electronic_dossier_id) # JOINs
        query = query.options(defer(User.password)) # removes passwords from resultset
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False
