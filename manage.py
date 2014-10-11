from flask.ext.script import Manager
from sched.app import app

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.

@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()

@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()
    
if __name__ == '__main__':  # pragma: no cover
    manager.run()
