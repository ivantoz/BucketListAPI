BucketList Application API
==========================

This project showcases my vision on how the RESTful API server should be
implemented.

The goals that were achived in this example:

* RESTful API server should be self-documented using OpenAPI (fka Swagger)
  specifications, so interactive documentation UI is in place;
* Authentication is handled with basic auth and using JWT tokens makes it usable
  not only for third-party "external" apps;
* Permissions are handled (and automaticaly documented);

Project Structure
-----------------

### Root folder

Folders:

* `BucketListAPI` - This Bucketlist API implementation is here.
* `migrations` - Database migrations are stored here 
* `BucketListAPI/api/auth/` -  authorization endpoints serializers, parsers and business logic is 
implemented here
* `BucketListAPI/api/bucketlist/` -  bucketlist endpoints, serializers, parsers and business logic
 is implemented here
* `BucketListAPI/tests` - These are [pytest](http://pytest.org) tests for this BucketList 
Application API implementation.


Files:

* `README.md`
* `BucketListAPI/config.py` - This is a config file of this BucketList API.
* `.coveragerc` - [Coverage.py](http://coverage.readthedocs.org/) (code
  coverage) config for code coverage reports.
* `.travis.yml` - [Travis CI](https://travis-ci.org/) (automated continuous
  integration) config for automated testing.
* `.pylintrc` - [Pylint](https://www.pylint.org/) config for code quality
  checking.
* `manage.py` - Commands for database migrations and running tests implemented here
* `.gitignore` - Lists files and file masks of the files which should not be
  added to git repository.
* `.logging.conf` - Logging configuration file
* `Procfile` - is a mechanism for declaring what commands are run by your application's 
dynos on the Heroku platform
* `runtime.txt` - specifies the python version to run on heroku



