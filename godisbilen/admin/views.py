from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException, Unauthorized
from flask import redirect, Response
from godisbilen.app import basic_auth


class AdminView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated. Refresh the page.")

        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(basic_auth.challenge())


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(message, 401, {"WWW-Authenticate": "Basic realm='Login Required'"}))
