import logging
import azure.functions as func
import json
from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data
from . import service_coach as sc

# Main method gets called when /api/coaches is accesed. 
# This method calls and executes the coresponding post/get/update/delete method
# Responds with a JSON/text http response
# Checks if a user is authenticated to execute a specific call
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a Coach request.')
    try:
        token = req.headers.get("Authorization")
        try:
            if req.method == "GET" and check_authorization_by_scope(token, 'read'):
                response = get_coach(req)
            elif req.method == "POST" and check_authorization_by_scope(token, 'write'):
                response = post_coach(req)
            elif req.method == "DELETE" and check_authorization_by_scope(token, 'write'):
                response = delete_coach(req)
            elif req.method == "PUT" and check_authorization_by_scope(token, 'write'):
                response = put_coach(req)
            else:
                response = func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain',
                                             status_code=401)
            return response
        except KeyError:
            return func.HttpResponse(
                'No valid token found',
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            "Token doesn't exist",
            status_code=400
        )
    

# Controller for the GET request, either returns a list with coach(es) or an error
def get_coach(req):
    try:
        return func.HttpResponse(json.dumps(prepare_data(sc.get_coach_logic(req), [['User'], ['Coach']]), indent=4, sort_keys=True, default=str),
                                mimetype='JSON', status_code=200)
    except:
       return func.HttpResponse(f"Coach doesn't exist or parameter incorrect", mimetype='text/plain', status_code=412)


# Controller for the GET request, either returns a list with coach(es) or an error
def post_coach(req):
    try:
        return func.HttpResponse(json.dumps(prepare_data(sc.post_coach_logic(req), [['User'], ['Coach']]), indent=4, sort_keys=True, default=str),
                                 mimetype='JSON', status_code=200)
    except:
        return func.HttpResponse(f"This call needs valid user data to post or the user already exists", mimetype='text/plain', status_code=412)


# Controller for the GET request, either returns succes or an error
def delete_coach(req):
    try:
        sc.delete_coach_logic(req)
        return func.HttpResponse(f"User succesfully removed", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"Failed to remove, provide a valid id as an int", mimetype='text/plain',
                                 status_code=412)


# Controller for the GET request, either returns a list with a coach or an error
def put_coach(req):
    try:
        return func.HttpResponse(json.dumps(prepare_data(sc.put_coach_logic(req), [['User'], ['Coach']]), indent=4, sort_keys=True, default=str),
                                    mimetype='JSON', status_code=200)
    except:
        return func.HttpResponse(f"Failed to update this coach, or invalid parameters",
                                 mimetype='text/plain', status_code=412)