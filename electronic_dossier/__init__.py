import logging
import azure.functions as func
import json

from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data, get_param
from . import service_electronic_dossier as sed

# Main function gets called when /api/patients/{id}/electronicdossier is accessed. This function calls and executes the corresponding get and put methods
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Electronic dossier endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_electronic_dossier(req)
        elif(req.method == "PUT" and check_authorization_by_scope(token, 'write')):
            return put_electronic_dossier(req)
        else:
            return func.HttpResponse(f"You are not authorized to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with authorization, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for GET requests
def get_electronic_dossier(req):
    try:
        electronic_dossier = sed.get_electronic_dossier_logic(req)
        if electronic_dossier:
            return func.HttpResponse(json.dumps(prepare_data(electronic_dossier, [['ElectronicDossier']]), indent=4, sort_keys=True), mimetype='JSON', status_code=200)
        else:
            return func.HttpResponse(f"No electronic dossier found for this patient", mimetype='text/plain', status_code=404)
    except:
        return func.HttpResponse(f"Something went wrong with GET, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for PUT requests
def put_electronic_dossier(req):
    try:
        if sed.put_electronic_dossier_logic(req) is True:
            return func.HttpResponse(f"Electronic dossier updated succesfully", mimetype='text/plain', status_code=200)
        else:
            return func.HttpResponse(f"Electronic dossier doesn't belong to a patient that belongs to the currently logged in coach. See API documentation for more info.", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with PUT, modify your request and try again.", mimetype='text/plain', status_code=400)