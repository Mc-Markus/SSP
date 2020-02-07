from nose.tools import assert_true, assert_false
from constants import HEADER, BASE_URL

# Third-party imports...
import requests
import time

timeStampMedicines = time.time()
medicine_posted_id = 0
PATH_VARIABLE = 'medicines'
URL_LOCAL = BASE_URL


# Test post function of medicine
def test_post_medicine():
    param = {'name': str(timeStampMedicines), 'image_path': 'functestimg', 'intakeInstructions': 'functestintake'}
    response = requests.post(URL_LOCAL + PATH_VARIABLE, json=param, headers=HEADER)
    assert response.status_code == 200
    print("Posting medicine succes")
    response = requests.get(URL_LOCAL + PATH_VARIABLE)
    assert response.status_code == 200
    if response:
        medicines_json = response.json()
        posted_med = max(medicines_json, key=lambda ev: ev['medicine_id'])
        assert_true(posted_med['medicine_id'] >= 1)
        assert_true(posted_med['name'] == str(timeStampMedicines))
        assert_true(posted_med['image_path'] == 'functestimg')
        assert_true(posted_med['description'] == 'functestintake')
        global medicine_posted_id
        medicine_posted_id = posted_med['medicine_id']
        print("Found inserted medicine, post test success")


# Func test for validating medicines get
def test_get_medicines():
    response = requests.get(URL_LOCAL + PATH_VARIABLE)
    assert response.status_code == 200
    if response:
        medicines_json = response.json()
        for medicines_inner in medicines_json:
            assert_true(medicines_inner['medicine_id'] >= 1)
    print("Get medicines test success.")


# Test for get by id function medicine endpoint
def test_get_medicine_by_id():
    assert_true(medicine_posted_id > 0,
                "Posted id should be more than 0, the post method has failed to insert the right id.")
    response = requests.get(URL_LOCAL + PATH_VARIABLE + '/' + str(medicine_posted_id))
    assert response.status_code == 200
    if response:
        medicines_json = response.json()
        assert_true(len(medicines_json) > 0)
        med_test = medicines_json[0]
        assert_true(med_test['medicine_id'] == medicine_posted_id)
        assert_true(med_test['name'] == str(timeStampMedicines))
        assert_true(med_test['image_path'] == 'functestimg')
        assert_true(med_test['description'] == 'functestintake')
        print("Get medicine by id tested successfully.")


# Test for put function medicine endpoint
def test_put_medicine():
    param = {'name': str(timeStampMedicines), 'image_path': 'imagePutTest', 'intakeInstructions': 'intakePutTest'}
    response = requests.put(URL_LOCAL + PATH_VARIABLE + '/' + str(medicine_posted_id), json=param, headers=HEADER)
    assert response.status_code == 200
    response = requests.get(URL_LOCAL + PATH_VARIABLE + '/' + str(medicine_posted_id))
    assert response.status_code == 200
    if response:
        medicines_json = response.json()
        med_test = medicines_json[0]
        assert_true(med_test['medicine_id'] == medicine_posted_id)
        assert_true(med_test['name'] == str(timeStampMedicines))
        assert_true(med_test['image_path'] == 'imagePutTest')
        assert_true(med_test['description'] == 'intakePutTest')
        print("Put medicine by id tested successfully.")


# Test for delete function medicine endpoint
def test_delete_medicine():
    response = requests.delete(URL_LOCAL + PATH_VARIABLE + '/' + str(medicine_posted_id), headers=HEADER)
    assert response.status_code == 200
    response = requests.get(URL_LOCAL + PATH_VARIABLE + '/' + str(medicine_posted_id))
    assert response.status_code == 200
    if response:
        medicines_json = response.json()
        assert_false(len(medicines_json) > 0)
        print("Removed entry successfully, delete test success.")
