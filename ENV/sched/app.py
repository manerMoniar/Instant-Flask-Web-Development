from flask import Flask
from flask import url_for

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'

@app.route('/appointments/')
def appointment_list():
	return 'Listing of all appointments we have. Felipe Feliz'
"""
@app.route('/', subdomain='<spam_eggs>')
def subdomain_example(spam_eggs):
	return '...'

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
	return 'Detail of appointment'
	#{}.'.format(appointment_id)

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
	edit_url = url_for('appointment_edit',
		appointment_id=appointment_id)
	# Return the URL string just for demonstration.
	return edit_url
"""
@app.route(
	'/appointments/<int:appointment_id>/',
	endpoint='some_name')
def appointment_detail(appointment_id):
	# Use url_for('some_name', appointment_id=x)
	# to build a URL for this.
	return 'Just to demonstrate...'

@app.route(
	'/appointments/<int:appointment_id>/edit/',
	methods=['GET', 'POST'])

def appointment_edit(appointment_id):
	return 'Form to edit appointment #.'.format(appointment_id)

@app.route(
	'/appointments/create/',
	methods=['GET', 'POST'])
def appointment_create():
	return 'Form to create a new appointment.'

@app.route(
	'/appointments/<int:appointment_id>/delete/',
	methods=['DELETE'])
def appointment_delete(appointment_id):
		raise NotImplementedError('DELETE')

if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
