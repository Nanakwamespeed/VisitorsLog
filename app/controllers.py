import uuid
import re
from flask import jsonify, request, render_template, url_for, redirect, session, flash
from functools import wraps
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from app import db
from app import app
from app.models import User
from app.models import Visit
from app.models import Roles
from datetime import datetime
import os
import base64
from werkzeug.utils import secure_filename

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ajaibkwame@gmail.com'
app.config['MAIL_PASSWORD'] = 'lukagvwmfbuxpnsf'
app.config['MAIL_DEFAULT_SENDER'] = ('Ghana Link Network Services', 'noreply@ghanalink.com')

mail = Mail(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_view'))
        return f(*args, **kwargs)

    return decorated_function


def suggest_usernames_controller():
    query = request.args.get('q')
    if query:
        # Query the database to find matching first or last names
        users = User.query.filter((User.first_name.like(f'%{query}%')) | (User.last_name.like(f'%{query}%'))).all()
        usernames = [f"{user.first_name} {user.last_name}" for user in users]
        print(usernames)  # Debugging line
        return jsonify(usernames)
    return jsonify([])


def login_controller():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        print("THIS IS THE USER: ", user)

        if user and check_password_hash(user.password, password):
            role = Roles.query.get(user.role_id)
            session['user_id'] = user.id
            session['user_role'] = role.name
            return jsonify({"message": "Login successful", "role": role.name, "status": 200}), 200
        else:
            return jsonify({"message": "Invalid credentials", "status": 401}), 401

    return render_template('login.html')


def logout_controller():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login_view'))


def get_statistics_controller():
    # Total number of visits
    total_visits = db.session.query(func.count(Visit.id)).scalar()

    # Average number of visits per day
    first_visit_date = db.session.query(func.min(Visit.entry_time)).scalar()
    last_visit_date = db.session.query(func.max(Visit.entry_time)).scalar()

    if first_visit_date and last_visit_date:
        first_date = datetime.strptime(first_visit_date, '%Y-%m-%d %H:%M:%S')
        last_date = datetime.strptime(last_visit_date, '%Y-%m-%d %H:%M:%S')
        total_days = (last_date - first_date).days + 1  # Adding 1 to include the last day
        average_visits_per_day = total_visits / total_days
    else:
        average_visits_per_day = 0

    # Number of official visits vs other visits
    official_visits = db.session.query(func.count(Visit.id)).filter(Visit.purpose == 'Official Appointment').scalar()
    other_visits = total_visits - official_visits

    # Total number of users
    total_users = db.session.query(func.count(User.id)).scalar()

    # Visits per month for the past year
    visits_per_month = db.session.query(
        func.strftime("%Y-%m", Visit.entry_time),
        func.count(Visit.id)
    ).group_by(func.strftime("%Y-%m", Visit.entry_time)).all()

    visits_data = {month: count for month, count in visits_per_month}

    # Count visits by purpose
    visit_purposes = db.session.query(
        Visit.purpose,
        func.count(Visit.id)
    ).group_by(Visit.purpose).all()

    purpose_data = {purpose: count for purpose, count in visit_purposes}

    statistics = {
        "total_visits": total_visits,
        "average_visits_per_day": average_visits_per_day,
        "official_visits": official_visits,
        "other_visits": other_visits,
        "total_users": total_users,
        "visits_data": visits_data,
        "purpose_data": purpose_data
    }

    return jsonify(statistics), 200


def create_user_controller():
    try:
        # Extract form data
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        role_id = data.get('role_id', 0)  # Default role to 0 if not provided
        created_by = data['created_by']
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        delete_yn = "N"

        print('Hashed password:', password)

        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            role_id=role_id,
            created_by=created_by,
            created_on=created_on,
            delete_yn=delete_yn
        )

        # Add the new user to the session and commit
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Employee created successfully",
            "status": 201
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})


def get_all_users_controller():
    users = User.query.all()
    user_list = [{
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'password': user.password,
        'role': user.role,
        'created_by': user.created_by,
        'updated_by': user.updated_by,
        'delete_yn': user.delete_yn
    } for user in users]

    return jsonify({
        "data": user_list,
        "message": "All users retrieved successfully",
        "status": 200
    }), 200


