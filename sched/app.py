from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import Base

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
    """
    >>> appointment_detail(3)
    'Detail of appointment #3.'
    """
    return 'Detail of appointment #{}.'.format(appointment_id)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """
    >>> appointment_edit(5)
    'Form to edit appointment #5.'
    """
    return 'Form to edit appointment #{}.'.format(appointment_id)


@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    """
    >>> appointment_create()
    'Form to create a new appointment.'
    """
    return 'Form to create a new appointment.'


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    raise NotImplementedError('DELETE')


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
