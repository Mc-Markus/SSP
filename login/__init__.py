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
    logging.info('login')
    try:
        message = req.get_json()
        username = message['username']
        password = message['password']
        accestoken = login(username,password)
        return func.HttpResponse(
                accestoken,
                status_code=200
            )
    except KeyError:
        return func.HttpResponse(
                'User not found',
                status_code=404
            )
    except:
        return func.HttpResponse(
            'No json found in the body',
            status_code=400
        )


def login(username, password):
    url = "http://medimaatje-oauth.azurewebsites.net/o/token/"

    payload = "grant_type=password&username="+username+"&password="+password+"&client_id=123&client_secret=123"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()
    
    ## LOOK IF ACCESS TOKEN EXISTS, IF NOT 403 UNAUTHORIZED ## 
    try:
        result_tokentype = result["token_type"]
        result_accesstoken = result["access_token"]
        accessToken = str(result_tokentype) + " " + str(result_accesstoken)
        return accessToken
    except TypeError:
        pass