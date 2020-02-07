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


# Test to get patient object based on patient user id 3
def test_get_patient():
    param = {'is_user_patient': '1', 'patient_user_id' : '3'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)


# Test to get patient object belonging to coach by supplying patient and coach user id
def test_get_coach_patient():
    param = {'is_user_patient': '0', 'patient_user_id' : '3', 'coach_user_id' : '9'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)


# Test to get list of all patients belonging to coach
def test_get_all_patients():
    param = {'is_user_patient': '0', 'coach_user_id' : '9'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)


def check_response(response):
    if response:
        patient_json = response.json()
        for patient_inner in patient_json:
            user = m.User(**{k: patient_inner[0][k] for k in ('date_joined', 'email', 'first_name', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'username') if k in patient_inner[0]})
            patient = m.Patient(**{k: patient_inner[1][k] for k in ('patient_user_id', 'coach_user_id', 'electronic_dossier_id') if k in patient_inner[1]})
            assert_true(user.id >= 0)
            assert_true(patient.patient_user_id >= 0)
            assert_true(patient.coach_user_id >= 0)
            assert_true(patient.electronic_dossier_id >= 0)


# Test to check if new patients can be created
def test_post_patient():
    param = {'patient_user_id': '10', 'coach_user_id': '9', 'electronic_dossier_id' : '10'}
    response = requests.post(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)


# Test see if deleting a patient works
def test_delete_patient():
    json_body = {'patient_user_id' : '10', 'coach_user_id': '9'}
    response = requests.delete(urljoin(BASE_URL, PATH_VARIABLE), headers=header, json=json_body)
    assert_true(response.ok)
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=json_body)
    assert_false(response.ok)


# Test to update a patient
def test_put_patient():
    json_body = {'current_coach_id' : '9', 'patient_user_id' : '10', 'new_coach_user_id': '2'}
    response = requests.put(urljoin(BASE_URL, PATH_VARIABLE), headers=header, json=json_body)
    assert_true(response.ok)


# Test to check if logout works, works the same for patients and coaches
def test_logout_user():
    global header
    response = requests.post(urljoin(BASE_URL, 'logout'), headers=header)
    assert_true(response.ok)
    if(response.ok):
        header = {''}