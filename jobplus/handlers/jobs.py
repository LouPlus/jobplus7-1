from flask import Blueprint, render_template
from jobplus.models import Job

job = Blueprint('job', __name__, url_prefix='/jobs')

@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('company/job_detail.html', job=job)


