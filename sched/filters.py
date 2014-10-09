def do_datetime(dt, format=None):
	"""Jinja template filter to format a datetime object."""
	if dt is None:
		# By default, render an empty string.
		return ''
	if format is None:
		# No format is given in the template call.
		# Use a default format.
		# No format is given in the template call.
		# Use a default format.
		#
		# Format time in its own strftime call in order to:	
		# 1. Left-strip leading 0 in hour display.
		# 2. Use 'am'/'pm' (lower case) instead of 'AM'/'PM'.
		formatted_date = dt.strftime('%Y-%m-%d - %A')
		formatted_time =\
			dt.strftime('%I:%M%p').lstrip('0').lower()
		formatted = '%s at %s' %\
		(formatted_date, formatted_time)
	else:
		formatted = dt.strftime(format)
	return formatted

def init_app(app):
	"""Initialize a Flask application with custom filters."""
	app.jinja_env.filters['datetime'] = do_datetime