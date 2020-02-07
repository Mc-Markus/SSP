import logging

import azure.functions as func
from ..resources import authorization as auth
from . import service_diseaseid


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('diseaseprofiles triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return service_diseaseid.get_diseaseprofile_by_id_logic(req)
        elif req.method == 'PUT' and auth.check_authorization_by_scope(token, 'write'):
            return service_diseaseid.put_diseaseprofile_logic(req)
        elif req.method == 'DELETE' and auth.check_authorization_by_scope(token, 'write'):
            return service_diseaseid.delete_diseaseprofile_logic(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(
            'Not a valid token found',
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            "Token doesn't exist",
            status_code=400
        )
