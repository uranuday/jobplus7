from flask import Blueprint, render_template
from flask_login import login_required
from flask.ext.login import current_user
from jobplus.forms import UserProfileForm



user = Blueprint("user", __name__, url_prefix="/user")



@login_required
@user.route("/")
def index():

    return render_template("user/index.html")



@login_required
@user.route("/profile", methods=["GET", "POST"])
def profile():

    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_user(current_user)

    return render_template("user/profile.html", form = form)
