from flask import  Blueprint, render_template, flash, redirect, url_for, request, current_app
from jobplus.models import User, Company, Job
from jobplus.forms import LoginForm, AddUserForm, AddCompanyForm
from flask_login import login_user, logout_user, login_required



front = Blueprint('front', __name__)



@front.route('/')
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(12)
    companies = Company.query.order_by(Company.created_at.desc()).limit(12)


    return render_template('index.html', jobs=jobs, companies=companies)




@front.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash("用户被禁用", 'danger')
            return render_template('login.html', form=form)
        else:
            login_user(user, form.remember_me.data)

        if user.is_admin:
            return redirect(url_for('admin.user'))
        elif user.is_company:
            return redirect(url_for('company.profile'))
        else:
            return redirect(url_for('user.profile'))

    else:
        return render_template('login.html', form=form)



@front.route("/logout")
@login_required
def logout():
    logout_user()
    flash("您已安全退出","success")
    return redirect(url_for(".index"))


@front.route("/jobs")
def job():
    return render_template("jobs.html")


@front.route("/userregister", methods=["GET", "POST"])
def user_register():
    form = AddUserForm()
    if form.validate_on_submit():
        form.add_user()
        return redirect(url_for('front.login'))
    else:
        return render_template("user_register.html", form=form)


@front.route("/companyregister", methods=["GET", "POST"])
def company_register():
    form = AddCompanyForm()
    if form.validate_on_submit():
        form.add_company_user()
        return redirect(url_for("front.login"))
    else:
        return render_template("company_register.html", form=form)



