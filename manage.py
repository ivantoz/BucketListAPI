import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from BucketListAPI.app import app
from BucketListAPI.model import db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
