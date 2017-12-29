from flask import Blueprint, render_template, redirect, url_for, request, current_app
from jobplus.models import Job
import json




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


@job.route("/<job_id>")
def detail(job_id):
    job = Job.query.get(job_id)
    job_desc = json.loads(job.description).values()
    return render_template("/job/job_detail.html", job=job, job_desc=job_desc)
