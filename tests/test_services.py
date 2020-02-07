# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports...
import requests

# Local imports...
from constants import BASE_URL

def do_request(call, parameters, headers, method, jsondata):
    request_url = urljoin(BASE_URL, call)

    if(method == 'get'):
        response = requests.get(request_url, params=parameters, headers=headers, json=jsondata)
    elif(method == 'post'):
        response = requests.post(request_url, params=parameters, headers=headers, json=jsondata)
    elif(method == 'put'):
        response = requests.put(request_url, params=parameters, headers=headers, json=jsondata)
    elif(method == 'delete'):
        response = requests.delete(request_url, params=parameters, headers=headers, json=jsondata)

    if (response.status_code == 200):
        return response
    else:
        return None