from ..resources.functions_shared import get_param, get_user_id_by_token
from . import db_coaches as db

# Get coaches with the following parameters:
# No parameters = all the coaches
# id = specific coach
# number and start_index is a specific amount of coaches
# or get own coachdata with id in token
def get_coach_logic(req):
    token = req.headers.get("Authorization")
    myself = get_param(req, 'self', 'string')

    if myself:
        id = get_user_id_by_token(token)
    else:
        id = get_param(req, 'id', 'int')
        number_of_coaches = get_param(req, 'number', 'int')
        start_index = get_param(req, 'start_index', 'int')
        workplace_filter = get_param(req, 'workplace', 'string')

    if id:
        data = db.get_coach(id)
        if(data[0] is None):
            return None
    elif number_of_coaches and start_index:
        data = db.get_multiple_coaches(start_index, number_of_coaches)
    elif workplace_filter:
        data = db.get_workplace_coaches(workplace_filter)
    else:
        data = db.get_all_coaches()

    return data


# Post a new coach
# Based on id in token
def post_coach_logic(req):
    token = req.headers.get("Authorization")
    workplace = get_param(req, 'workplace', 'string')
    phone = get_param(req, 'phone', 'string')
    date_of_birth = get_param(req, 'date_of_birth', 'string')

    id = get_user_id_by_token(token)

    db.create_coach(id, workplace, phone, date_of_birth)
    data = db.get_coach(id)
    return data


# This method removes a single coach (and user & details)
# Based on id in token
def delete_coach_logic(req):
    token = req.headers.get("Authorization")
    id = get_user_id_by_token(token)
    db.remove_coach(id)


# Updates a existing coach in the DB
# Valid id in the token and the workplace as param are required
def put_coach_logic(req):
    token = req.headers.get("Authorization")
    id = get_user_id_by_token(token)
    workplace = get_param(req, 'workplace', 'string')
    phone = get_param(req, 'phone', 'string')
    date_of_birth = get_param(req, 'date_of_birth', 'string')

    db.update_coach(id, workplace, phone, date_of_birth)
    data = db.get_coach(id)
    return data

