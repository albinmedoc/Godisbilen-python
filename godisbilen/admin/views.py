from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_roles("Admin")
