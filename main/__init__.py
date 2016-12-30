from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = None
def create_app(config_name):
    global db
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    config[config_name].init_app(app)
    databaseurl = 'mysql+pymysql://%s:%s@%s:%s/%s' % (app.config["MYSQL_USER"],app.config["MYSQL_PASS"],app.config["MYSQL_HOST"],app.config["MYSQL_PORT"],app.config["MYSQL_DB"])
    app.config['SQLALCHEMY_DATABASE_URI'] =databaseurl
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    db = SQLAlchemy(app)
    from users import users as users_blueprint
    app.register_blueprint(users_blueprint)
    from customers import customers as customers_blueprint
    app.register_blueprint(customers_blueprint)
    from offers import offers as offers_blueprint
    app.register_blueprint(offers_blueprint)
    from facebookData import facebookDate as facebook_blueprint
    app.register_blueprint(facebook_blueprint)

    return app