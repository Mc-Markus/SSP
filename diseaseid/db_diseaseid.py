from sqlalchemy.orm import sessionmaker
from ..resources.db_connection import request_session
from ..resources.models import DiseaseProfile


# get disease profile by id
def get_diseaseprofiles_by_id(id):
    session = request_session()

    query = session.query(DiseaseProfile)
    query = query.filter(DiseaseProfile.disease_profile_id == id)

    result = query.all()
    session.close()
    return result


# update disease profile in db
def put_diseaseprofile(id, name, image_path, description):
    try:
        session = request_session()

        query = session.query(DiseaseProfile)
        disease = query.filter(DiseaseProfile.disease_profile_id == id).first()
        disease.name = name
        disease.image_path = image_path
        disease.description = description
        session.commit()
        session.close()
        return True
    except:
        return None


# delete disease profile from db
def delete_diseaseprofile(id):
    try:
        session = request_session()
        query = session.query(DiseaseProfile)
        query = query.filter(DiseaseProfile.disease_profile_id == id)
        query.delete()
        session.commit()
        session.close()
        return True
    except:
        return None