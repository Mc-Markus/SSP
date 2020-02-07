import logging
import azure.functions as func
import json

from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data, get_param
from . import service_patients as sp

# Main function gets called when /api/patients is accesed. This function calls and executes the coresponding post/get/update/delete method
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Patients endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_patients(req)
        elif(req.method == "POST" and check_authorization_by_scope(token, 'write')):
            return post_patients(req)
        elif(req.method == "DELETE" and check_authorization_by_scope(token, 'write')):
            return delete_patient(req)
        elif(req.method == "PUT" and check_authorization_by_scope(token, 'write')):
            return put_patient(req)
        else:
            return func.HttpResponse(f"You are not authorized to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with authorization, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for GET requests
def get_patients(req) -> func.HttpResponse:
    try:
        patients_data = sp.get_patients_logic(req)
        if patients_data:
            return func.HttpResponse(json.dumps(prepare_data(patients_data, [['User'], ['Patient']]), indent=4, sort_keys=True, default=str), mimetype='JSON', status_code=200)
        else:
            return func.HttpResponse(f"No patients found", mimetype='text/plain', status_code=404)
    except:
        return func.HttpResponse(f"Something went wrong with GET, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for POST requests
def post_patients(req) -> func.HttpResponse:
    try:
        if sp.post_patients_logic(req) is True:
            return func.HttpResponse(f"Successfully added patient to database.", mimetype='text/plain', status_code=201)
        else:
            return func.HttpResponse(f"Wrong post data or patient already exists. See API documentation for more info.", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with POST, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for PUT requests
def put_patient(req) -> func.HttpResponse:
    try:
        if sp.put_patient_logic(req) is True:
            return func.HttpResponse(f"New coach assigned succesfully", mimetype='text/plain', status_code=200)
        else:
            return func.HttpResponse(f"Patient or coach doesn't exist or JSON is incorrect. See API documentation for more info.", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with PUT, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for DELETE requests
def delete_patient(req) -> func.HttpResponse:
    try:
        return func.HttpResponse(str(sp.delete_patient_logic(req)), mimetype='text/plain', status_code=200)
        if sp.delete_patient_logic(req) is True:
            return func.HttpResponse(f"Patient succesfully removed", mimetype='text/plain', status_code=200)
        else:
            return func.HttpResponse(f"Failed to remove", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with DELETE, modify your request and try again.", mimetype='text/plain', status_code=400)
