from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config


app = Flask(__name__, static_folder='../html', static_url_path='/static')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import api_views, error_handlers, views
from yacut.models import URLMap


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'URLMap': URLMap}
