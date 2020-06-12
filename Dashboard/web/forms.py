import flask_wtf
import re
import wtforms
import numpy as np
from datetime import date

WORK_LOCATION_REQUIRED_MSG = 'Work Location is required if Employee'
CAMPUS_REQUIRED_MSG = 'Campus is required if Employee'

def make_choices(values, include_all=True):

    unique_values = list(set(values))
    unique_values = [x for x in unique_values if x != None]
    unique_values.sort()

    if include_all:
        
        return [("", "(all)")] + [(v, v) for v in unique_values]
    else:
        return [(v, v) for v in unique_values]
 


base_sta3n_choices = [
    ("402", "402: Lincoln Community Based Outpatient Clinic"),
    ("405", "405: White River Junction Regional Office"),
    ("518", "518: Edith Nourse Rogers Memorial Veterans Hospital"),
    ("523", "523: VA Boston Healthcare System"),
    ("608", "608: Manchester VA Medical Center"),
    ("631", "631: VA Central Western MA Healthcare System"),
    ("650", "650: Providence VA Medical Center"),
    ("689", "689: VA Connecticut Healthcare System")]

sta3n_choices =[
    ("", "(all)" )] + base_sta3n_choices

sta3n_choices_add_patient = [
    ("", "")] + base_sta3n_choices
        

yes_no_choices = [
        ("", "Select..."),
        ("Yes", "Yes"),
        ("No", "No")]

person_type_choices = [
        #("", ""),
        ("Patient", "Patient"),
        ("Employee", "Employee"),
        ("Patient + Employee", "Patient + Employee"),
        ("Resident", "Resident"),
        ("Other", "Other")]

