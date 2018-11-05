import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.getcwd() + "/config/base_setting.py")
    if "ops_config" in os.environ:
        app.config.from_pyfile(
            os.getcwd() + "/config/%s_setting.py" % os.environ["ops_config"]
        )
    return app


app = create_app()
db = SQLAlchemy(app)
