from flask import Blueprint, render_template
from jobplus.models import User
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
    return render_template("admin/user.html", users=users)


