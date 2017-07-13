from flask import (Flask, url_for, send_from_directory, render_template, abort, 
    jsonify, redirect, request, session, flash)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, current_user, login_user, logout_user, 
    login_required)
from sched.forms import AppointmentForm, LoginForm
from sched.models import Base, User, Appointment
from sched import filters

app = Flask(__name__, static_folder=None, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'

# use Flask-SQLAlchemy for its engine and session configuration. Load the 
# extension, giving it the app object, and override its default Model class 
# with the pure SQLAchemy declarative Base class.
db = SQLAlchemy(app)
filters.init_app(app)
# db.Model = Base
db.Model = Appointment


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# @app.route('/')
# def hello():
#     return 'Hello, World!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments/')
# @login_required
def appointment_list():
    '''Provide HTML listing of all appointments'''
    # Query: Get all Appointment objects, sorted by date
    appts = (db.session.query(Appointment)
        .order_by(Appointment.start.asc()).all())
    return render_template('appointment/index.html', appts=appts)

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    '''Provide HTML page with a given appointment'''
    # Query: get Appointment object by ID
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found
        abort(404)
    return render_template('appointment/detail.html', appt=appt)

@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    '''Provide HTML form to edit a given appointment'''
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    # Either first load or validation error at this point
    return render_template('appointment/edit.html', form=form)

@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    '''Provide HTML form to create a new appointment.'''
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point
    return render_template('appointment/edit.html', form=form)

@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    '''Delete record using HTTP DELETE, respond with JSON'''
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found, but with simple JSON response
        response = jsonify({'status': 'Not Found'})
        response.status = 404
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})

# @app.route('/appointments/<int:appointment_id>/')
# def appointment_detail(appointment_id):
#     edit_url = url_for('appointment_edit', appointment_id=appointment_id)
#     return edit_url # return the URL string for demonstration

# @app.route('/appointments/<int:appointment_id>/', endpoint='some_name')
# def appointment_detail(appointment_id):
#     # Use url_for('some_name', appointment_id=x) to build a URL for this
#     return 'Just to demonstrate...'

@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = User.authenticate(db.session.query, email, password)
        if authenticated:
            return redirect(url_for('appointment_list'))
        else:
            error = 'Incorrect username or password'
            return render_template('user/login.html', form=form, error=error)
    return render_template('user/login.html', form=form, error=error)

@app.route('/logout/')
def logout():
    return redirect(url_for('login'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run(debug=True)
