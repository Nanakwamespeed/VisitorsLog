from flask import jsonify, request, render_template, url_for
from flask_mail import Mail, Message
from app import db
from app import app
from app.models import User
from app.models import Visit
from app.models import Roles
from datetime import datetime

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ajaibkwame@gmail.com'
app.config['MAIL_PASSWORD'] = 'lukagvwmfbuxpnsf'
app.config['MAIL_DEFAULT_SENDER'] = ('Ghana Link Network Services', 'noreply@ghanalink.com')

mail = Mail(app)


def create_user_controller():
    try:
        # Extract form data
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        password = data['password']
        role = data.get('role', 0)  # Default role to 0 if not provided
        created_by = data['created_by']
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        delete_yn = "N"

        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            role=role,
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
    user.role = data.get('role', user.role)
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
            'role': user.role,
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


def create_visit_controller():
    data = request.get_json()

    # Validate the data
    required_fields = ['full_name', 'phone', 'staff_name', 'purpose']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create a new Visit object
    new_visit = Visit(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        staff_name=data['staff_name'],
        purpose=data['purpose'],
        entry_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status="Pending",
        delete_yn="N"
    )

    # Add to the session and commit
    db.session.add(new_visit)
    db.session.commit()
    name_parts = data['staff_name'].split()
    first_name = name_parts[0]
    user = User.query.filter_by(first_name=first_name).first()
    staff_email = user.email if user else None

    msg = Message(f'New Visit Request from {data['full_name']}',
                  recipients=[f'{staff_email}'])

    # Render the HTML template with dynamic data
    msg.html = render_template('emailTemplate.html',
                               title=f'Visit Request from {data['full_name']}',
                               body=f"""
                                               Full Name: {data['full_name']}
                                               Email: {data['email']}
                                               Phone Number: {data['phone']}
                                               Host Name: {data['staff_name']}
                                               Visit Purpose: {data['purpose']}
                                               """,
                               link1_url=url_for('reply_form', visit_id=new_visit.id,
                                                 _external=True))

    mail.send(msg)

    return jsonify({
        'id': new_visit.id,
        'full_name': new_visit.full_name,
        'email': new_visit.email,
        'phone': new_visit.phone,
        'staff_name': new_visit.staff_name,
        'purpose': new_visit.purpose,
        'entry_time': new_visit.entry_time,
        'exit_time': new_visit.exit_time,
        'status': new_visit.status,
        'response': new_visit.response,
        'reschedule_date': new_visit.reschedule_date,
        'cancellation_reason': new_visit.cancellation_reason,
        'delete_yn': new_visit.delete_yn
    }), 201


def get_all_visits_controller():
    visits = Visit.query.all()
    visits_list = [{
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
    visit.email = data.get('email', visit.email)
    visit.phone = data.get('phone', visit.phone)
    visit.staff_name = data.get('staff_name', visit.staff_name)
    visit.purpose = data.get('purpose', visit.purpose)
    visit.entry_time = data.get('entry_time', visit.entry_time)
    visit.exit_time = data.get('exit_time', visit.exit_time)
    visit.status = data.get('status', visit.status)
    visit.response = data.get('response', visit.response)
    visit.reschedule_date = data.get('reschedule_date', visit.reschedule_date)
    visit.cancellation_reason = data.get('cancellation_reason', visit.cancellation_reason)
    visit.delete_yn = data.get('delete_yn', visit.delete_yn)

    # Commit the changes to the database
    db.session.commit()

    # Return a success response with the updated visit data
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
