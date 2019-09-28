from flask import flash, url_for, request, redirect
from flask_login import current_user
from functools import wraps
from godisbilen.app import db

def roles_accepted(*role_names):
    def wrapper(view_function):

        @wraps(view_function)
        def decorator(*args, **kwargs):
            allowed = current_user.is_authenticated
            if(not allowed):
                flash("You must be logged in to visit that page", "danger")
                return redirect(url_for("admin_route.login", next=request.url))
            elif(not current_user.has_roles(role_names)):
                flash("You don´t have permission to visit that page", "danger")
                return redirect(url_for("main.home"))
            return view_function(*args, **kwargs)
        return decorator
    return wrapper

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"