import logging
import azure.functions as func

from . import service_medicines
from ..resources import authorization as auth


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('medicine triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return service_medicines.get_all_medicines_logic()
        elif req.method == "POST" and auth.check_authorization_by_scope(token, 'write'):
            return service_medicines.post_medicine_logic(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
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
