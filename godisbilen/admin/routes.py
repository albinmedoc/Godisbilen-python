from flask import Blueprint, render_template
from godisbilen.app import basic_auth

bp_admin = Blueprint("admin", __name__)

@bp_admin.route("/admin/map")
@basic_auth.required
def test():
    return render_template("admin/map.html")
