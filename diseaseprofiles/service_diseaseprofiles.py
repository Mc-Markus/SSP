from . import db_diseaseprofiles
import azure.functions as func
import logging
import json
from ..resources import functions_shared


# Logistics for the get method of Diseaseprofiles endpoint
def get_all_diseaseprofiles_logic():
    logging.info('Diseaseprofiles handling get request.')
    try:
        c = db_diseaseprofiles.get_all_diseaseprofiles()

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


# Logistics for the post method of Diseaseprofiles endpoint
def post_diseaseprofile_logic(req):
    logging.info('Diseaseprofiles handling post request')
    try:
        message = req.get_json()
        try:
            name = message['name']
            description = message['description']
            imagepath = message['image_path']
            db_diseaseprofiles.post_diseaseprofile(name, imagepath, description)
            return func.HttpResponse(
                'Added entry to database.',
                mimetype='text/plain',
                status_code=200
            )
        except KeyError:
            return func.HttpResponse(
                'Body is not valid.',
                mimetype='text/plain',
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            'No json found in the body',
            mimetype='text/plain',
            status_code=400
        )
    except:
        return func.HttpResponse(
            f"Unknown error occurred.",
            mimetype='text/plain',
            status_code=400
        )
