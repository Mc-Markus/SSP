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
PATH_MEDLIST = 'medicinelist'

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


# Test to get medicine list, consisting of MedicinePerPatients objects, based on patient user id 3
def test_get_medicine_list():
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE + '/3/' + PATH_MEDLIST), headers=header)
    assert_true(response.ok)
    check_response(response)


# Check contents of response, patient id 3 used
def check_response(response):
    if response:
        medlist_json = response.json()
        for medlist_inner in medlist_json:
            mpp = m.MedicinePerPatient(**{k: medlist_inner[0][k] for k in ('id', 'patient_user_id', 'medicine_id', 'intake_time', 'intake_state', 'dose') if k in medlist_inner[0]})
            assert_true(mpp.id > 0)
            assert_true(mpp.patient_user_id == 3)
            assert_true(mpp.medicine_id > 0)
            assert_true(mpp.intake_state != None)
            assert_true(mpp.intake_time != None)
            assert_true(mpp.dose != None)


# Test to check if new patients can be created
def test_post_medicine_to_medicine_list():
    json_body = {'medicine_id' : '3', 'intake_time' : '2020-12-02 13:00:00', 'intake_state' : 'taken', 'dose' : 'test medicine list post'}
    response = requests.post(urljoin(BASE_URL, PATH_VARIABLE + '/3/' + PATH_MEDLIST), headers=header, json=json_body)
    assert_true(response.ok)


# Test see if deleting a patient works
def test_delete_medicine_from_medicine_list():
    # Change ID to something that exists before executing test
    param = {'id' : '10'}
    response = requests.delete(urljoin(BASE_URL, PATH_VARIABLE + '/3/' + PATH_MEDLIST), headers=header, json=param)
    assert_true(response.ok)


# Test to check if logout works, works the same for patients and coaches
def test_logout_user():
    global header
    response = requests.post(urljoin(BASE_URL, 'logout'), headers=header)
    assert_true(response.ok)
    if(response.ok):
        header = {''}
