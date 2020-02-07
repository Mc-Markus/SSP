from nose.tools import assert_true, assert_false
from constants import HEADER, BASE_URL
from urllib.parse import urljoin

# Third-party imports...
import requests
import time


timestamp_diseaseprofile_test = time.time()
disease_posted_id = 0
PATH_VARIABLE = 'diseaseprofiles'
LOCAL_URL = BASE_URL


# Test post function of diseaseprofile
def test_post_diseaseprofile():
    param = {'name': str(timestamp_diseaseprofile_test), 'image_path': 'functestimg', 'description': 'functestintake'}
    response = requests.post(urljoin(LOCAL_URL, PATH_VARIABLE), json=param, headers=HEADER)
    assert response.status_code == 200
    print("Posting diseaseprofile success")
    response = requests.get(urljoin(LOCAL_URL, PATH_VARIABLE))
    assert response.status_code == 200
    if response:
        diseaseprofile_json = response.json()
        posted_profile = max(diseaseprofile_json, key=lambda ev: ev['disease_profile_id'])
        assert_true(posted_profile['disease_profile_id'] >= 1)
        assert_true(posted_profile['name'] == str(timestamp_diseaseprofile_test))
        assert_true(posted_profile['image_path'] == 'functestimg')
        assert_true(posted_profile['description'] == 'functestintake')
        global disease_posted_id
        disease_posted_id = posted_profile['disease_profile_id']
        print("Found inserted diseaseprofile, post test success")


# Func test for validating diseaseprofiles get
def test_get_diseaseprofiles():
    response = requests.get(LOCAL_URL + PATH_VARIABLE)
    assert response.status_code == 200
    if response:
        diseaseprofile_json = response.json()
        for diseaseprofile_inner in diseaseprofile_json:
            assert_true(diseaseprofile_inner['disease_profile_id'] >= 1)
    print("Get diseaseprofiles test success.")


# Test get diseaseprofile by id
def test_get_diseaseprofile_by_id():
    assert_true(disease_posted_id > 0, "Posted id should be more than 0, the post method has failed to insert the right id.")
    response = requests.get(LOCAL_URL + PATH_VARIABLE + '/' + str(disease_posted_id))
    assert response.status_code == 200
    if response:
        diseaseprofile_json = response.json()
        assert_true(len(diseaseprofile_json) > 0)
        profile_test = diseaseprofile_json[0]
        assert_true(profile_test['disease_profile_id'] == disease_posted_id)
        assert_true(profile_test['name'] == str(timestamp_diseaseprofile_test))
        assert_true(profile_test['image_path'] == 'functestimg')
        assert_true(profile_test['description'] == 'functestintake')
        print("Get diseaseprofile by id tested successfully.")


# Test insertion of new diseaseprofile information in existing entry
def test_put_diseaseprofile():
    param = {'name': str(timestamp_diseaseprofile_test), 'image_path': 'imagePutTest', 'description': 'intakePutTest'}
    response = requests.put(LOCAL_URL + PATH_VARIABLE + '/' + str(disease_posted_id), json=param, headers=HEADER)
    assert response.status_code == 200
    response = requests.get(LOCAL_URL + PATH_VARIABLE + '/' + str(disease_posted_id))
    assert response.status_code == 200
    if response:
        diseaseprofile_json = response.json()
        profile_test = diseaseprofile_json[0]
        assert_true(profile_test['disease_profile_id'] == disease_posted_id)
        assert_true(profile_test['name'] == str(timestamp_diseaseprofile_test))
        assert_true(profile_test['image_path'] == 'imagePutTest')
        assert_true(profile_test['description'] == 'intakePutTest')
        print("Put diseaseprofile by id tested successfully.")


# Test for delete function diseaseprofile endpoint
def test_delete_diseaseprofile():
    response = requests.delete(LOCAL_URL + PATH_VARIABLE + '/' + str(disease_posted_id), headers=HEADER)
    assert response.status_code == 200
    response = requests.get(LOCAL_URL + PATH_VARIABLE + '/' + str(disease_posted_id))
    assert response.status_code == 200
    if response:
        diseaseprofile_json = response.json()
        assert_false(len(diseaseprofile_json) > 0)
        print("Removed entry successfully, delete test success.")
