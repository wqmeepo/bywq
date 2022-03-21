from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # 注册蓝图
    from app.home import home as home_blueprint
    from app.bs import bs as bs_blueprint
    from app.workspace import workspace as workspace_blueprint
    from app.jymng import jymng as jymng_blueprint
    # from app.admin import admin as admin_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(bs_blueprint, url_prefix='/bs')
    app.register_blueprint(workspace_blueprint, url_prefix='/workspace')
    app.register_blueprint(jymng_blueprint, url_prefix='/jymng')
    # app.register_blueprint(admin_blueprint, url_prefix="/admin")
    return app
