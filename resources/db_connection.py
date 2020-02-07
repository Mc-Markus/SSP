import sqlalchemy
import psycopg2
from sqlalchemy import Column, Integer, String, ForeignKey, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import requests
import json
import azure.functions as func
import os

Base = declarative_base()

# connect to database
def db_connect():
    engine = sqlalchemy.engine.create_engine(
        'postgresql+psycopg2://Test-DB-account:Ikhoopdatiknooitmeerazureterugzie1!@160.153.246.141:5432/mmoauthprovider')
    return engine


# returns a session with the db_connect
def request_session():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    return Session()


# script to create the db
def init_db():
    from .models import Coach, User, Token, Medicine, DiseaseProfile, Patient, MedicinePerPatient, ElectronicDossier

    engine = db_connect()
    Base.metadata.reflect(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("DATABASE CREATED SUCCESFULLY")

# test a table
def tb_test():
    engine = db_connect()
    inspector = inspect(engine)
    # Get table information
    print(inspector.get_table_names())