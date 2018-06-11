from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort
from jobplus.models import db, Job, Application
import json
from flask_login import login_required, current_user
from jobplus.decorators import company_required
from jobplus.forms import JobBaseForm



job = Blueprint("job", __name__, url_prefix="/job")



@job.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(is_online=True).order_by(Job.updated_at.desc()).paginate(
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
    page = request.args.get('page', default=1, type=int)
    if current_user.is_admin:
        pagination = Job.query.paginate(
                page = page,
                per_page = current_app.config['DEFAULT_PER_PAGE'],
                error_out = False
                )
    elif current_user.is_company:
        pagination = Job.query.filter_by(company_id=current_user.company.id).paginate(
                page = page,
                per_page = current_app.config['DEFAULT_PER_PAGE'],
                error_out = False
                )
    else:
        abort(403)

    return render_template("/job/job_admin.html", pagination=pagination)


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
        abort(403)


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
        abort(403)


@job.route("/<int:job_id>/delete")
@company_required
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        db.session.delete(job)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("职位删除失败，请使用下线功能或联系管理员",'danger')
        else:
            flash("职位删除成功", 'success')
        finally:
            return redirect(url_for("job.admin"))
    else:
        abort(403)


@job.route("/<int:job_id>/edit", methods=["GET", "POST"])
@company_required
def edit(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.is_admin or job in current_user.company.jobs: 
        form = JobBaseForm(obj=job)
        if form.validate_on_submit():
            form.update_job(job)
            return redirect(url_for("job.admin"))
        else:
            return render_template("job/edit_job.html", form=form, job_id=job_id)
    else:
        abort(403)


@job.route("/new", methods=["GET", "POST"])
@company_required
def new():
    form = JobBaseForm()

    if form.validate_on_submit():
        form.add_job()
        return redirect(url_for("job.admin"))
    else:
        return render_template("job/new_job.html", form=form)


