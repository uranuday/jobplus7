from flask import Blueprint, render_template, redirect, url_for
from jobplus.models import db, User
from jobplus.decorators import admin_required



admin = Blueprint("admin", __name__, url_prefix="/admin")



@admin.route('/')
@admin_required
def index():
    return render_template("admin/index.html")


@admin.route("/user")
@admin_required
def user():
    users = User.query.all()
    return render_template("admin/user_overview.html", users=users)


@admin.route("/user/<int:user_id>/disable")
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_disable = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("admin.user"))



@admin.route("/user/<int:user_id>/enable")
@admin_required
def enable_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_disable = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("admin.user"))



@admin.route("/user/<int:user_id>/edit")
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("admin/user_edit.html", user=user)








