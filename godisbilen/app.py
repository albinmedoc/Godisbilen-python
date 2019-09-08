from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from config import Config

db = SQLAlchemy()
basic_auth = BasicAuth()
admin = Admin(name="Godisbilen", endpoint="flask_admin")


def create_app(config_class=Config, create_db=False):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    basic_auth.init_app(app)

    from .main.routes import bp_main
    from .order.routes import bp_order
    from .location.routes import bp_loc
    from .admin.routes import bp_admin
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_order)
    app.register_blueprint(bp_loc)
    app.register_blueprint(bp_admin)

    from godisbilen.order import Order
    from godisbilen.user import User
    from godisbilen.location import Location

    if(create_db):
        with app.test_request_context():
            db.create_all()

    from godisbilen.order.views import OrderView
    from godisbilen.user.views import UserView
    from godisbilen.location.views import LocationView

    admin.add_view(OrderView(Order, db.session, endpoint="orders"))
    admin.add_view(UserView(User, db.session, endpoint="users"))
    admin.add_view(LocationView(Location, db.session, endpoint="locations"))
    admin.init_app(app)

    return app
