from sqlalchemy import inspect
from ..resources.functions_shared import get_param, get_user_id_by_token
from . import db_electronic_dossier as db

# Business logic to handle /api/patients/{id}/electronicdossier GET requests
# Works with a patient_user_id as route parameter
def get_electronic_dossier_logic(req):
    try:
        patient_user_id = int(req.route_params.get('id'))
        return db.fetch_electronic_dossier(patient_user_id)
    except TypeError:
        return False
# DONE


# Business logic to handle /api/patients/{id}/electronicdossier PUT requests
# Returns True if supplied JSON body is correct, returns False otherwise
def put_electronic_dossier_logic(req):
    try:
        patient_user_id = int(req.route_params.get('id'))
    except TypeError:
        return False
    
    if patient_user_id:
        # check if patient belongs to coach
        token = req.headers.get("Authorization")
        if "earer" in token:
            token = token[7:]
        coach_user_id = get_user_id_by_token(token)
        patient = db.fetch_coach_patient_by_id(patient_user_id, coach_user_id)

        # if db.fetch_coach_patient_by_id(patient_user_id, coach_user_id) returned a record, update the dossier
        if patient:
            electronic_dossier = db.fetch_electronic_dossier(patient_user_id)
            electronic_dossier_id = inspect(electronic_dossier[0][0]).identity
            new_iq = get_param(req, 'new_iq', 'int')
            new_summary = get_param(req, 'new_summary', 'string')
            
            return db.update_electronic_dossier(electronic_dossier_id, new_iq, new_summary)
        else:
            return False
    else:
        return False
# DONE
