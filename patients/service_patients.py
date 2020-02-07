from ..resources.functions_shared import get_param, get_user_id_by_token
from . import db_patients as db

# Business logic to handle /api/patients GET requests
# Works with a coach_user_id and optionally a patient_user_id as query parameters
def get_patients_logic(req):
    # token = req.headers.get("Authorization")
    # current_user_id = get_user_id_by_token(token)

    is_user_patient = get_param(req, 'is_user_patient', 'int')
    patient_user_id = get_param(req, 'patient_user_id', 'int')
    coach_user_id = get_param(req, 'coach_user_id', 'int')

    if is_user_patient == 1 and patient_user_id:
        return db.fetch_patient_by_id(patient_user_id)
    else:    
        if coach_user_id:
            if patient_user_id:
                return db.fetch_coach_patient_by_id(patient_user_id, coach_user_id)
            else:
                return db.fetch_all_patients(coach_user_id)
        else:
            return False
# DONE


# Business logic to handle /api/patients POST requests
# Returns true if supplied JSON body is correct, returns false otherwise
def post_patients_logic(req):
    patient_user_id = get_param(req, 'patient_user_id', 'int')
    coach_user_id = get_param(req, 'coach_user_id', 'int')
    
    body = req.get_json()
    summary = body['electronic_dossier']['summary']
    iq = body['electronic_dossier']['iq']

    try:
        iq = int(iq)
    except TypeError:
        return False

    coach = db.check_if_coach_exists(coach_user_id)
    patient = db.fetch_patient_by_id(patient_user_id)
    if coach and not patient:
        electronic_dossier_id = db.insert_electronic_dossier(summary, iq)
        if electronic_dossier_id:
            db.insert_patient(patient_user_id, coach_user_id, electronic_dossier_id)
            return True
        else:
            return False
    else:
        return False
# DONE


# Business logic to handle /api/patients PUT requests
# Returns True if supplied JSON body is correct, returns False otherwise
def put_patient_logic(req):
    patient_user_id = get_param(req, 'patient_user_id', 'int')
    current_coach_user_id = get_param(req, 'current_coach_user_id', 'int')
    new_coach_user_id = get_param(req, 'new_coach_user_id', 'int')

    # look up patient by supplied ID to see if it exists and belongs to the currently logged in coach
    patient = db.fetch_coach_patient_by_id(patient_user_id, current_coach_user_id)

    if patient:
        # check if supplied new_coach_user_id belongs to an actual coach record
        coach = db.check_if_coach_exists(new_coach_user_id)
        if coach:
            return db.update_patient(patient_user_id, new_coach_user_id)
        else:
            return False
    else:
        return False
# DONE


# Function to delete patient from database
# Automagically deletes related auth_user and electronic_dossier_id entries as well
def delete_patient_logic(req):
    patient_user_id = get_param(req, 'patient_user_id', 'int')
    coach_user_id = get_param(req, 'coach_user_id', 'int')

    patient = db.fetch_coach_patient_by_id(patient_user_id, coach_user_id)

    if patient:
        db.delete_patient_by_id(patient_user_id)
        return True
    else:
        return False
# DONE
