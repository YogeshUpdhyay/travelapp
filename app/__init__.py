import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from importlib import import_module

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
admin = Admin()

def dbInit(app):
    # initializing database
    db.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def init_extensions(app):
    CORS(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

def initadmin():
    for module_name in ['main']:
        module = import_module('app.{}.admin'.format(module_name))


def include_blueprints(app):
    for module_name in ['auth','main', 'membership']:
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.bp)

def create_app(config_name):
    # initializing app
    appconf = config[config_name]
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), appconf.TEMPLATE_DIR),
        static_folder=os.path.join(os.getcwd(), appconf.STATIC_DIR),
    )
    app.config.from_object(appconf)

    # configuring database
    dbInit(app)
    migrate = Migrate(app, db)

    # initializing extensions
    init_extensions(app)

    # registering blueprints
    include_blueprints(app)

    # initializing admin
    initadmin()

    return app
