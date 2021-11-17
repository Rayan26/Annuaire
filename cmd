set FLASK_APP=project
set FLASK_DEBUG=1

set FLASK_APP=project
set FLASK_APP=feed_service
set FLASK_APP=auth_service
set FLASK_APP=front_service
set FLASK_DEBUG=1


from project import db, create_app
from auth_service import db, create_app
from feed_service import db, create_app
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
