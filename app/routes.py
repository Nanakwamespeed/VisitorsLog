from app import app
from app.models import Visit
from app.models import User
from flask import render_template
from app.controllers import (create_user_controller, create_role_controller, get_all_roles_controller,
                             update_role_controller, get_role_controller, get_all_users_controller,
                             get_user_controller, update_user_controller, create_visit_controller,
                             get_all_visits_controller, get_visit_controller, update_visit_controller,
                             search_user_controller, login_controller, suggest_usernames_controller, logout_controller,
                             get_statistics_controller, login_required, upload_image, accept_visit_controller,
                             decline_visit_controller)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/reports')
@login_required
def reports():
    visits_data = Visit.query.all()  # Fetch all visits from the database
    return render_template('reports.html', visits=visits_data)


@app.route('/login-view')
def login_view():
    return render_template('login.html')


@app.route('/thank-you')
def thank_you_view():
    return render_template('thankyou.html')


@app.route('/new-user')
@login_required
def new_user():
    return render_template('newUser.html')


app.add_url_rule('/suggest-usernames', 'suggest_usernames', suggest_usernames_controller, methods=['GET'])


app.add_url_rule('/login', 'login', login_controller, methods=['POST'])


app.add_url_rule('/logout', 'logout', logout_controller, methods=['GET'])


@app.route('/visit-logs')
@login_required
def visit_logs():
    visits_data = Visit.query.all()  # Fetch all visits from the database
    return render_template('visitLogs.html', visits=visits_data)


@app.route('/edit-user/<user_id>')
@login_required
def edit_user(user_id):
    user_data = User.query.get(user_id)  # Fetch all visits from the database
    return render_template('editUser.html', user=user_data)


@app.route('/user-list')
@login_required
def user_list():
    users_data = User.query.all()  # Fetch all visits from the database
    return render_template('userList.html', users=users_data)


@app.route('/reply-form/<visit_id>')
def reply_form(visit_id):
    return render_template('replyForm.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    visits_data = Visit.query.all()  # Fetch all visits from the database
    return render_template('dashboard.html', visits=visits_data)


app.add_url_rule('/accept-visit/<visit_id>', 'accept_visit', accept_visit_controller, methods=['GET'])

app.add_url_rule('/decline-visit/<visit_id>', 'decline_visit', decline_visit_controller, methods=['GET'])

app.add_url_rule('/upload-image', 'upload_image', upload_image, methods=['POST'])

app.add_url_rule('/get-stats', 'get_stats', get_statistics_controller, methods=['GET'])

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
