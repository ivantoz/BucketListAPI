import os
import unittest
import coverage

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from BucketListAPI.app import app
from BucketListAPI.model import db

app.config.from_object(os.environ['APP_SETTINGS'])


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
COV = coverage.coverage(
    branch=True,
    include='BucketListAPI/*',
    omit=[
        'BucketListAPI/tests/*',
    ]
)
COV.start()


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('BucketListAPI/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('BucketListAPI/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
