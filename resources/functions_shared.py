from sqlalchemy.ext.declarative import DeclarativeMeta
import json


# gets parameter from either the path or body in the request
def get_param(req, param, par_type):
    par = req.params.get(param)
    if not par:
        try:
            req_body = req.get_json()
        except ValueError:
            return None
        else:
            par = req_body.get(param)

    if(par_type == "int"):
        par = int(par)
    if(par_type == "string"):
        par = str(par)
    else:
        pass

    return par


# sqlalchemy response to list with dicts, and remove unwanted data
def prepare_data(db_data, var_list):
    return_list = []
    for rindex, item in enumerate(db_data):
        for iindex, var in enumerate(var_list):
            var_attr = getattr(item, var[0])
            obj_dict = var_attr.__dict__
            del obj_dict["_sa_instance_state"]
            try:
                return_list[rindex].append(obj_dict)
            except IndexError:
                return_list.append([obj_dict])
    return return_list


def get_user_id_by_token(token):
    from .models import Token
    from .db_connection import request_session

    session = request_session()
    if "earer" in token:
        data = session.query(Token).filter(Token.token == token[7:]).first()
    else:
        data = session.query(Token).filter(Token.token == token).first()
    session.close()
    
    return data.__dict__['user_id']


# function for encoding sql alchemy data to json
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields