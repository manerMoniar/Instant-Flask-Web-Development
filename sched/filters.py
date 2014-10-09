def do_datetime(dt, format=None):
	"""Jinja template filter to format a datetime object."""
	if dt is None:
		# By default, render an empty string.
		return ''
	if format is None:
		# No format is given in the template call.
		# Use a default format.