def update_user_controller(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.password = data.get('password', user.password)
    user.role_id = data.get('role_id', user.role_id)
    user.updated_by = data.get('updated_by', user.updated_by)
    user.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user.delete_yn = data.get('delete_yn', user.delete_yn)

    db.session.commit()

    return jsonify({
        "data": {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role_id,
            'created_by': user.created_by,
            'created_on': user.created_on,
            'last_updated': user.last_updated,
            'updated_by': user.updated_by
        },
        "message": "User updated successfully",
        "status": 200
    }), 200


def get_user_controller(user_id):
    user = User.query.get_or_404(user_id)

    return jsonify({
        "data": {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role,
            'created_by': user.created_by,
            'created_on': user.created_on,
            'last_updated': user.last_updated,
            'updated_by': user.updated_by
        },
        "message": "User retrieved successfully",
        "status": 200
    }), 200


def search_user_controller():
    query = request.args.get('query', '')
    users = User.query.filter(User.full_name.ilike(f'%{query}%')).all()
    user_names = [user.full_name for user in users]
    return jsonify(user_names)


def create_role_controller():
    try:
        # Extract form data
        data = request.get_json()
        name = data['name']
        created_by = data['created_by']
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        delete_yn = "N"

        # Create a new user instance
        new_role = Roles(
            name=name,
            created_by=created_by,
            created_on=created_on,
            delete_yn=delete_yn
        )

        # Add the new user to the session and commit
        db.session.add(new_role)
        db.session.commit()

        return jsonify({
            "message": "Role created successfully",
            "status": 201
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})


def get_all_roles_controller():
    roles = Roles.query.all()
    roles_list = [{
        'id': role.id,
        'name': role.name,
        'created_by': role.created_by,
        'created_on': role.created_on,
        'last_updated': role.last_updated,
        'updated_by': role.updated_by,
        'delete_yn': role.delete_yn
    } for role in roles]

    return jsonify({
        "data": roles_list,
        "message": "All roles retrieved successfully",
        "status": 200
    }), 200


def update_role_controller(role_id):
    role = Roles.query.get_or_404(role_id)
    data = request.json

    role.name = data.get('name', role.name)
    role.updated_by = data.get('updated_by', role.updated_by)
    role.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db.session.commit()

    return jsonify({
        "data": {
            'id': role.id,
            'name': role.name,
            'created_by': role.created_by,
            'created_on': role.created_on,
            'last_updated': role.last_updated,
            'updated_by': role.updated_by
        },
        "message": "Role updated successfully",
        "status": 200
    }), 200


def get_role_controller(role_id):
    role = Roles.query.get_or_404(role_id)

    return jsonify({
        "data": {
            'id': role.id,
            'name': role.name,
            'created_by': role.created_by,
            'created_on': role.created_on,
            'last_updated': role.last_updated,
            'updated_by': role.updated_by,
            'delete_yn': role.delete_yn
        },
        "message": "Role retrieved successfully",
        "status": 200
    }), 200


def upload_image():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    # Decode the base64 image data
    try:
        header, encoded = image_data.split(',', 1)
        file_data = base64.b64decode(encoded)
        file_extension = header.split(';')[0].split('/')[1]

        # Generate a unique filename and save the image
        filename = secure_filename(f'{uuid.uuid4()}.{file_extension}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(file_data)

        # Return the image path
        return jsonify({'imagePath': f'/static/uploads/{filename}'})

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error processing image data'}), 500


def create_visit_controller():
    data = request.get_json()

    # Validate the data
    required_fields = ['full_name', 'contact_method', 'contact', 'staff_name', 'reason']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate contact based on the contact method
    if data['contact_method'] == 'email':
        if not validate_email(data['contact']):
            return jsonify({'error': 'Invalid email address'}), 400
    elif data['contact_method'] == 'phone':
        if not validate_phone_number(data['contact']):
            return jsonify({'error': 'Invalid phone number'}), 400

    # Create a new Visit object
    new_visit = Visit(
        full_name=data['full_name'],
        contact_method=data['contact_method'],
        contact=data['contact'],
        staff_name=data['staff_name'],
        purpose=data['reason'],
        multiple_visitors=data.get('multiple', False),
        number_of_visitors=data.get('counter_value', 1),
        entry_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status="Pending",
        delete_yn="N",
        image=data.get('image', '')
    )

    # Add to the session and commit
    db.session.add(new_visit)
    db.session.commit()

    # Find the staff email based on staff_name
    name_parts = data['staff_name'].split()
    first_name = name_parts[0]
    user = User.query.filter_by(first_name=first_name).first()
    staff_email = user.email if user else None

    # Prepare and send the email
    msg = Message(
        subject=f'New Visit Request from {data["full_name"]}',
        recipients=[staff_email] if staff_email else []
    )
    msg.html = render_template(
        'emailTemplate.html',
        title=f'Visit Request from {data["full_name"]}',
        body=f"""
            <p>A guest by the name {data['full_name']} is here to see you. This is their {data['contact_method']}: 
            {data['contact']}. This is the reason they're here to see you: {data['reason']}</p>
            <p><strong>Multiple Individuals:</strong> {'Yes' if data.get('multiple') else 'No'}</p>
            <p><strong>Number Of Individuals:</strong> {data.get('counter_value', 1)}</p>
        """,
        accept_url=url_for('accept_visit', visit_id=new_visit.id, _external=True),
        decline_url=url_for('decline_visit', visit_id=new_visit.id, _external=True)
    )
    mail.send(msg)

    return jsonify({
        'id': new_visit.id,
        'full_name': new_visit.full_name,
        'contact_method': new_visit.contact_method,
        'contact': new_visit.contact,
        'staff_name': new_visit.staff_name,
        'purpose': new_visit.purpose,
        'multiple_visitors': new_visit.multiple_visitors,
        'number_of_visitors': new_visit.number_of_visitors,
        'entry_time': new_visit.entry_time,
        'status': new_visit.status,
        'response': new_visit.response,
        'reschedule_date': new_visit.reschedule_date,
        'cancellation_reason': new_visit.cancellation_reason,
        'delete_yn': new_visit.delete_yn,
        'image': new_visit.image
    }), 201


def get_all_visits_controller():
    visits = Visit.query.all()
    visits_list = [{
        'id': visit.id,
        'full_name': visit.full_name,
        'contact_method': visit.contact_method,
        'contact': visit.contact,
        'staff_name': visit.staff_name,
        'purpose': visit.purpose,
        'entry_time': visit.entry_time,
        'exit_time': visit.exit_time,
        'status': visit.status,
        'response': visit.response,
        'reschedule_date': visit.reschedule_date,
        'cancellation_reason': visit.cancellation_reason,
        'delete_yn': visit.delete_yn
    } for visit in visits]

    return jsonify({
        "data": visits_list,
        "message": "All visits retrieved successfully",
        "status": 200
    }), 200


def update_visit_controller(visit_id):
    data = request.get_json()

    # Retrieve the visit by ID
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404

    # Update the visit's attributes with data from the request
    visit.full_name = data.get('full_name', visit.full_name)
    visit.contact_method = data.get('contact_method', visit.contact_method)
    visit.contact = data.get('contact', visit.contact)
    visit.staff_name = data.get('staff_name', visit.staff_name)
    visit.purpose = data.get('purpose', visit.purpose)
    visit.multiple_visitors = data.get('multiple_visitors', visit.multiple_visitors)
    visit.number_of_visitors = data.get('number_of_visitors', visit.number_of_visitors)
    visit.entry_time = data.get('entry_time', visit.entry_time)
    visit.exit_time = data.get('exit_time', visit.exit_time)
    visit.status = data.get('status', visit.status)
    visit.response = data.get('response', visit.response)
    visit.reschedule_date = data.get('reschedule_date', visit.reschedule_date)
    visit.cancellation_reason = data.get('cancellation_reason', visit.cancellation_reason)
    visit.delete_yn = data.get('delete_yn', visit.delete_yn)
    visit.image = data.get('image', visit.image)

    # Commit the changes to the database
    db.session.commit()

    # Return a success response with the updated visit data
    return jsonify({
        "data": {
            'id': visit.id,
            'full_name': visit.full_name,
            'contact_method': visit.contact_method,
            'contact': visit.contact,
            'staff_name': visit.staff_name,
            'purpose': visit.purpose,
            'multiple_visitors': visit.multiple_visitors,
            'number_of_visitors': visit.number_of_visitors,
            'entry_time': visit.entry_time,
            'exit_time': visit.exit_time,
            'status': visit.status,
            'response': visit.response,
            'reschedule_date': visit.reschedule_date,
            'cancellation_reason': visit.cancellation_reason,
            'delete_yn': visit.delete_yn,
            'image': visit.image
        },
        "message": "Visit updated successfully",
        "status": 200
    }), 200


def get_visit_controller(visit_id):
    visit = Visit.query.get_or_404(visit_id)

    return jsonify({
        "data": {
            'id': visit.id,
            'full_name': visit.full_name,
            'email': visit.email,
            'phone': visit.phone,
            'staff_name': visit.staff_name,
            'purpose': visit.purpose,
            'entry_time': visit.entry_time,
            'exit_time': visit.exit_time,
            'status': visit.status,
            'response': visit.response,
            'reschedule_date': visit.reschedule_date,
            'cancellation_reason': visit.cancellation_reason,
            'delete_yn': visit.delete_yn
        },
        "message": "Role retrieved successfully",
        "status": 200
    }), 200


def accept_visit_controller(visit_id):
    # Retrieve the visit by ID
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404

    # Update the visit's response and status
    visit.response = 'Accepted'
    visit.status = 'Accepted'

    # Commit the changes to the database
    db.session.commit()

    # Return a success response
    return redirect('/thank-you')


def decline_visit_controller(visit_id):
    # Retrieve the visit by ID
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404

    # Update the visit's response and status
    visit.response = 'Declined'
    visit.status = 'Declined'

    # Commit the changes to the database
    db.session.commit()

    # Return a success response
    return redirect('/thank-you')


# Validation functions
def validate_email(email):
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def validate_phone_number(phone):
    # Basic validation for a phone number, adjust regex as needed
    regex = r'^\+?[\d\s]{10,15}$'
    return re.match(regex, phone) is not None
