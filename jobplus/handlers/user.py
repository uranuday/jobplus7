from flask import Blueprint, render_template,url_for, redirect, current_app, flash, send_from_directory
from flask_login import current_user
from jobplus.forms import UserProfileForm, UploadResumeForm
from jobplus.decorators import user_required
from jobplus.models import db, User
from werkzeug import secure_filename



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



@user.route("/resume", methods=['GET', 'POST'])
@user_required
def resume():
    form = UploadResumeForm()
    if form.validate_on_submit():
        user = current_user
        filename = secure_filename(form.resume.data.filename)
        filename = user.username + '-' + filename
        form.resume.data.save(current_app.config['UPLOAD_FOLDER'] + filename)
        user.resume_file_name = filename
        db.session.add(user)
        db.session.commit()
        flash("简历更新成功", 'success')
        return redirect(url_for("user.resume"))
    else:
        return render_template("user/upload_resume.html", form=form)



@user.route("/resume/<filename>")
@user_required
def resume_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)