location_choices = [ ("BR 21 B","BR 21 B"),
("BR 21 C CIRCA","BR 21 C CIRCA"),
("BR 22B","BR 22B"),
("BR 22C","BR 22C"),
("BR 23B","BR 23B"),
("BR 23C","BR 23C"),
("BR 24B","BR 24B"),
("BR 24C","BR 24C"),
("BR 41B","BR 41B"),
("BR 71B","BR 71B"),
("BR 71C","BR 71C"),
("BR 72C","BR 72C"),
("BR 81B","BR 81B"),
("BR BUILDING 5","BR BUILDING 5"),
("BR BUILDING 62","BR BUILDING 62"),
("BR URGENT CARE","BR URGENT CARE"),
("CBOC BEDFORD","CBOC BEDFORD"),
("CBOC LOWELL","CBOC LOWELL"),
("CBOC PLYMOUTH","CBOC PLYMOUTH"),
("CBOC QUINCY","CBOC QUINCY"),
("HOME/COMMUNITY","HOME/COMMUNITY"),
("JP BUILDING 4 (SAARTP)","JP BUILDING 4 (SAARTP)"),
("JP HEME ONC INFUSION","JP HEME ONC INFUSION"),
("JP HEMODIALYSIS","JP HEMODIALYSIS"),
("JP PRIMARY CARE CLINIC","JP PRIMARY CARE CLINIC"),
("JP SPECIALTY CLINIC","JP SPECIALTY CLINIC"),
("JP URGENT CARE","JP URGENT CARE"),
("MANCHESTER VA","MANCHESTER VA"),
("OCCUPATIONAL HEALTH","OCCUPATIONAL HEALTH"),
("OUTSIDE HOSP: BIDMC","OUTSIDE HOSP: BIDMC"),
("OUTSIDE HOSP: BMC","OUTSIDE HOSP: BMC"),
("OUTSIDE HOSP: BRIGHAM & W","OUTSIDE HOSP: BRIGHAM & W"),
("OUTSIDE HOSP: FAULKNER","OUTSIDE HOSP: FAULKNER"),
("OUTSIDE HOSP: GOOD SAM","OUTSIDE HOSP: GOOD SAM"),
("OUTSIDE HOSP: LAHEY","OUTSIDE HOSP: LAHEY"),
("OUTSIDE HOSP: MGH","OUTSIDE HOSP: MGH"),
("OUTSIDE HOSP: TUFTS","OUTSIDE HOSP: TUFTS"),
("PROVIDENCE VA","PROVIDENCE VA"),
("WHITE RIVER JUNCTION VA","WHITE RIVER JUNCTION VA"),
("WX 2N","WX 2N"),
("WX 2S","WX 2S"),
("WX 3N","WX 3N"),
("WX A1","WX A1"),
("WX A2","WX A2"),
("WX AG","WX AG"),
("WX CCU","WX CCU"),
("WX EMERGENCY ROOM","WX EMERGENCY ROOM"),
("WX HEMODIALYSIS","WX HEMODIALYSIS"),
("WX MICU","WX MICU"),
("WX MSDU","WX MSDU"),
("WX PARKING LOT","WX PARKING LOT"),
("WX PCU","WX PCU"),
("WX PRIMARY CARE CLINIC","WX PRIMARY CARE CLINIC"),
("WX SICU","WX SICU"),
("WX SUBSPECIALTY CLINIC","WX SUBSPECIALTY CLINIC"),
("BR 21 B", "BR 21 B"),
("BR 21 C CIRCA", "BR 21 C CIRCA"),
("BR 22B", "BR 22B"),
("BR 22C", "BR 22C"),
("BR 23B", "BR 23B"),
("BR 23C", "BR 23C"),
("BR 24B", "BR 24B"),
("BR 24C", "BR 24C"),
("BR 41B", "BR 41B"),
("BR 42B", "BR 42B"),
("BR 71B", "BR 71B"),
("BR 71C", "BR 71C"),
("BR 72B", "BR 72B"),
("BR 72C", "BR 72C"),
("BR 81B", "BR 81B"),
("BR BUILDING 5", "BR BUILDING 5"),
("BR BUILDING 62", "BR BUILDING 62"),
("BR URGENT CARE", "BR URGENT CARE"),
("CBOC BEDFORD", "CBOC BEDFORD"),
("CBOC LOWELL", "CBOC LOWELL"),
("CBOC PLYMOUTH", "CBOC PLYMOUTH"),
("CBOC QUINCY", "CBOC QUINCY"),
("HOME/COMMUNITY", "HOME/COMMUNITY"),
("JP AMB/SURG", "JP AMB/SURG"),
("JP BUILDING 4 (SAARTP)", "JP BUILDING 4 (SAARTP)"),
("JP HEME ONC INFUSION", "JP HEME ONC INFUSION"),
("JP HEMODIALYSIS", "JP HEMODIALYSIS"),
("JP OCCUPATIONAL HEALTH", "JP OCCUPATIONAL HEALTH"),
("JP OR", "JP OR"),
("JP PRIMARY CARE CLINIC", "JP PRIMARY CARE CLINIC"),
("JP SPECIALTY CLINIC", "JP SPECIALTY CLINIC"),
("JP URGENT CARE", "JP URGENT CARE"),
("MANCHESTER VA", "MANCHESTER VA"),
("PROVIDENCE VA", "PROVIDENCE VA"),
("WHITE RIVER JUNCTION VA", "WHITE RIVER JUNCTION VA"),
("WX 2N", "WX 2N"),
("WX 2S", "WX 2S"),
("WX 3N", "WX 3N"),
("WX A1", "WX A1"),
("WX A2", "WX A2"),
("WX AG", "WX AG"),
("WX CCU", "WX CCU"),
("WX EMERGENCY ROOM", "WX EMERGENCY ROOM"),
("WX HEMODIALYSIS", "WX HEMODIALYSIS"),
("WX MICU", "WX MICU"),
("WX MSDU", "WX MSDU"),
("WX OR", "WX OR"),
("WX PACU", "WX PACU"),
("WX PCU", "WX PCU"),
("WX PRIMARY CARE CLINIC", "WX PRIMARY CARE CLINIC"),
("WX SICU", "WX SICU"),
("WX SUBSPECIALTY CLINIC", "WX SUBSPECIALTY CLINIC"),
("FOOD SERVICE", "FOOD SERVICE"),
("CANTEEN", "CANTEEN"),
("WX PHLEBOTOMY (MULTIPLE UNITS)", "WX PHLEBOTOMY (MULTIPLE UNITS)"),
("BR PARKING LOT", "BR PARKING LOT"),
("BR EMS (MULTIPLE UNITS)", "BR EMS (MULTIPLE UNITS)")
]

