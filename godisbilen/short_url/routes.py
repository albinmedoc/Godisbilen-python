from flask import Blueprint, request, jsonify, redirect
from .short_url import ShortUrl
from godisbilen.app import db
from godisbilen.user import roles_accepted

bp_short = Blueprint("short", __name__)

@bp_short.route("/short/<short_url>")
def redirect_to_url(short_url):
    short_url = ShortUrl.query.filter_by(short_url=short_url).first_or_404()
    short_url.visits = short_url.visits + 1
    db.session.commit()
    return redirect(short_url.original_url)



@bp_short.route("/short/add_link", methods=["POST"])
def add_link():
    original_url = request.form.get("original_url")
    short_url = ShortUrl(original_url=original_url)
    db.session.add(short_url)
    db.session.commit()
