from flask import Blueprint, render_template,url_for, redirect, current_app, flash, send_from_directory
from flask_login import current_user
from jobplus.forms import UserProfileForm, UploadResumeForm
from jobplus.decorators import user_required
from jobplus.models import db, User, Application
from werkzeug import secure_filename
import os




user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/")
@user_required
def index():

    return redirect(url_for("user.profile"))



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
        form.resume.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
        file_url = url_for('user.resume_file', filename=filename)
        user.resume_url = file_url
        db.session.add(user)
        db.session.commit()
        flash("简历更新成功", 'success')
        return redirect(url_for("user.resume"))
    else:
        return render_template("user/upload_resume.html", form=form)


#有待实现简历保护
@user.route("/resume/<filename>")
@user_required
def resume_file(filename):
    print(os.getcwd())
    print(current_app.root_path)
    print(current_app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)



@user.route("/application")
@user_required
def application():
    applications = current_user.applications
    return render_template("user/application.html", applications = applications)




