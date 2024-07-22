from app import app
from app.models import Visit
from flask import render_template
from app.controllers import (create_user_controller, create_role_controller, get_all_roles_controller,
                             update_role_controller, get_role_controller, get_all_users_controller,
                             get_user_controller, update_user_controller, create_visit_controller,
                             get_all_visits_controller, get_visit_controller, update_visit_controller,
                             search_user_controller)


@app.route('/')
def index():
    return render_template('visitLogForm.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/visit-logs')
def visit_logs():
    visits_data = Visit.query.all()  # Fetch all visits from the database
    return render_template('visitLogs.html', visits=visits_data)


@app.route('/reply-form/<visit_id>')
def reply_form(visit_id):
    return render_template('replyForm.html')


@app.route('/dashboard')
def dashboard():
    visits_data = Visit.query.all()  # Fetch all visits from the database
    return render_template('dashboard.html', visits=visits_data)


app.add_url_rule('/search-user', 'search_user', search_user_controller, methods=['GET'])

app.add_url_rule('/create-user', 'create_user', create_user_controller, methods=['POST'])

app.add_url_rule('/get-users', 'get_users', get_all_users_controller, methods=['GET'])

app.add_url_rule('/get-user/<user_id>', 'get_user', get_user_controller, methods=['GET'])

app.add_url_rule('/update-user/<user_id>', 'user_role', update_user_controller, methods=['PUT'])

app.add_url_rule('/create-role', 'create_role', create_role_controller, methods=['POST'])

app.add_url_rule('/get-roles', 'get_roles', get_all_roles_controller, methods=['GET'])

app.add_url_rule('/get-role/<role_id>', 'get_role', get_role_controller, methods=['GET'])

app.add_url_rule('/update-role/<role_id>', 'update_role', update_role_controller, methods=['PUT'])

app.add_url_rule('/create-visit', 'create_visit', create_visit_controller, methods=['POST'])

app.add_url_rule('/get-visits', 'get_visits', get_all_visits_controller, methods=['GET'])

app.add_url_rule('/get-visit/<visit_id>', 'get_visit', get_visit_controller, methods=['GET'])

app.add_url_rule('/update-visit/<visit_id>', 'update_visit', update_visit_controller, methods=['PUT'])
