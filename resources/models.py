from sqlalchemy import Column, Integer, String, ForeignKey, Table, inspect, DateTime, Enum
from .db_connection import Base, db_connect
import enum


class Coach(Base):
    __table__ = Table('Coach', Base.metadata,
                      Column('id', Integer, ForeignKey('auth_user.id'), primary_key=True),
                      Column('workplace', String(50)),
                      )


class User(Base):
    __table__ = Table('auth_user', Base.metadata,
                      autoload=True, autoload_with=db_connect())


class Token(Base):
    __table__ = Table('oauth2_provider_accesstoken', Base.metadata,
                      autoload=True, autoload_with=db_connect())


class Medicine(Base):
    __table__ = Table('medicines', Base.metadata,
                      Column('medicine_id', Integer, primary_key=True, autoincrement=True),
                      Column('name', String(255), nullable=False),
                      Column('image_path', String(255), nullable=False),
                      Column('description', String(255), nullable=False)
                      )


class DiseaseProfile(Base):
    __table__ = Table('disease_profiles', Base.metadata,
                      Column('disease_profile_id', Integer, primary_key=True, autoincrement=True),
                      Column('name', String(255), nullable=False),
                      Column('image_path', String(255), nullable=False),
                      Column('description', String(255), nullable=False)
                      )


class Patient(Base):
    __table__ = Table(
        'patients', Base.metadata,
        Column('patient_user_id', Integer, ForeignKey('auth_user.id'), primary_key=True),
        Column('coach_user_id', Integer, ForeignKey('Coach.id')),
        Column('electronic_dossier_id', Integer, ForeignKey('electronic_dossiers.electronic_dossier_id'))
    )


# Enum class for intake_state in database, the assigned values are not actually used in the db, only the variable names
class IntakeStateEnum(enum.Enum):
    not_taken = 'not_taken'
    taken = 'taken'
    too_late = 'too_late'


class MedicinePerPatient(Base):
    __table__ = Table(
        'medicine_per_patient', Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('patient_user_id', Integer, ForeignKey('patients.patient_user_id')),
        Column('medicine_id', Integer, ForeignKey('medicines.medicine_id')),
        Column('intake_time', DateTime, nullable=False),
        Column('intake_state', Enum(IntakeStateEnum), nullable=False),
        Column('dose', String(50), nullable=False)
    )


class ElectronicDossier(Base):
    __table__ = Table(
        'electronic_dossiers', Base.metadata,
        Column('electronic_dossier_id', Integer, primary_key=True, autoincrement=True),
        Column('summary', String(250), nullable=False),
        Column('iq', Integer, nullable=False)
    )
