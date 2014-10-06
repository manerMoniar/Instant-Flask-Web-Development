from flask import Flask

app = Flask(__name__)


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
