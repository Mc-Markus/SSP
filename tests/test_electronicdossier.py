import requests
import json
from nose.tools import assert_true, assert_false

from resources import models as m

# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Local imports...
from constants import BASE_URL

header = {''}
PATH_VARIABLE = 'patients'
PATH_ELECDOSS = 'electronicdossier'

# Test for login patient
# This test will get a token for a patient
def test_login_patient():
    credentials_json = {"username": "testpatient1", "password": "h4xx0r123"}
    response = requests.post(urljoin(BASE_URL, 'login'), json=credentials_json)
    assert_true(response.ok)
    global header 
    header = {"Authorization": "{0}".format(response.text)}


# Coaches have access to every endpoint that patients also have access to
# This test will get a token for a coach
def test_login_coach():
    credentials_json = {"username": "testcoach1", "password": "h4xx0r123"}
    response = requests.post(urljoin(BASE_URL, 'login'), json=credentials_json)
    assert_true(response.ok)
    global header 
    header = {"Authorization": "{0}".format(response.text)}


# Test to check if electronic dossier can be retrieved based on patient ID as path parameter
def test_get_electronic_dossier():
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE + '/3/' + PATH_ELECDOSS), headers=header)
    assert_true(response.ok)
    if response:
        electronic_dossier_json = response.json()
        assert_true(len(electronic_dossier_json) > 0)
        ed_test = electronic_dossier_json[0][0]
        assert_true(ed_test['electronic_dossier_id'] > 0)
        assert_true(ed_test['iq'] > 0)
        assert_true(len(ed_test['summary']) > 0)


# Test to check if electronic dossier can be updated, needs patient ID as path parameter
def test_put_electronic_dossier():
    json_body = {'new_summary' : 'nieuwe test summary', 'new_iq' : '69'}
    response = requests.post(urljoin(BASE_URL, PATH_VARIABLE + '/3/' + PATH_ELECDOSS), headers=header, json=json_body)
    assert_true(response.ok)


# Test to check if logout works, works the same for patients and coaches
def test_logout_user():
    global header
    response = requests.post(urljoin(BASE_URL, 'logout'), headers=header)
    assert_true(response.ok)
    if(response.ok):
        header = {''}