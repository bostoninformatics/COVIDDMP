import csv
import flask
import io
import pandas as pd
import sys
import urllib
import wtforms
import pdb
import re

# import flask_bootstrap_forms
import request_proxy
import forms
import get_user_authorization

app = flask.Flask(__name__)
app.secret_key = "super_secret"
#flask_bootstrap_forms.init(app)



# Miscellenaous routes
# ====================

# Route to render the front page.
@app.route('/dashboard')
def index():
    return flask.render_template("index.html")

@app.route('/dashboard/')
def index_slash():
    return flask.redirect('/dashboard', code=301)

# Route to render static resources.
@app.route("/dashboard/static/<path:path>")
def send_static(path):
    return flask.send_from_directory("static", path)

# User Guide
# ==========

@app.route("/dashboard/user_guide")
def render_user_guide():
    return flask.render_template("COVID19_Dashboard_Introduction_User_Guide.html")

# Search page routes
# ==================

def get_current_path_with_args():
    return "{}?{}".format(flask.request.path, flask.request.query_string.decode("utf-8"))

@app.route("/dashboard/patient_search")
def render_patient_search():
    f = forms.PatientSearchForm(flask.request.args)
    person_type = f.data["PersonType"]
    r = request_proxy.get_patient_search(f)
    u = urllib.parse.quote(get_current_path_with_args())
    t = request_proxy.get_update_times()
 
    loc_vars = []
    if person_type == "Patient":
        loc_vars = ["InstitutionName", "WardLocationName"]
    elif person_type == "Employee":
        loc_vars = ["EmplCampus", "EmplWorkLocation"]

    if loc_vars: 
        k=loc_vars[0]
        j=loc_vars[1]
        f[k].choices = forms.make_choices(request_proxy.get_search_dropdown_choices(k))
        f[j].choices = forms.make_choices(r[j])

    # check for errors in input (SSN and DOB) and flash them
    if not f.validate():
        for key in f.errors.keys():
            flask.flash(f.errors.get(key)[0])
    is_auth_for_csv = get_user_authorization.is_authorized_for_csv()

    return flask.render_template("patient_search.html", form=f, result=r, next_url=u, times=t, person_type=person_type, is_auth_for_csv=is_auth_for_csv)

@app.route("/dashboard/patient_search_emp_no_rtw_date")
def patient_search_emp_no_rtw_date():
    f = forms.PatientEmployeesNoRTWDateForm(flask.request.args)
    r = request_proxy.get_patient_search_emp_no_rtw_date(f)
    u = urllib.parse.quote(get_current_path_with_args())
 
    columns = ["EmplWorkLocation", "MostRecentTestResult"]
    for column in columns:
        f[column].choices = forms.make_choices(r[column])

    return flask.render_template("patient_search_emp_no_rtw_date.html", next_url=u, form=f, result=r)

@app.route("/dashboard/patient_csv")
def export_patient_csv():    
    auth_for_csv = get_user_authorization.is_authorized_for_csv()

    if auth_for_csv:
        f = forms.PatientSearchForm(flask.request.args)
        r = request_proxy.get_patient_search(f, csv=True)
        if "SSN" in r.columns:
            r = r.drop("SSN", axis=1)
        if "PatientSSN" in r.columns:
            r = r.drop("PatientSSN", axis=1)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(r.columns)
        for i in range(r.shape[0]):
            writer.writerow(r.iloc[i])
        return flask.Response(output.getvalue(),
                              mimetype = "text/csv",
                              headers={"Content-disposition": "attachment; filename=patient_search.csv"})
    else:
        return flask.render_template("not_authorized_for_csv.html")

@app.route("/dashboard/patient_detail")
def render_patient_detail():
    r = request_proxy.get_patient_detail(flask.request.args)
    return flask.render_template("patient_detail.html", result=r)


# Contacted and tracked status routes
# ===================================

