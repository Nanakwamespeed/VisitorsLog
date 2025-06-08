from flask_sqlalchemy import model
from app import db


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)  # Increased length to accommodate longer names
    contact_method = db.Column(db.String(10), nullable=False, default='email')  # 'email' or 'phone'
    contact = db.Column(db.String(50), nullable=False)  # Increased length to accommodate longer email or phone numbers
    staff_name = db.Column(db.String(50), nullable=False)  # Increased length for more descriptive staff names
    purpose = db.Column(db.String(100), nullable=False)  # Increased length for more detailed purposes
    multiple_visitors = db.Column(db.Boolean, default=False)  # To indicate if multiple individuals
    number_of_visitors = db.Column(db.Integer, default=1)  # To store the number of individuals if 'multiple' is True
    entry_time = db.Column(db.String(30), nullable=False)
    exit_time = db.Column(db.String(30))
    status = db.Column(db.String(30), nullable=False)
    response = db.Column(db.String(30))
    reschedule_date = db.Column(db.String(30))
    cancellation_reason = db.Column(db.String(30))
    delete_yn = db.Column(db.String(1), nullable=False)
    image = db.Column(db.String(120))  # URL or file path for the image


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', name='fk_user_role'))
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