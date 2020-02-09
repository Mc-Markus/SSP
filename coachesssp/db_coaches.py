import sqlalchemy
import psycopg2
from sqlalchemy import Column, Integer, String, ForeignKey, inspect, MetaData
from sqlalchemy.orm import defer
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from ..resources.db_connection import request_session
from ..resources.models import coach as Coach, User

# Get all the coaches in the db with sqlalchemy
# Link with userdata and defer password
def get_all_coaches():
    session = request_session()
    query = session.query(Coach, User)
    query = query.filter(Coach.id == User.id)
    query = query.options(defer(User.password))

    result = query.all()
    session.close()
    return result


# Get a single coach with id in the db with sqlalchemy
# Link with userdata and defer password
def get_coach(id):
    session = request_session()
    query = session.query(Coach, User)
    query = query.filter(Coach.id == id)
    query = query.filter(Coach.id == User.id)
    query = query.options(defer(User.password))

    result = query.all()
    session.close()
    return result


# Get multiple coaches based on the number provided in the db with sqlalchemy
# Link with userdata and defer password
def get_multiple_coaches(start_index, number):
    session = request_session()
    query = session.query(Coach, User)
    query = query.filter(Coach.id == User.id)
    query = query.limit(number)
    query = query.offset(start_index - 1)
    query = query.options(defer(User.password))

    result = query.all()
    session.close()
    return result

def get_workplace_coaches(workplace_filter):
    session = request_session()
    query = session.query(Coach, User)
    query = query.filter(Coach.id == User.id)
    query = query.filter(Coach.workplace == workplace_filter)
    query = query.options(defer(User.password))

    result = query.all()
    session.close()
    return result

# Update coach into database table
def update_coach(id, new_workplace, new_phone, new_dob):
    session = request_session()
    query = session.query(Coach)
    query = query.filter(Coach.id == id)
    query = query.first()
    query.workplace = new_workplace
    query.date_of_birth = new_dob
    query.phone = new_phone
    session.commit()
    session.close()


# Remove coach from db
def remove_coach(id):
    session = request_session()
    query = session.query(Coach)
    query = query.get(id)
    session.delete(query)
    session.commit()
    session.close()

# Create coach in db
def create_coach(user_id, workplace, phone, date_of_birth):
    session = request_session()
    coach = Coach(id=user_id, workplace=workplace, phone=phone, date_of_birth=date_of_birth)
    session.add(coach)
    session.commit()
    session.close()