@app.route("/dashboard/patient_contacted_status", methods=["POST", "GET"])
def render_patient_contacted_status():
    r = request_proxy.get_patient_contacted_status(flask.request.args)
    f = forms.PatientContactedStatusForm(flask.request.args, data=r["current"])
    p = request_proxy.get_PersonCombined_row_by_person_id(flask.request.args)
    return flask.render_template("patient_contacted_status.html", form=f, result=r, patient=p)

@app.route("/dashboard/patient_contacted_status_post")
def render_patient_contacted_status_post():
    f = forms.PatientContactedStatusForm(flask.request.args)
    request_proxy.post_patient_contacted_status(f.data)
    if f.data["NextURL"] != "":
        next_url = f.data["NextURL"]
    else:
        next_url = "/dashboard/patient_search"
    return flask.redirect(next_url, code=302)

@app.route("/dashboard/patient_tracked_status", methods=["POST", "GET"])
def render_patient_tracked_status():
    r = request_proxy.get_patient_tracked_status(flask.request.args)
    f = forms.PatientTrackedStatusForm(flask.request.args, data=r["current"])
    p = request_proxy.get_PersonCombined_row_by_person_id(flask.request.args)
    return flask.render_template("patient_tracked_status.html", form=f, result=r, patient=p)

@app.route("/dashboard/patient_tracked_status_post")
def render_patient_tracked_status_post():
    f = forms.PatientTrackedStatusForm(flask.request.args)
    request_proxy.post_patient_tracked_status(f.data)
    if f.data["NextURL"] != "":
        next_url = f.data["NextURL"]
    else:
        next_url = "/dashboard/patient_search"
    return flask.redirect(next_url, code=302)


# Patient add and edit
# ====================

@app.route("/dashboard/patient_lookup")
def render_patient_lookup():
    f = forms.PatientLookupForm(flask.request.args)
    r = request_proxy.get_patient_lookup_results(f)
    u = urllib.parse.quote(get_current_path_with_args())

    # check for errors in input (SSN and DOB) and flash them
    if not f.validate():
        for key in f.errors.keys():
            flask.flash(f.errors.get(key)[0])
    return flask.render_template("patient_lookup.html", form=f, next_url=u, result=r)

@app.route("/dashboard/patient_add", methods=["GET", "POST"])
def render_patient_add():
    init_data = {"SSN": flask.request.args.get("SSN", ""),
                 "LastName": flask.request.args.get("LastName", "")}
    f = forms.PatientAddForm(flask.request.form, data=init_data)
    if f.validate_on_submit():
        person_id_unquoted = request_proxy.post_patient_add(f)
        if person_id_unquoted == "person exists":
            flask.flash('Person exists already, please search for and edit person or verify their lastname and SSN')
            quoted_ssn = urllib.parse.quote(str(f.SSN.data))
            quoted_lastname = urllib.parse.quote(str(f.LastName.data))
            return flask.redirect("/dashboard/patient_lookup?SSN={}&LastName={}".format(quoted_ssn, quoted_lastname), code=302)
        else:   
            person_id  = urllib.parse.quote(str(person_id_unquoted))
            return flask.redirect("/dashboard/patient_edit?PersonID=" + person_id, code=302)
    else:
        for key in f.errors.keys():
            flask.flash(f.errors.get(key)[0])
        return flask.render_template("patient_add.html", form=f)

