from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort
from jobplus.models import db, Job, Application
import json
from flask_login import login_required, current_user
from jobplus.decorators import company_required



job = Blueprint("job", __name__, url_prefix="/job")



@job.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page=current_app.config['DEFAULT_PER_PAGE'],
            error_out=False
            )

    return render_template("job/index.html", pagination=pagination)


@job.route("/<int:job_id>")
def detail(job_id):
    job = Job.query.get(job_id)
    return render_template("/job/job_detail.html", job=job)


@job.route("/<int:job_id>/apply")
@login_required
def apply(job_id):
    if current_user.resume_url is None:
        flash("请上传简历",'warning')
        return redirect(url_for("user.resume"))
    job = Job.query.get_or_404(job_id)
    application = Application(job_id=job.id, user_id=current_user.id)
    db.session.add(application)
    db.session.commit()
    flash("投递成功", 'success')
    return redirect(url_for("job.detail", job_id=job.id))




@job.route("/admin")
@company_required
def admin():
    if current_user.is_admin:
        jobs = Job.query.all()[0:12]
    elif current_user.is_company:
        jobs = current_user.company.jobs
    else:
        abort(404)

    return render_template("/job/job_admin.html", jobs=jobs)


@job.route("/<int:job_id>/disable")
@company_required
def disable(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        job.is_online = False
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("job.admin"))
    else:
        abort(404)


@job.route("/<int:job_id>/enable")
@company_required
def enable(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        job.is_online = True
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("job.admin"))
    else:
        abort(404)


@job.route("/<int:job_id>/delete")
@company_required
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        db.session.delete(job)
        db.session.commit()
        flash("职位删除成功", 'success')
        return redirect(url_for("job.admin"))
    else:
        abort(404)


@job.route("/<int:job_id>/edit")
@company_required
def edit(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        return render_template("job/edit_job.html", job=job)
    else:
        abort(404)





