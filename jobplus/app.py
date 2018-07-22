from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.models import db
from flask_login import LoginManager


#后面还要加上flask_login的user_loader函数
def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

def register_blueprints(app):
    from .handlers import front, admin, jobs, user, company
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(jobs)
    app.register_blueprint(user)
    app.register_blueprint(company)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_extensions(app)
    register_blueprints(app)

    return app