@app.route("/dashboard/patient_edit", methods=["GET", "POST"])
def render_patient_edit():
    # Get data to populate the form.
    if flask.request.args.get("PersonID", "") == "":
        flask.flash("Person not found, try looking them up here")
        return flask.redirect("/dashboard/patient_lookup", code=302)
    r = request_proxy.get_patient_for_editing(flask.request.args)
    if r == "patient not found":
        flask.flash("Person not found, try looking them up here")
        return flask.redirect("/dashboard/patient_lookup", code=302)

    # Define form, initialized with PersonCombined and PersonCrosswalk values.
    f = forms.PatientEditForm(flask.request.form, data=r["PersonCombined"],
            PersonID = flask.request.args.get("PersonID"),
            DisabledLastName=r["PersonCrosswalk"]["PatientLastName"],
            DisabledSSN="***-**-{}".format(r["PersonCrosswalk"]["PatientSSN"][5:9]),
            NextURL=flask.request.args.get("NextURL", "/dashboard/patient_lookup"))

    symptom_fields = ["SymptomType" + str(n) for n in list(range(1, 11))]

    # Populate the symptom field values when GETting patient data
    # doing it this way because these fields aren't populating in the construction above 
    if flask.request.method == "GET" and r["PersonCombined"]:
        for k in symptom_fields:
            f[k].data = r["PersonCombined"][k]
    
    # Assert that the PersonCombined dict returned has the same keys as the form to ensure that new fields
    # are added to both. Exclude any hidden form fields that have no database equivalent.
    hidden_fields = ["NextURL", "DisabledLastName", "DisabledSSN", "DisabledStreetAddress", "DisabledCity",
                     "DisabledCounty", "DisabledState", "DisabledZip"]
    if "PersonId" in r["PersonCombined"]: # Verify person is not new
        for form_key in f.data.keys():
            if form_key not in hidden_fields:
                assert form_key in r["PersonCombined"].keys(), "KeyNotFound:" + form_key

    # Populate choices for free-text dropdown fields
    # get lists of fields that need choice
    location_fields =  (["PtCurrentLocationID", "DataEntryLocationID"] + 
                       ["ExposureLocation" + str(n) for n in list(range(1, 6))]+
                       ["TestLocation" + str(n) for n in list(range(1, 11))]+ 
                       ["LocationChangeNewLocationID" + str(n) for n in list(range(1, 6))]+
                       ["SymptomOnsetLocationID" + str(n) for n in list(range(1, 11))]+
                       ["SymptomResolutionLocationID" + str(n) for n in list(range(1, 11))])

    assignee_fields = ["AssignedProvider" + str(n) for n in list(range(1, 11))] 
    # group list of fields with their choices
    open_list = [(location_fields, forms.location_choices) , (symptom_fields, forms.symptom_type_choices), (assignee_fields, forms.assignee_choices), (["EmplCampus"], forms.campus_choices), (["EmplWorkLocation"], forms.empl_work_locations)]

    for (fields, choices) in open_list: 
        # choices is list tuples
        # create white_list_choices as the first value in each tuple from choices
        white_list_choices = [x[0] for x in choices] # "white list" here means it's the list of non-"Other"/non-UserEntered choices
        # populate choices for each field
        for k in fields:
            if not isinstance(f[k].data, list): # single select fields
                if f[k].data in white_list_choices or f[k].data in [None, "None"]:
                    f[k].choices = [("", "Select...")] + forms.make_choices(white_list_choices, include_all=False)
                else:
                    f[k].choices = [("", "Select...")] + forms.make_choices(white_list_choices, include_all=False) + forms.make_choices([f[k].data], include_all=False)
            else: # for the select multiple fields
                values_not_in_white_list = list(set(f[k].data)-set(white_list_choices))
                if values_not_in_white_list is None:
                    f[k].choices = [("", "Select...")] + forms.make_choices(white_list_choices, include_all=False) 
                else:
                    f[k].choices = [("", "Select...")] + forms.make_choices(white_list_choices, include_all=False) + forms.make_choices(values_not_in_white_list, include_all=False)
                
    # Populate Personal Information (Per Vista) box
    for k in ["StreetAddress", "City", "County", "State", "Zip"]:
        j = "Disabled" + k
        f[j].render_kw = {}
        f[j].render_kw["value"] = r["PersonCDW"][k]

    # Validate form and either show page or update patient, as appropriate.
    if f.validate_on_submit():                             
        request_proxy.post_patient_edit(f)
        return flask.redirect(f.data["NextURL"], code=302)
    else:
        return flask.render_template("patient_edit.html", form=f, result=r)


# Summary pages routes
# ====================

@app.route("/dashboard/summary")
def render_summary():
    r = request_proxy.get_summary()
    return flask.render_template("summary.html", result=r)

# Test routes
# ===========

@app.route("/dashboard/test", methods=["POST", "GET"])
def render_test():
    return flask.render_template("test.html", request=flask.request)