employee_role_choices = [("", "Select..."),
    ("Clinical", "Clinical"),
    ("Non-Clinical", "Non-Clinical")]

campus_choices = [("WX","WX"),
    ("JP","JP"),
    ("BR","BR"),
    ("LO","LO")]

exposure_type_choices = [("", "Select..."),
    ("COV POS", "COV POS"),
    ("work", "work"),
    ("community", "community"),
    ("travel", "travel")]

test_choices = [("", "Select..."),
                ("Positive", "Positive"),
                ("Negative", "Negative"),
                ("PUI", "PUI"),
                ("Pending", "Pending"),
                ("Refused", "Refused"), 
                ("Self-Monitoring", "Self-Monitoring"),
                ("Under Review", "Under Review"),
                ("Other", "Other")]

symptom_type_choices = make_choices([
    "New Fever (>100.4)",
    "New Subjective (feels) Fever",
    "New or Worsening Cough",
    "Chills",
    "Muscle Aches",
    "Sore Throat",
    "Runny Nose",
    "Coughing Up Blood",
    "Diarrhea",
    "Nausea or Vomiting",
    "Abdominal Pain",
    "Pink Eye",
    "Headache",
    "Shortness of Breath",
    "Fatigue",
    "Anosmia",
    "Ageusia"], include_all=False)

clinical_role_choices = [
        ("", "Select..."),
        ("Clinical", "Clinical"),
        ("Non-Clinical", "Non-Clinical")]
empl_work_locations = [
("FOOD SERVICE", "FOOD SERVICE"),
("CANTEEN", "CANTEEN"),
("WX PHLEBOTOMY (MULTIPLE UNITS)", "WX PHLEBOTOMY (MULTIPLE UNITS)"),
("BR EMS (MULTIPLE UNITS)", "BR EMS (MULTIPLE UNITS)"),
("BR 21 B", "BR 21 B"),
("BR 21 C CIRCA", "BR 21 C CIRCA"),
("BR 22B", "BR 22B"),
("BR 22C", "BR 22C"),
("BR 23B", "BR 23B"),
("BR 23C", "BR 23C"),
("BR 24B", "BR 24B"),
("BR 24C", "BR 24C"),
("BR 41B", "BR 41B"),
("BR 42B", "BR 42B"),
("BR 71B", "BR 71B"),
("BR 71C", "BR 71C"),
("BR 72B", "BR 72B"),
("BR 72C", "BR 72C"),
("BR 81B", "BR 81B"),
("BR BUILDING 5", "BR BUILDING 5"),
("BR BUILDING 62", "BR BUILDING 62"),
("BR URGENT CARE", "BR URGENT CARE"),
("CBOC BEDFORD", "CBOC BEDFORD"),
("CBOC LOWELL", "CBOC LOWELL"),
("CBOC PLYMOUTH", "CBOC PLYMOUTH"),
("CBOC QUINCY", "CBOC QUINCY"),
("HOME/COMMUNITY", "HOME/COMMUNITY"),
("JP AMB/SURG", "JP AMB/SURG"),
("JP BUILDING 4 (SAARTP)", "JP BUILDING 4 (SAARTP)"),
("JP HEME ONC INFUSION", "JP HEME ONC INFUSION"),
("JP HEMODIALYSIS", "JP HEMODIALYSIS"),
("JP OCCUPATIONAL HEALTH", "JP OCCUPATIONAL HEALTH"),
("JP OR", "JP OR"),
("JP PRIMARY CARE CLINIC", "JP PRIMARY CARE CLINIC"),
("JP SPECIALTY CLINIC", "JP SPECIALTY CLINIC"),
("JP URGENT CARE", "JP URGENT CARE"),
("MANCHESTER VA", "MANCHESTER VA"),
("PROVIDENCE VA", "PROVIDENCE VA"),
("WHITE RIVER JUNCTION VA", "WHITE RIVER JUNCTION VA"),
("WX 2N", "WX 2N"),
("WX 2S", "WX 2S"),
("WX 3N", "WX 3N"),
("WX A1", "WX A1"),
("WX A2", "WX A2"),
("WX AG", "WX AG"),
("WX CCU", "WX CCU"),
("WX EMERGENCY ROOM", "WX EMERGENCY ROOM"),
("WX HEMODIALYSIS", "WX HEMODIALYSIS"),
("WX MICU", "WX MICU"),
("WX MSDU", "WX MSDU"),
("WX OR", "WX OR"),
("WX PACU", "WX PACU"),
("WX PCU", "WX PCU"),
("WX PRIMARY CARE CLINIC", "WX PRIMARY CARE CLINIC"),
("WX SICU", "WX SICU"),
("WX SUBSPECIALTY CLINIC", "WX SUBSPECIALTY CLINIC")
]

