from flask import flash, url_for, request, redirect
from flask_login import current_user
from functools import wraps
from godisbilen.app import db

def roles_accepted(*role_names):
    def wrapper(view_function):
        @wraps(view_function)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            if(not current_user.is_authenticated):
                # Redirect to unauthenticated page
                return redirect(url_for("admin_route.login"))

            # User must have the required roles
            if(not current_user.has_roles(*role_names)):
                # Redirect to the unauthorized page
                return redirect(url_for("main.home"))

            # It's OK to call the view
            return view_function(*args, **kwargs)

        return decorator
    return wrapper

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"