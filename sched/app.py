from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from sched.forms import AppointmentForm
from sched.models import Base, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'

# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base


@app.route('/')
def hello():
    """
    >>> hello()
    'Hello, world!'
    """
    return 'Hello, world!'


@app.route('/appointments/')
def appointment_list():
    """
    >>> appointment_list()
    'Listing of all appointments we have.'
    """
    return 'Listing of all appointments we have.'


@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    """Provide HTML page with a given appointment."""
    # Query: get Appointment object by ID.
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """
    >>> appointment_edit(5)
    'Form to edit appointment #5.'
    """
    return 'Form to edit appointment #{}.'.format(appointment_id)


@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    """Provide HTML form to create a new appointment."""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list.
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point.
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    raise NotImplementedError('DELETE')


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