assignee_choices =[("", "Select..."),
    ("Dennis Lacroix", "Dennis Lacroix"),
  ("Corinne Sheridan", "Corinne Sheridan"),
  ("Neah Ling", "Neah Ling"),
  ("Michelle Helm", "Michelle Helm"),
  ("Nancy Gendreau", "Nancy Gendreau"),
  ("Laura Moderi", "Laura Moderi"),
  ("Kristin Antoine", "Kristin Antoine")]


covid_choices = [("", "Select..."),
    ("PUI", "PUI"),
("Negative", "Negative"),
("Positive (New)", "Positive (New)"),
("Previous Positive (Retest Pending)", "Previous Positive (Retest Pending)"),
("Previous Positive (Retest Positive)", "Previous Positive (Retest Positive)"),
("Previous Positive (1st Consecutive Retest Negative)", "Previous Positive (1st Consecutive Retest Negative)"),
("Previous Positive (Retest Pending)", "Previous Positive (Retest Pending)"),
("Previous Positive (Retest Positive)", "Previous Positive (Retest Positive)"),
("Previous Positive (2nd Consecutive Retest Negative)", "Previous Positive (2nd Consecutive Retest Negative)"),
("Cleared to Work", "Cleared to Work"),
("Self-Monitoring", "Self-Monitoring")
]



def strip_ssn(s):
    stripped_ssn = re.sub(r'[^0-9]', "", s)
    if s and not stripped_ssn:
        return s
    else:
        return re.sub(r'[^0-9]', "", s)

def strip_address(x):
    stripped_add = re.sub(r"[^A-Za-z0-9\s\-\.\'\#]", "", x)
    if x and not stripped_add:
        return x
    else:
        return re.sub(r"[^A-Za-z0-9\s\-\.\'\#]", "", x)
      
def quote_to_none(x):
    if(x == ''):
        return(None)
    else:
        return(x)

def before_today(form, field):
    if field.data > date.today():
        raise wtforms.ValidationError('date of death after current date')

def upcase(x):
    return x.upper()

class NonValidatingSelectField(wtforms.SelectField):
    def pre_validate(self, form):
        pass 

class NonValidatingSelectMultipleField(wtforms.SelectMultipleField):
    def pre_validate(self, form):
        pass 


class PatientSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False
    SSN4 = wtforms.StringField("Last 4 Digits of SSN", filters=[strip_ssn], validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[0-9]{4}$", message = "Please type the last 4 digits of the SSN")])
    FirstName = wtforms.StringField("First Name")
    LastName = wtforms.StringField("Last Name")
    Gender = wtforms.SelectField("Gender", choices=make_choices(["M", "F"]), default="")
    PersonType = wtforms.SelectField("Person Type", choices=make_choices(["Patient","Employee","Patient + Employee","Resident","Other"], include_all=True), default="")
    AdmitStatus = wtforms.SelectField("Admission Status", choices=make_choices(["Admitted", "Never Admitted", "Discharged", "Unknown", "Not Currently Admitted (Never Admitted, Discharged, or Unknown)"], include_all=True), default="")
    MostRecentTestResult = wtforms.SelectField("Most Recent Result", choices=make_choices(["Positive", "Negative", "PUI", "Pending", "Under Review","Self-Monitoring","Refused","Other"], include_all=True), default="")
    MostRecentTestDateLo = wtforms.DateField("Test Date Start", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d', description = 'Start Date of most recent COVID-19 test', default="")
    MostRecentTestDateHi = wtforms.DateField("Test Date End", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d', description = 'End Date of most recent COVID-19 test', default="")
    Contacted = wtforms.SelectField("Contacted", choices=make_choices(["Yes", "No"]), default="")
    Sta3n = wtforms.SelectField("Station", choices = sta3n_choices, default="523") 
    InstitutionName = NonValidatingSelectField("Patient Institution",  default="",validators=[wtforms.validators.Optional()])
    WardLocationName = NonValidatingSelectField("Patient Ward", default="",validators=[wtforms.validators.Optional()])
    EmplCampus = NonValidatingSelectField("Employee Campus", default="", validators=[wtforms.validators.Optional()])
    EmplWorkLocation = NonValidatingSelectField("Employee Work Location", default="", validators=[wtforms.validators.Optional()])
    
class PatientEmployeesNoRTWDateForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False
    PersonID = wtforms.HiddenField("PersonID")
    NextURL = wtforms.HiddenField("NextURL", default="")
    Sta3n = wtforms.SelectField("Station", choices = sta3n_choices, default="523") 
    SSN4 = wtforms.StringField("Last 4 Digits of SSN", filters=[strip_ssn], validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[0-9]{4}$", message = "Please type the last 4 digits of the SSN")])
    MostRecentTestResult = NonValidatingSelectField("Most Recent COVID Status", default="", validators=[wtforms.validators.Optional()])
    EmplWorkLocation = NonValidatingSelectField("Employee Work Location", default="", validators=[wtforms.validators.Optional()])
    

class PatientContactedStatusForm(flask_wtf.FlaskForm): 
    class Meta:
        csrf = False
    PersonID = wtforms.HiddenField("PersonID")
    NextURL = wtforms.HiddenField("NextURL", default="")
    Contacted = wtforms.SelectField("Contacted", choices=[("Yes", "Yes"), ("No", "No")])
    Comment = wtforms.TextAreaField("Comment")

class PatientTrackedStatusForm(flask_wtf.FlaskForm): 
    class Meta:
        csrf = False
    PersonID = wtforms.HiddenField("PersonID")
    NextURL = wtforms.HiddenField("NextURL", default="")
    Tracked = wtforms.SelectField("Tracked", choices=[("Yes", "Yes"), ("No", "No")])
    Comment = wtforms.TextAreaField("Comment")

class PatientLookupForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False
    PersonID = wtforms.StringField("PersonID", default="")
    NextURL = wtforms.HiddenField("NextURL", default="")
    FirstName = wtforms.StringField("First Name", default="")
    LastName = wtforms.StringField("Last Name", default="")
    #SSN = wtforms.StringField("SSN", default="", validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$", message = "Invalid SSN, please correct.")], filters=[strip_ssn])
    SSN4 = wtforms.StringField("Last 4 Digits of SSN", default="", validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[0-9]{4}$", message = "Please type the last 4 digits of the SSN")])
    DOB = wtforms.DateField("Date of Birth", validators=[wtforms.validators.Optional()])
    PersonType = wtforms.SelectField("Person Type", choices=[("", "")] + person_type_choices, validators=[wtforms.validators.Optional()], default="")

class PatientAddForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False
    LastName = wtforms.StringField("Last Name", default="", validators=[wtforms.validators.DataRequired()])
    SSN = wtforms.StringField("SSN", default="", validators=[wtforms.validators.DataRequired(), wtforms.validators.Regexp("^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$", message = "Invalid SSN, please correct.")], filters=[strip_ssn])

class PatientEditForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    # Person Information
    PersonID = wtforms.HiddenField("PersonID", default="")
    NextURL = wtforms.HiddenField("NextURL", default="")
    FirstName = wtforms.StringField("First Name*", filters=[quote_to_none], validators=[wtforms.validators.DataRequired()])
    DisabledLastName = wtforms.StringField("Last Name") # use "Disabled" prefix to prevent accidental update
    DisabledSSN = wtforms.StringField("SSN") # use "Disabled" prefix to prevent accidental update
    DOB = wtforms.DateField("Date of Birth*", format = '%Y-%m-%d', validators=[wtforms.validators.DataRequired()])
    DOD = wtforms.DateField("Date of Death", format = '%Y-%m-%d', validators=[wtforms.validators.Optional(), before_today], default=None, filters = [quote_to_none])
    Phone = wtforms.StringField("Phone", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    Email = wtforms.StringField("Email Address", validators=[wtforms.validators.Email(), wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PersonType = wtforms.SelectField("Person Type*", choices=[("", "")] + person_type_choices, filters=[quote_to_none], validators=[wtforms.validators.DataRequired()])
    Sta3n = wtforms.SelectField("Station*", choices=[("", "")] + base_sta3n_choices, filters=[quote_to_none], validators=[wtforms.validators.DataRequired()])
    StreetAddress = wtforms.StringField("Street Address", validators=[wtforms.validators.Optional(),  wtforms.validators.Regexp("^[A-Za-z0-9\s\-\.\'\#]+$", message = "Please enter a valid address")], default=None, filters = [quote_to_none])
    City = wtforms.StringField("City", validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[A-Za-z0-9\s\-\.\']+$", message = "Please enter a valid city")], default=None, filters = [quote_to_none])
    County = wtforms.StringField("County", validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[A-Za-z0-9\s\-\.\']+$", message = "Please enter a valid county")], default=None, filters = [quote_to_none])
    State = wtforms.StringField("State", validators=[wtforms.validators.Optional(), wtforms.validators.Regexp("^[A-Za-z0-9\s\-\.\']+$", message = "Please enter a valid state")], default=None, filters = [quote_to_none])
    Zip = wtforms.StringField("Zip", validators=[wtforms.validators.Optional(),  wtforms.validators.Regexp("^[0-9]{5}$", message = "Please enter a valid 5 digit zip code")], default=None, filters = [quote_to_none])

    DisabledStreetAddress = wtforms.StringField("Street Address", default=None)
    DisabledCity = wtforms.StringField("City", default=None)
    DisabledCounty = wtforms.StringField("County", default=None)
    DisabledState = wtforms.StringField("State", default=None)
    DisabledZip = wtforms.StringField("Zip", default=None)

    # General
    DataEntryLocationID = NonValidatingSelectField("Location of Patient/Employee at Time of Initial Data Entry", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    AssignedInfectionStaff = wtforms.StringField("Assigned Infection Staff", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    Note = wtforms.TextAreaField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # If Patient...
    PtHospitalizedYN = wtforms.SelectField("Hospitalized?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PtCurrentLocationID = NonValidatingSelectField("Current Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PtHighComplicationRiskYN = wtforms.SelectField("High Complication Risk", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PtVABostonPCPYN = wtforms.SelectField("VA Boston PCP?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PtPCPName = wtforms.StringField("PCP Name", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    PtPCPPhone = wtforms.StringField("PCP Phone", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # If Employee...
    EmplSupervisorName = wtforms.StringField("Supervisor Name", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplSupervisorPhone = wtforms.StringField("Supervisor Phone", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplSupervisorNotifiedYN = wtforms.SelectField("Supervisor Notified", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplIDNotifiedYN = wtforms.SelectField("ID Notified", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplEmployeeRole = wtforms.StringField("Employee Role", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplCampus =  NonValidatingSelectField("Campus", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplCampusesOther = wtforms.StringField("Other Campus", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplShiftSchedule = wtforms.StringField("Shift Schedule", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplWorkLocation = NonValidatingSelectField("Work Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplPatientInteractionYN = wtforms.SelectField("Clinical/Non-Clinical Role", choices=clinical_role_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplSXSExposureWorkStartDate = wtforms.DateField("SX SE Exposure Work Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplSXSExposureWorkEndDate = wtforms.DateField("SX SE Exposure Work End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplWorkClearedYN1 = wtforms.SelectField("Cleared for Work", choices=yes_no_choices,  validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplReturnToWorkDate1 = wtforms.DateField("Return to Work Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplWorkClearedYN2 = wtforms.SelectField("Cleared for Work", choices=yes_no_choices,  validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplReturnToWorkDate2 = wtforms.DateField("Return to Work Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplWorkClearedYN3 = wtforms.SelectField("Cleared for Work", choices=yes_no_choices,  validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplReturnToWorkDate3 = wtforms.DateField("Return to Work Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplWorkClearedYN4 = wtforms.SelectField("Cleared for Work", choices=yes_no_choices,  validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplReturnToWorkDate4 = wtforms.DateField("Return to Work Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    EmplWorkClearedYN5 = wtforms.SelectField("Cleared for Work", choices=yes_no_choices,  validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    EmplReturnToWorkDate5 = wtforms.DateField("Return to Work Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')

    # Contacted Status - fields are for displaying values - will link to contact page via edit page
    Contacted = wtforms.SelectField("Contacted", choices=yes_no_choices)
    Comment = wtforms.TextAreaField("Comment")

    # Test Information
    TestDate1 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation1 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult1 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN1 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus1 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider1 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos1 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos1 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate2 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation2 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult2 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN2 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus2 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider2 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos2 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos2 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate3 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation3 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult3 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN3 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus3 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider3 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos3 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos3 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate4 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation4 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult4 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN4 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus4 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider4 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos4 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos4 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate5 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation5 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult5 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN5 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus5 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider5 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos5 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos5 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate6 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation6 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult6 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN6 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus6 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider6 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos6 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos6 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate7 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation7 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult7 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN7 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus7 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider7 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos7 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos7 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate8 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation8 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult8 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN8 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus8 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider8 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos8 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos8 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate9 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation9 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult9 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN9 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus9 = wtforms.SelectField("Covid Status", choices=covid_choices, validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none]) 
    AssignedProvider9 = NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos9 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos9 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    TestDate10 = wtforms.DateField("Test Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    TestLocation10 = NonValidatingSelectField("Test Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestResult10 = wtforms.SelectField("Test Result/COVID Status", choices=test_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    TestDriveThruNeededYN10 = wtforms.SelectField("Drive Thru Needed", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    CovidStatus10 = wtforms.SelectField("Covid Status",choices=covid_choices, validators=[wtforms.validators.Optional()],  default=None, filters=[quote_to_none])
    AssignedProvider10= NonValidatingSelectField("Assignee Provider", validators=[wtforms.validators.Optional()], default=None, filters=[quote_to_none])
    DisabledNumOfDaysSinceSinceFirstPos10 = wtforms.StringField("Number of Days Since First Pos", default=None, filters=[quote_to_none])
    NumOfConsecutiveNegTestSinceLastPos10 = wtforms.StringField("Number of Consecutive Neg Tests Since Last Pos", default=None, filters=[quote_to_none])
    
    # Quarantine
    QuarantinedYN1 = wtforms.SelectField("Quarantined?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantineStartDate1 = wtforms.DateField("Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineEndDate1 = wtforms.DateField("End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineSymptomTrackerYN1 = wtforms.SelectField("Symptom Tracker", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantinedYN2 = wtforms.SelectField("Quarantined?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantineStartDate2 = wtforms.DateField("Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineEndDate2 = wtforms.DateField("End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineSymptomTrackerYN2 = wtforms.SelectField("Symptom Tracker", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantinedYN3 = wtforms.SelectField("Quarantined?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantineStartDate3 = wtforms.DateField("Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineEndDate3 = wtforms.DateField("End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineSymptomTrackerYN3 = wtforms.SelectField("Symptom Tracker", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantinedYN4 = wtforms.SelectField("Quarantined?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantineStartDate4 = wtforms.DateField("Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineEndDate4 = wtforms.DateField("End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineSymptomTrackerYN4 = wtforms.SelectField("Symptom Tracker", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantinedYN5 = wtforms.SelectField("Quarantined?", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    QuarantineStartDate5 = wtforms.DateField("Start Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineEndDate5 = wtforms.DateField("End Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    QuarantineSymptomTrackerYN5 = wtforms.SelectField("Symptom Tracker", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # Location
    LocationChangeDateTime1 = wtforms.DateTimeField("Change Date/Time", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    LocationChangeNewLocationID1 = NonValidatingSelectField("New Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    LocationChangeDateTime2 = wtforms.DateTimeField("Change Date/Time", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    LocationChangeNewLocationID2 = NonValidatingSelectField("New Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    LocationChangeDateTime3 = wtforms.DateTimeField("Change Date/Time", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    LocationChangeNewLocationID3 = NonValidatingSelectField("New Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    LocationChangeDateTime4 = wtforms.DateTimeField("Change Date/Time", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    LocationChangeNewLocationID4 = NonValidatingSelectField("New Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    LocationChangeDateTime5 = wtforms.DateTimeField("Change Date/Time", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    LocationChangeNewLocationID5 = NonValidatingSelectField("New Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # Exposure
    ExposureDate1 = wtforms.DateField("Date of Exposure", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    ExposureType1 = wtforms.SelectField("Exposure Type", choices=exposure_type_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureLocation1 = NonValidatingSelectField("Exposure Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDetails1 = wtforms.StringField("Exposure Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDate2 = wtforms.DateField("Date of Exposure", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    ExposureType2 = wtforms.SelectField("Exposure Type", choices=exposure_type_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureLocation2 = NonValidatingSelectField("Exposure Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDetails2 = wtforms.StringField("Exposure Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDate3 = wtforms.DateField("Date of Exposure", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    ExposureType3 = wtforms.SelectField("Exposure Type", choices=exposure_type_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureLocation3 = NonValidatingSelectField("Exposure Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDetails3 = wtforms.StringField("Exposure Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDate4 = wtforms.DateField("Date of Exposure", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    ExposureType4 = wtforms.SelectField("Exposure Type", choices=exposure_type_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureLocation4 = NonValidatingSelectField("Exposure Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDetails4 = wtforms.StringField("Exposure Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDate5 = wtforms.DateField("Date of Exposure", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    ExposureType5 = wtforms.SelectField("Exposure Type", choices=exposure_type_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureLocation5 = NonValidatingSelectField("Exposure Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    ExposureDetails5 = wtforms.StringField("Exposure Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # Symptoms
    SymptomType1 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate1 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID1 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate1 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID1 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote1 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType2 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate2 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID2 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate2 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID2 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote2 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType3 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate3 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID3 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate3 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID3 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote3 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType4 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate4 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID4 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate4 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID4 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote4 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType5 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate5 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID5 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate5 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID5 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote5 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType6 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate6 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID6 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate6 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID6 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote6 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType7 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate7 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID7 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate7 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID7 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote7 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType8 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate8 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID8 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate8 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID8 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote8 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType9 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate9 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID9 = NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate9 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID9 = NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote9 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    SymptomType10 = NonValidatingSelectMultipleField("Symptom", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomOnsetDate10 = wtforms.DateField("Onset Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomOnsetLocationID10 =NonValidatingSelectField("Onset Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomResolutionDate10 = wtforms.DateField("Resolution Date", validators=[wtforms.validators.Optional()], format = '%Y-%m-%d')
    SymptomResolutionLocationID10 =NonValidatingSelectField("Resolution Location", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    SymptomNote10 = wtforms.StringField("Note", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    # Study
    PartOfStudyYN = wtforms.SelectField("Part of Study", choices=yes_no_choices, validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])
    StudyDetails = wtforms.TextAreaField("Study Details", validators=[wtforms.validators.Optional()], default=None, filters = [quote_to_none])

    """
    validates that there are not null test dates with not-null results and visa versa
    """
    def validate(self):
        # check the field validators
        rv = flask_wtf.FlaskForm.validate(self)
        if not rv:
            return False

        # check the test result and date
        for i in range(1,6):
            # get test and result number i
            test = getattr(self, 'TestDate' + str(i))
            res = getattr(self, 'TestResult' + str(i))
            
            # if just one of them is empty, return an error
            if (test.data is None) ^ (res.data is None):
                test.errors.append('Please input a test result AND a test date (or neither)')
                return False
        
        # The result of this last validation becomes the 
        # validate() return value (True if successful; False otherwise)
        return self.validate_other_empl_fields()    
    
    """
        Validates other form fields related to the Employee PersonType
        Returns: True if validation passed; false otherwise
    """
    def validate_other_empl_fields(self):
        if 'Employee' in str(getattr(self, 'PersonType').data):
            empl_campus = getattr(self, 'EmplCampus')
            work_location = getattr(self, 'EmplWorkLocation')
            if empl_campus.data is None or work_location.data is None:
                if empl_campus.data is None:
                    empl_campus.errors.append(CAMPUS_REQUIRED_MSG)
                if work_location.data is None:
                    work_location.errors.append(WORK_LOCATION_REQUIRED_MSG)
                return False
        return True
