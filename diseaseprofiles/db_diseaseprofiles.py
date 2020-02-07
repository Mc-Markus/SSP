from sqlalchemy.orm import sessionmaker
from ..resources.db_connection import request_session
from ..resources.models import DiseaseProfile


# Get all the disease profiles in the db with sqlalchemy
def get_all_diseaseprofiles():
    session = request_session()
    query = session.query(DiseaseProfile)
    result = query.all()
    session.close()
    return result


# post disease profile to db
def post_diseaseprofile(name, image_path, description):
    try:
        session = request_session()
        disease = DiseaseProfile(name=name, image_path=image_path, description=description)
        session.add(disease)
        session.commit()
        session.close()
        return True
    except:
        return None
