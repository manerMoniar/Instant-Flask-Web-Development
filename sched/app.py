import logging

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from sched import config, filters
from sched.forms import AppointmentForm, LoginForm
from sched.models import Appointment, Base, User


app = Flask(__name__)
app.config.from_object(config)

# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base


login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to see your appointments.'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID."""
    return db.session.query(User).get(user_id)


filters.init_app(app)


# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler())  # Log to stderr.
    app.logger.setLevel(logging.INFO)


@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404


@app.route('/appointments/')
@login_required
def appointment_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Appointment)
             .filter_by(user_id=current_user.id)
             .order_by(Appointment.start.asc()).all())
    return render_template('appointment/index.html', appts=appts)


@app.route('/appointments/<int:appointment_id>/')
@login_required
def appointment_detail(appointment_id):
    """Provide HTML page with all details on a given appointment."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None or appt.user_id != current_user.id:
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/create/', methods=['GET', 'POST'])
@login_required
def appointment_create():
    """Provide HTML form to create a new appointment record."""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('appointment_list'))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
@login_required
def appointment_edit(appointment_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
@login_required
def appointment_delete(appointment_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = '404'
        return response
    if appt.user_id != current_user.id:
        response = jsonify({'status': 'Forbidden'})
        response.status_code = '403'
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('appointment_list'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = \
            User.authenticate(db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('appointment_list'))
        else:
            error = 'Incorrect username or password. Try again.'
    return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))
