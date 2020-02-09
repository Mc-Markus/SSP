import requests
import json
from nose.tools import assert_true, assert_false

from ..resources import models as m

# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Local imports...
from constants import BASE_URL_LOCAL

header = {''}
PATH_VARIABLE = 'coachesssp'

def test_login_coach():
    credentials_json = {"username": "medimaatjeadmin", "password": "medimaatjeadmin"}
    response = requests.post(urljoin(BASE_URL, 'login'), json=credentials_json)
    assert_true(response.ok)
    global header 
    header = {"Authorization": "{0}".format(response.text)}


def test_get_coach():
    param = {'id': '1'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)


def test_get_coaches():
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header)
    assert_true(response.ok)
    check_response(response)


def test_get_numberof_coaches():
    param = {'start_index': '1', 'number': '2'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)

def test_get_where-workplace_coaches():
    param = {'workplace': 'haarlem'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    check_response(response)


def check_response(response):
    if response:
        coach_json = response.json()
        for coach_inner in coach_json:
            user = m.User(**{k: coach_inner[0][k] for k in ('date_joined', 'email', 'first_name', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'username') if k in coach_inner[0]})
            coach = m.Coach(**{k: coach_inner[1][k] for k in ('id', 'workplace', 'phone', 'date_of_birth') if k in coach_inner[1]})
            assert_true(user.id >= 0)
            assert_true(coach.id >= 0)


def test_delete_coach():
    response = requests.delete(urljoin(BASE_URL, PATH_VARIABLE), headers=header)
    assert_true(response.ok)
    param = {'self': 'true'}
    response = requests.get(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_false(response.ok)


def test_post_coach():
    param = {'workplace': 'Haarlem', 'phone': '+31600000000', 'date_of_birth': '25-10-1996'}
    response = requests.post(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    if response:
        coach_json = response.json()
        coach_inner = coach_json[0]
        assert_true(coach_inner[1]['id'] > 0)
        assert_true(coach_inner[1]['workplace'] == 'Haarlem')
        assert_true(coach_inner[1]['phone'] == '+31600000000')
        assert_true(coach_inner[1]['date_of_birth'] == '25-10-1996')


def test_put_coach():
    param = {'workplace': 'Amsterdam'}
    param = {'phone': '+31600000001'}
    param = {'date_of_birth': '25-10-1997'}
    response = requests.put(urljoin(BASE_URL, PATH_VARIABLE), headers=header, params=param)
    assert_true(response.ok)
    if response:
        coach_json = response.json()
        coach_inner = coach_json[0]
        assert_true(coach_inner[1]['id'] > 0)
        assert_true(coach_inner[1]['workplace'] == 'Amsterdam')
        ssert_true(coach_inner[1]['phone'] == '+31600000001')
        assert_true(coach_inner[1]['date_of_birth'] == '25-10-1997')


def test_logout_coach():
    response = requests.post(urljoin(BASE_URL, 'logout'), headers=header)
    assert_true(response.ok)