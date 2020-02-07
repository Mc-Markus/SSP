from . import db_medicineId
import azure.functions as func
import logging
import json
from ..resources import functions_shared


# Logistics for the get med by id method of medicines endpoint
def get_medicine_by_id_logic(req):
    logging.info('medicine handling get request.')
    try:
        med_id = req.route_params.get("medicineid")
        int(med_id)
        c = db_medicineId.get_medicine_by_id(med_id)
        return func.HttpResponse(
            json.dumps(c, cls=functions_shared.AlchemyEncoder, indent=4, sort_keys=True),
            mimetype='JSON',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            mimetype='text/plain',
            status_code=400
        )
    except:
        return func.HttpResponse(
            'unknown error occurred check your implementation.',
            mimetype='text/plain',
            status_code=400
        )


# Logistics for the put method of medicines endpoint
def put_medicine_logic(req):
    logging.info('medicine handling put request.')
    try:
        message = req.get_json()
        med_id = req.route_params.get("medicineid")
        int(med_id)
        name = message['name']
        description = message['intakeInstructions']
        image_path = message['image_path']
        if db_medicineId.put_medicine(med_id, name, image_path, description) is not None:
            return func.HttpResponse(
                f'Updated entry to database.',
                status_code=200
            )
        else:
            return func.HttpResponse(
                f'Could not inject new data in db.',
                status_code=400
            )
    except KeyError:
        return func.HttpResponse(
            f'Body is not valid.',
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            f'No json found in the body',
            status_code=400
        )
    except:
        return func.HttpResponse(
            f'Unknown error occurred check your implementation.',
            mimetype='text/plain',
            status_code=400
        )


# Logistics for the delete method of medicines endpoint
def delete_medicine_logic(req):
    logging.info('medicine handeling delete request.')
    try:
        med_id = req.route_params.get("medicineid")
        int(med_id)
        db_medicineId.delete_medicine(med_id)
        return func.HttpResponse(
            'Successfully removed entry from database',
            mimetype='text/plain',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            mimetype='text/plain',
            status_code=400
        )
    except:
        return func.HttpResponse(
            'unknown error occurred check your implementation.',
            mimetype='text/plain',
            status_code=400
        )
