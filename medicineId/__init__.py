import logging

import azure.functions as func
from ..resources import authorization as auth
from . import service_medicineid


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('medicine triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return service_medicineid.get_medicine_by_id_logic(req)
        elif req.method == 'PUT' and auth.check_authorization_by_scope(token, 'write'):
            return service_medicineid.put_medicine_logic(req)
        elif req.method == 'DELETE' and auth.check_authorization_by_scope(token, 'write'):
            return service_medicineid.delete_medicine_logic(req)
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
