@app.route(
'/appointments/<int:appointment_id>/',
endpoint='some_name')
def appointment_detail(appointment_id):
# Use url_for('some_name', appointment_id=x)
# to build a URL for this.
return 'Just to demonstrate...'