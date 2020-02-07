from sqlalchemy import inspect
from ..resources.functions_shared import get_param
from ..resources.models import MedicinePerPatient
from . import db_medicine_list as db

# Business logic to handle /api/patients/{id}/medicinelist GET requests
# Works with a patient_user_id as route parameter
def get_medicine_list_logic(req):
    try:
        patient_user_id = int(req.route_params.get('id'))
        return db.fetch_medicine_list(patient_user_id)
    except TypeError:
        return False
# Doesn't work


# Business logic to handle /api/patients/{id}/medicinelist POST requests
# Returns True if supplied JSON body is correct, returns False otherwise
def post_medicine_list_logic(req):
    try:
        patient_user_id = int(req.route_params.get('id'))
    except TypeError:
        return False
    
    if patient_user_id:
        meds_to_add = []
        body = req.get_json()
        for item in body:
            mpp = MedicinePerPatient(
                patient_user_id=patient_user_id,
                medicine_id=item['medicine_id'],
                intake_time=item['intake_time'],
                intake_state=item['intake_state'],
                dose=item['dose']
            )
            meds_to_add.append(mpp)

        try:
            for mpp in meds_to_add:
                db.insert_medicine_per_patient(mpp)
            return True
        except:
            return False
    else:
        return False
# DONE


# Business logic to handle /api/patients/{id}/medicinelist DELETE requests
# Deletes medicine_per_patient based on supplied id
def delete_medicine_list_logic(req):
    try:
        patient_user_id = int(req.route_params.get('id'))
    except TypeError:
        return False
    
    if patient_user_id:
        mpp_id = get_param(req, 'id', 'int')
        try:
            db.delete_medicine_per_patient(mpp_id, patient_user_id)
            return True
        except:
            return False
    else:
        return False
# DONE
