from flask import Blueprint, render_template, url_for, redirect, request, current_app, flash, abort
from flask_login import current_user
from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required
from jobplus.models import db, Company, Application



company = Blueprint("company", __name__, url_prefix="/company")



@company.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.paginate(
            page = page,
            per_page = current_app.config['DEFAULT_PER_PAGE'],
            error_out = False
            )
    return render_template("company/index.html", pagination=pagination)



@company.route("/admin")
@company_required
def admin():
    return redirect(url_for("company.profile"))



#更新企业信息
@company.route("/admin/profile", methods=['GET', 'POST'])
@company_required
def profile():

    form = CompanyProfileForm(obj=current_user.company)
    if form.validate_on_submit():
        form.update_company(current_user.company)
        return redirect(url_for("company.profile"))
    else:
        return render_template("company/profile.html", form=form)


@company.route("/admin/application")
@company_required
def job_application():
    return redirect(url_for("company.job_appl_waiting_list"))


@company.route("/admin/application/waiting")
@company_required
def job_appl_waiting_list():
    jobs = current_user.company.jobs
    applications = []
    waiting_list = []
    for job in jobs:
        applications += job.applications
    for application in applications:
        if application.status == Application.WAITING:
            waiting_list.append(application)
    return render_template("company/job_application.html", application_list=waiting_list, button='waiting')


@company.route("/admin/application/accept")
@company_required
def job_appl_accept_list():
    jobs = current_user.company.jobs
    applications = []
    accept_list = []
    for job in jobs:
        applications += job.applications
    for application in applications:
        if application.status == Application.ACCEPTED:
            accept_list.append(application)
    return render_template("company/job_application.html", application_list=accept_list, button='accept')


@company.route("/admin/application/reject")
@company_required
def job_appl_reject_list():
    jobs = current_user.company.jobs
    applications = []
    reject_list = []
    for job in jobs:
        applications += job.applications
    for application in applications:
        if application.status == Application.REJECTED:
            reject_list.append(application)
    return render_template("company/job_application.html", application_list=reject_list, button='reject')




@company.route("/admin/application/<int:application_id>/accept")
@company_required
def accept_application(application_id):
    application = Application.query.filter_by(id=application_id).first()
    if application.job not in current_user.company.jobs:
        return abort(403)
    application.status = Application.ACCEPTED
    db.session.add(application)
    db.session.commit()
    flash("申请已接受",'success')
    return redirect(url_for("company.job_application"))


@company.route("/admin/application/<int:application_id>/reject")
@company_required
def reject_application(application_id):
    application = Application.query.filter_by(id=application_id).first()
    if application.job not in current_user.company.jobs:
        return abort(403)
    application.status = Application.REJECTED
    db.session.add(application)
    db.session.commit()
    flash("申请已拒绝",'danger')
    return redirect(url_for("company.job_application"))




@company.route("/<company_id>")
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company/company_detail.html", company=company, tab="company")


@company.route("/<company_id>/jobs")
def jobs(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template("company/company_jobs.html", company=company, tab="job")
