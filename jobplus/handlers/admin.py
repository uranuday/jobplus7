from flask import Blueprint, render_template
from jobplus.models import User




admin = Blueprint("admin", __name__, url_prefix="/admin")



@admin.route('/')
def index():
    return render_template("admin/index.html")


@admin.route("/user")
def user():
    users = User.query.all()
    return render_template("admin/user.html", users=users)


