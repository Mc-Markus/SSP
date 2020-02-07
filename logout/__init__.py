import logging
import azure.functions as func
import json
from collections import namedtuple
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    response = post(req)
    return response


def post(req) -> func.HttpResponse:
    logging.info('Logout')
    try:
        token = req.headers.get("Authorization")
        logout(token[7:])
        return func.HttpResponse(
            'Logout succesful',
            status_code=200
        )
    except (KeyError, TypeError) as e:
        return func.HttpResponse(
            'Not a valid token found',
            status_code=400
           )
    except ValueError:
        return func.HttpResponse(
            "Token doesn't exist",
            status_code=400
        )


def logout(token):
    url = "http://medimaatje-oauth.azurewebsites.net/o/revoke_token/"

    payload = "token="+token+"&client_id=123&client_secret=123"

    requests.request("POST", url, data=payload)
