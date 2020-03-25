import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import MenuLink
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
mail = Mail()
admin = Admin(name="Godisbilen", url="/admin/db", template_mode="bootstrap3")
bcrypt = Bcrypt()
login = LoginManager()
cors = CORS()

def create_app(config_class=Config, create_db=False):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    cors.init_app(app)

    # Register Blueprints
    from .main.routes import bp_main
    from .order.routes import bp_order
    from .region.routes import bp_region
    from .admin.routes import bp_admin
    from .api import bp_api
    from .short_url.routes import bp_short
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_order)
    app.register_blueprint(bp_region)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_short)

    # Register database models
    from godisbilen.order_number import OrderNumber
    from godisbilen.order import Order
    from godisbilen.user import User
    from godisbilen.admin import Admin
    from godisbilen.user.role import Role
    from godisbilen.location import Location
    from godisbilen.region import Region
    from godisbilen.short_url import ShortUrl

    if(create_db):
        with app.test_request_context():
            db.create_all()

    # Register database views

    from godisbilen.order.views import OrderView
    from godisbilen.user.views import UserView
    from godisbilen.location.views import LocationView
    from godisbilen.region.views import RegionView
    from godisbilen.short_url.views import ShortURLView

    path = os.path.join(os.path.dirname(__file__), "static")
    admin.add_view(FileAdmin(path, "/static/", name="Filer"))
    admin.add_view(OrderView(Order, db.session, endpoint="orders", name="Ordrar", menu_icon_type="glyph", menu_icon_value="glyphicon-earphone"))
    admin.add_view(UserView(User, db.session, endpoint="users", name="Användare", menu_icon_type="glyph", menu_icon_value="glyphicon-user"))
    admin.add_view(LocationView(Location, db.session, endpoint="location", name="Adresser", menu_icon_type="glyph", menu_icon_value="glyphicon-map-marker"))
    admin.add_view(RegionView(Region, db.session, endpoint="region", name="Områden", menu_icon_type="glyph", menu_icon_value="glyphicon-globe"))
    admin.add_view(ShortURLView(ShortUrl, db.session, endpoint="short_url", name="Korta URLer", menu_icon_type="glyph", menu_icon_value="glyphicon-link"))
    admin.add_link(MenuLink(name="Admin Hem", endpoint="admin_route.home", icon_type="glyph", icon_value="glyphicon-home"))
    admin.init_app(app)

    return app
