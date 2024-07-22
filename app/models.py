from flask_sqlalchemy import model
from app import db


class Visit(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30))
    phone = db.Column(db.String(15), nullable=False)
    staff_name = db.Column(db.String(30), nullable=False)
    purpose = db.Column(db.String(30), nullable=False)
    entry_time = db.Column(db.String(30), nullable=False)
    exit_time = db.Column(db.String(30))
    status = db.Column(db.String(30), nullable=False)
    response = db.Column(db.String(30))
    reschedule_date = db.Column(db.String(30))
    cancellation_reason = db.Column(db.String(30))
    delete_yn = db.Column(db.String(1), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.Integer())
    created_by = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.String(30), nullable=False)
    last_updated = db.Column(db.String(30))
    updated_by = db.Column(db.String(30))
    delete_yn = db.Column(db.String(1), nullable=False)


class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(30), nullable=False)
    created_on = db.Column(db.Integer(), nullable=False)
    last_updated = db.Column(db.String(30))
    updated_by = db.Column(db.String(30))
    delete_yn = db.Column(db.String(1), nullable=False)