from flask import Blueprint, render_template
from flask.ext.login import current_user
from jobplus.forms import CompanyProfileForm



company = Blueprint("company", __name__, url_prefix="/company")



@company.route("/")
def index():

    return render_template("company/index.html")



@company.route("/profile")
def profile():

    form = CompanyProfileForm(obj=current_user.company)
    if form.validate_on_submit():
        form.update_company
    else:
        return render_template("company/profile.html", form=form)




