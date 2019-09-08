from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config, create_db=False):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    from .main.routes import bp_main
    from .order.routes import bp_order
    from .location.routes import bp_loc
    from .admin.routes import bp_admin
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_order)
    app.register_blueprint(bp_loc)
    app.register_blueprint(bp_admin)

    if(create_db):
        with app.test_request_context():
            from godisbilen.order import Order
            from godisbilen.user import User
            from godisbilen.location import Location
            db.create_all()

    return app
