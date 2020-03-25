from flask import Blueprint, request, jsonify, redirect, render_template, url_for
from .short_url import ShortUrl
from .forms import ShortURLForm
from godisbilen.app import db
from godisbilen.user import roles_accepted

bp_short = Blueprint("short", __name__)

@bp_short.route("/short/<short_url>")
def redirect_to_url(short_url):
    short_url = ShortUrl.query.filter_by(short_url=short_url).first_or_404()
    short_url.visits = short_url.visits + 1
    db.session.commit()
    return redirect(short_url.original_url)



@bp_short.route("/short/add_link", methods=["GET", "POST"])
@roles_accepted("Admin")
def add_link():
    form = ShortURLForm()
    if(form.validate_on_submit() and request.method=="POST"):
        short_url = ShortUrl(original_url=form.original_url.data)
        db.session.add(short_url)
        db.session.commit()
        return render_template("short_url/create.html", form=form, result=url_for("short.redirect_to_url", short_url=short_url.short_url, _external=True))
    return render_template("short_url/create.html", form=form)
