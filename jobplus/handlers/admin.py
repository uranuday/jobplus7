from flask import Blueprint, render_template, redirect, url_for
from jobplus.models import db, User, Job
from jobplus.decorators import admin_required
from jobplus.forms import AddUserForm, AddCompanyForm, EditUserForm, EditCompanyForm



admin = Blueprint("admin", __name__, url_prefix="/admin")



@admin.route('/')
@admin_required
def index():
    return redirect(url_for("admin.user"))


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



@admin.route("/user/<int:user_id>/edit", methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == user.ROLE_COMPANY:
        form = EditCompanyForm(obj=user.company)
        form.username.data = user.username
        form.email.data = user.email
        if form.validate_on_submit():
            form.update_company_user(user)
            return redirect(url_for("admin.user"))
        else:
            return render_template("admin/edit_user.html", form=form, user_id=user_id)
    else:
        form = EditUserForm(obj=user)
        if form.validate_on_submit():
            form.update_user(user)
            return redirect(url_for("admin.user"))
        else:
            return render_template("admin/edit_user.html", form=form, user_id=user_id)



@admin.route("/user/adduser", methods=['GET', 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        form.add_user()
        return redirect(url_for("admin.user"))
    else:
        return render_template("admin/add_user.html", form=form)



@admin.route("/user/addcompany", methods=['GET', 'POST'])
@admin_required
def add_company():
    form = AddCompanyForm()
    if form.validate_on_submit():
        form.add_company_user()
        return redirect(url_for("admin.user"))
    else:
        return render_template("admin/add_company.html", form=form)



