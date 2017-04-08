import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from BucketListAPI.app import app
from BucketListAPI.model import db

app.config.from_object(os.environ['APP_SETTINGS'])


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

with app.app_context():
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
