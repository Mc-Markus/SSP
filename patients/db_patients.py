import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from ..resources.models import Patient, User, ElectronicDossier, Coach
from ..resources.db_connection import request_session

# Function to fetch all patients belonging to the currently logged in coach
# Joins Patient.patient_user_id on User.id and Patient.electronic_dossier_id on ElectronicDossier.electronic_dossier_id
def fetch_all_patients(c_id):
    try:
        session = request_session()
        query = session.query(Patient, User, ElectronicDossier)
        query = query.filter(Patient.coach_user_id == c_id) # WHERE coach_user_id = c_id
        query = query.filter(Patient.patient_user_id == User.id).filter(Patient.electronic_dossier_id == ElectronicDossier.electronic_dossier_id) # JOINs
        query = query.options(defer(User.password)) # removes passwords from resultset
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False


# Function to fetch a single patient belonging to the currently logged in coach, based on the supplied patient user id
# Joins Patient.patient_user_id on User.id and Patient.electronic_dossier_id on ElectronicDossier.electronic_dossier_id
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


# Function to fetch patient record if the user is the patient itself
def fetch_patient_by_id(p_id):
    try:
        session = request_session()
        query = session.query(Patient, User, ElectronicDossier)
        query = query.filter(Patient.patient_user_id == p_id) # WHERE patient_user_id = p_id
        query = query.filter(Patient.patient_user_id == User.id).filter(Patient.electronic_dossier_id == ElectronicDossier.electronic_dossier_id) # JOINs
        query = query.options(defer(User.password)) # removes passwords from resultset
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False

# Function to insert a new patient record into the database
# Requires three IDs:
# - patient_user_id (as a user object has to already exist)
# - coach_user_id (which is the currently logged in coach's user id) 
# - an electronic_dossier_id, obtained as a return value from insert_electronic_dossier
def insert_patient(p_id, c_id, ed_id):
    try:
        session = request_session()
        patient = Patient(patient_user_id=p_id, coach_user_id=c_id, electronic_dossier_id=ed_id)
        session.add(patient)
        session.commit()
        session.close()
        return True
    except SQLAlchemyError:
        return False


# Function to update an existing patient record
# Requires the targeted patient_user_id and new_coach_user_id (which is the only field to be edited, currently)
def update_patient(p_id, new_c_id):
    try:
        session = request_session()
        query = session.query(Patient).filter(Patient.patient_user_id == p_id).first()
        query.coach_user_id = new_c_id
        session.commit()
        session.close()
        return True
    except SQLAlchemyError:
        return False


# Function to delete an existing patient record based on the supplied patient_user_id
# Electronic dossier and auth_user objects should be deleted due to ON DELETE CASCADE settings
def delete_patient_by_id(p_id):
    try:
        session = request_session()
        session.query(Patient).filter(Patient.patient_user_id == p_id).delete()
        session.commit()
        session.close()
        return True
    except SQLAlchemyError:
        return False


# Function to insert a new electronic dossier record in the database
# Inserts a summary and IQ
def insert_electronic_dossier(summ, ed_iq):
    try:
        session = request_session()
        electronic_dossier = ElectronicDossier(summary=summ, iq=ed_iq)
        session.add(electronic_dossier)
        session.flush()
        ed_id = electronic_dossier.electronic_dossier_id
        session.commit()
        session.close()
        return ed_id
    except SQLAlchemyError:
        return False


# Check if supplied user id belongs to a coach
def check_if_coach_exists(c_id):
    try:
        session = request_session()
        query = session.query(Coach).filter(Coach.id == c_id)
        result = query.all()
        session.close()
        return result
    except SQLAlchemyError:
        return False
