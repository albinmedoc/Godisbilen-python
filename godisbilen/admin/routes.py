from flask import Blueprint, render_template

bp_admin = Blueprint("admin", __name__)

@bp_admin.route("/admin/map")
def test():
    return render_template("admin/map.html")