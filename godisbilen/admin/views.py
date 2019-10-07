from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_roles("Admin")
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("admin_route.login", next=request.url))
