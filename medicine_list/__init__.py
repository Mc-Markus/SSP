import logging
import azure.functions as func
import json

from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data, get_param
from . import service_medicine_list as sml

# Main function gets called when /api/patients is accesed. This function calls and executes the coresponding post/get/update/delete method
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Medicine list endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_medicine_list(req)
        elif(req.method == "POST" and check_authorization_by_scope(token, 'write')):
            return post_medicine_list(req)
        elif(req.method == "DELETE" and check_authorization_by_scope(token, 'write')):
            return delete_medicine_list(req)
        else:
            return func.HttpResponse(f"You are not authorized to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)
    except:
        return func.HttpResponse(f"Something went wrong with authorization, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for GET requests
def get_medicine_list(req):
    try:
        medicine_list = sml.get_medicine_list_logic(req)
        # comment the following line to test the call properly, uncomment it to see the content of medicine_list
        return func.HttpResponse(str(medicine_list), mimetype='text/plain', status_code=400)
        if medicine_list:
            # the following SHOULD work but it actually doesn't for some reason
            return func.HttpResponse(json.dumps(prepare_data(medicine_list, [['MedicinePerPatient']]), indent=4, sort_keys=True), mimetype='JSON', status_code=200)
        else:
            return func.HttpResponse(f"No medicine list found for this patient", mimetype='text/plain', status_code=404)
    except:
        return func.HttpResponse(f"Something went wrong with GET, modify your request and try again.", mimetype='text/plain', status_code=400)
    

# Handler for POST requests
def post_medicine_list(req):
    try:
        if sml.post_medicine_list_logic(req) is True:
            return func.HttpResponse(f"Entries successfully added to medicine list", mimetype='text/plain', status_code=200)
        else:
            return func.HttpResponse(f"No medicine list found for this patient", mimetype='text/plain', status_code=404)
    except:
        return func.HttpResponse(f"Something went wrong with POST, modify your request and try again.", mimetype='text/plain', status_code=400)


# Handler for DELETE requests
def delete_medicine_list(req):
    try:
        if sml.delete_medicine_list_logic(req) is True:
            return func.HttpResponse(f"Entries successfully removed from medicine list", mimetype='text/plain', status_code=200)
        else:
            return func.HttpResponse(f"No medicine list found for this patient", mimetype='text/plain', status_code=404)
    except:
        return func.HttpResponse(f"Something went wrong with DELETE, modify your request and try again.", mimetype='text/plain', status_code=400)