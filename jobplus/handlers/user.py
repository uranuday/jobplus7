from flask import Blueprint, render_template,url_for, redirect
from flask_login import current_user
from jobplus.forms import UserProfileForm
from jobplus.decorators import user_required


user = Blueprint("user", __name__, url_prefix="/user")



@user.route("/")
@user_required
def index():

    return render_template("user/index.html")



@user.route("/profile", methods=["GET", "POST"])
@user_required
def profile():

    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_user(current_user)
        return redirect(url_for("user.profile"))

    return render_template("user/profile.html", form = form)
