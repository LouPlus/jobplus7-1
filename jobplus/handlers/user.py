from flask import Blueprint, render_template
from werkzeug import secure_filename
from flask_login import login_required
from jobplus.forms import PersonalForm
from jobplus.models import Personal



user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile', methods=['POST','GET'])
@login_required
def profile():
    form = PersonalForm()
    if form.validate_on_submit():
        person = Personal()
    
    return render_template('user/profile.html',form=form)

