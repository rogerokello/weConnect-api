import unittest
# class for handling a set of commands
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



from app import db, create_app

# initialize the app with all its configurations
app = create_app('testing')

# create an instance of class that will handle our commands
manager = Manager(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# define our command for testing called "test"
# Usage: python manage.py test
@manager.command
def testv1():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests/api/v1', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()