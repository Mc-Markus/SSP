from . import db_diseaseid
import azure.functions as func
import logging
import json
from ..resources import functions_shared


# Logistics for the get med by id method of Diseaseprofiles endpoint
def get_diseaseprofile_by_id_logic(req):
    logging.info('diseaseprofiles handeling get request.')
    profile_id = req.route_params.get("diseaseid")
    try:
        int(profile_id)
        c = db_diseaseid.get_diseaseprofiles_by_id(profile_id)
        return func.HttpResponse(
            json.dumps(c, cls=functions_shared.AlchemyEncoder, indent=4, sort_keys=True),
            mimetype='JSON',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            f'Route parameter not a valid input.',
            mimetype='text/plain',
            status_code=400
        )
    except:
        return func.HttpResponse(
            f"Unknown error occurred.",
            mimetype='text/plain',
            status_code=400
        )


# Logistics for the put method of Diseaseprofiles endpoint
def put_diseaseprofile_logic(req):
    logging.info('diseaseprofiles handeling put request.')
    try:
        message = req.get_json()
        profile_id = req.route_params.get("diseaseid")
        int(profile_id)
        name = message['name']
        description = message['description']
        imagepath = message['image_path']
        if db_diseaseid.put_diseaseprofile(profile_id, name, imagepath, description) is not None:
            return func.HttpResponse(
                f'Updated entry to database.',
                mimetype='text/plain',
                status_code=200
            )
    except KeyError:
        return func.HttpResponse(
            f'Body is not valid.',
            mimetype='text/plain',
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            f'No json found in the body',
            mimetype='text/plain',
            status_code=400
        )
    except:
        return func.HttpResponse(
            f"Unknown error occurred.",
            mimetype='text/plain',
            status_code=400
        )


# Logistics for the delete method of Diseaseprofiles endpoint
def delete_diseaseprofile_logic(req):
    logging.info('diseaseprofiles handling delete request.')
    try:
        profile_id = req.route_params.get("diseaseid")
        int(profile_id)
        db_diseaseid.delete_diseaseprofile(profile_id)
        return func.HttpResponse(
            f'Successfully removed entry',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            f'Route parameter not a valid input.',
            status_code=400
        )
    except:
        return func.HttpResponse(
            f"Unknown error occurred.",
            mimetype='text/plain',
            status_code=400
        )