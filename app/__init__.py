# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config
from redis import Redis
import rq

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Pre prístup na túto stránku sa musíš prihlásiť.'
login_manager.login_message_category = 'danger'


def create_app(config_class=Config()):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('testovac-judge', connection=app.redis)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.users.routes import users
    from app.main.routes import main
    from app.submit.routes import submis
    from app.tasky.routes import tasky
    from app.learn.routes import learn
    from app.stats.routes import stats
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(tasky)
    app.register_blueprint(submis)
    app.register_blueprint(learn)
    app.register_blueprint(stats)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
