from . import db_medicines
import azure.functions as func
import logging
import json
from ..resources import functions_shared


# Logistics for the get method of medicines endpoint
def get_all_medicines_logic():
    logging.info('medicine handeling get request.')
    try:
        c = db_medicines.get_all_medicines()

        return func.HttpResponse(
            json.dumps(c, cls=functions_shared.AlchemyEncoder, indent=4, sort_keys=True),
            mimetype='JSON',
            status_code=200
        )
    except:
        return func.HttpResponse(
            f"Unknown error occurred.",
            mimetype='text/plain',
            status_code=400
        )


# Logistics for the post method of medicines endpoint
def post_medicine_logic(req):
    logging.info('Medicines handeling post request')
    try:
        message = req.get_json()
        name = message['name']
        intakeInstructions = message['intakeInstructions']
        imagepath = message['image_path']
        db_medicines.post_medicine(name, imagepath, intakeInstructions)
        return func.HttpResponse(
            'Added entry to database.',
            mimetype='text/plain',
            status_code=200
        )
    except KeyError:
        return func.HttpResponse(
            'Body is not valid.',
            mimetype='text/plain',
            status_code=412
        )
    except ValueError:
        return func.HttpResponse(
            'No json found in the body',
            mimetype='text/plain',
            status_code=412
        )
    except:
        return func.HttpResponse(
            'unknown error occurred check your implementation.',
            mimetype='text/plain',
            status_code=400
        )
