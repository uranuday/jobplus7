from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from jobplus.models import db, Job, Application
import json
from flask_login import login_required, current_user



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
