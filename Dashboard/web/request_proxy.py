import datetime
import flask
import numpy as np
import pandas as pd
import sys
import re
import connect
import coalesce_test_results

engine, staging_schema, app_schema = connect.sql_connect()

def is_empty_form_value(v):
    return (v == "") or (v == "None") or (v is None)

def get_current_user():
    return flask.request.headers.get("Userid", "").upper()
    
def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_table_by_person_id(table, person_id, schema=staging_schema, fields="default"):
    """This function reads all the rows in `table` where the PersonID equals
    `person_id` and returns them as a data frame.
    """
    if fields == "default":
        columns = " * "
    elif fields == "Edit":
        columns = " [PersonID], [FirstName], [LastName], [SSN], [DOB], [Phone], [Email], [PersonType], [DataEntryLocationID], [AssignedInfectionStaff], [Note], [PartOfStudyYN], [StudyDetails], [PtHospitalizedYN], [PtCurrentLocationID], [PtHighComplicationRiskYN], [PtContactedYN], [PtDateLastContacted], [PtVABostonPCPYN], [PtPCPName], [PtPCPPhone], [EmplSupervisorName], [EmplSupervisorPhone], [EmplSupervisorNotifiedYN], [EmplIDNotifiedYN], [EmplEmployeeRole], [EmplCampus], [EmplCampusesOther], [EmplShiftSchedule], [EmplWorkLocation], [EmplPatientInteractionYN], [EmplSXSExposureWorkStartDate], [EmplSXSExposureWorkEndDate], [EmplWorkClearedYN1], [EmplReturnToWorkDate1] ,TestDate1, TestLocation1, TestResult1, TestDriveThruNeededYN1, CovidStatus1, AssignedProvider1, NumOfConsecutiveNegTestSinceLastPos1, TestDate2, TestLocation2, TestResult2, TestDriveThruNeededYN2, CovidStatus2, AssignedProvider2, NumOfConsecutiveNegTestSinceLastPos2, TestDate3, TestLocation3, TestResult3, TestDriveThruNeededYN3, CovidStatus3, AssignedProvider3, NumOfConsecutiveNegTestSinceLastPos3, TestDate4, TestLocation4, TestResult4, TestDriveThruNeededYN4, CovidStatus4, AssignedProvider4, NumOfConsecutiveNegTestSinceLastPos4, TestDate5, TestLocation5, TestResult5, TestDriveThruNeededYN5, CovidStatus5, AssignedProvider5, NumOfConsecutiveNegTestSinceLastPos5, TestDate6, TestLocation6, TestResult6, TestDriveThruNeededYN6, CovidStatus6, AssignedProvider6, NumOfConsecutiveNegTestSinceLastPos6, TestDate7, TestLocation7, TestResult7, TestDriveThruNeededYN7, CovidStatus7, AssignedProvider7, NumOfConsecutiveNegTestSinceLastPos7, TestDate8, TestLocation8, TestResult8, TestDriveThruNeededYN8, CovidStatus8, AssignedProvider8, NumOfConsecutiveNegTestSinceLastPos8, TestDate9, TestLocation9, TestResult9, TestDriveThruNeededYN9, CovidStatus9, AssignedProvider9, NumOfConsecutiveNegTestSinceLastPos9, TestDate10, TestLocation10, TestResult10, TestDriveThruNeededYN10, CovidStatus10, AssignedProvider10, NumOfConsecutiveNegTestSinceLastPos10, [QuarantinedYN1], [QuarantineStartDate1], [QuarantineEndDate1], [QuarantineSymptomTrackerYN1], [QuarantinedYN2], [QuarantineStartDate2], [QuarantineEndDate2], [QuarantineSymptomTrackerYN2], [QuarantinedYN3], [QuarantineStartDate3], [QuarantineEndDate3], [QuarantineSymptomTrackerYN3], [QuarantinedYN4], [QuarantineStartDate4], [QuarantineEndDate4], [QuarantineSymptomTrackerYN4], [QuarantinedYN5], [QuarantineStartDate5], [QuarantineEndDate5], [QuarantineSymptomTrackerYN5], [LocationChangeDateTime1], [LocationChangeNewLocationID1], [LocationChangeDateTime2], [LocationChangeNewLocationID2], [LocationChangeDateTime3], [LocationChangeNewLocationID3], [LocationChangeDateTime4], [LocationChangeNewLocationID4], [LocationChangeDateTime5], [LocationChangeNewLocationID5], [ExposureDate1], [ExposureType1], [ExposureLocation1], [ExposureDetails1], [ExposureDate2], [ExposureType2], [ExposureLocation2], [ExposureDetails2], [ExposureDate3], [ExposureType3], [ExposureLocation3], [ExposureDetails3], [ExposureDate4], [ExposureType4], [ExposureLocation4], [ExposureDetails4], [ExposureDate5], [ExposureType5], [ExposureLocation5], [ExposureDetails5], [SymptomType1], [SymptomOnsetDate1], [SymptomOnsetLocationID1], [SymptomResolutionDate1], [SymptomResolutionLocationID1], [SymptomNote1], [SymptomType2], [SymptomOnsetDate2], [SymptomOnsetLocationID2], [SymptomResolutionDate2], [SymptomResolutionLocationID2], [SymptomNote2], [SymptomType3], [SymptomOnsetDate3], [SymptomOnsetLocationID3], [SymptomResolutionDate3], [SymptomResolutionLocationID3], [SymptomNote3], [SymptomType4], [SymptomOnsetDate4], [SymptomOnsetLocationID4], [SymptomResolutionDate4], [SymptomResolutionLocationID4], [SymptomNote4], [SymptomType5], [SymptomOnsetDate5], [SymptomOnsetLocationID5], [SymptomResolutionDate5], [SymptomResolutionLocationID5], [SymptomNote5], [SymptomType6], [SymptomOnsetDate6], [SymptomOnsetLocationID6], [SymptomResolutionDate6], [SymptomResolutionLocationID6], [SymptomNote6], [SymptomType7], [SymptomOnsetDate7], [SymptomOnsetLocationID7], [SymptomResolutionDate7], [SymptomResolutionLocationID7], [SymptomNote7], [SymptomType8], [SymptomOnsetDate8], [SymptomOnsetLocationID8], [SymptomResolutionDate8], [SymptomResolutionLocationID8], [SymptomNote8], [SymptomType9], [SymptomOnsetDate9], [SymptomOnsetLocationID9], [SymptomResolutionDate9], [SymptomResolutionLocationID9], [SymptomNote9], [SymptomType10], [SymptomOnsetDate10], [SymptomOnsetLocationID10], [SymptomResolutionDate10], [SymptomResolutionLocationID10], [SymptomNote10], [Sta3n], [DOD], [EmplWorkClearedYN2], [EmplReturnToWorkDate2], [EmplWorkClearedYN3], [EmplReturnToWorkDate3], [EmplWorkClearedYN4], [EmplReturnToWorkDate4], [EmplWorkClearedYN5], [EmplReturnToWorkDate5], [StreetAddress], [City], [County], [State], [Zip] "
    elif fields == "Detail":
        columns = " SSN4, LastName, FirstName, DOB, DOD, Phone, Email, PersonType, AdmitStatus, RoomBed, WardLocationName, InstitutionName, PACT_Provider, PACT_Team, PACT_Phone, CDWUpdatedDateTime "

    q = "select {columns} from {schema}.{table} where PersonID = ?"
    q = q.format(columns=columns, schema=schema, table=table)
    tb = pd.read_sql(q, engine, params=[person_id])
    return tb

def get_most_recent_row_by_person_id(table, person_id, timestamp="UpdatedDateTime", schema=staging_schema, format="dict"):
    """This function reads the most recent row in `table` where the PersonID
    equals `person_id`, ordered by `timestamp`, and returns that row as a
    dictionary if `format` == "dict", or as a DataFrame if `format` ==
    "DataFrame".
    """
    q = ("select top 1 * " +
        "from {schema}.{table} ".format(schema=schema, table=table) +
        "where PersonID = ? " +
        "order by {timestamp} desc".format(timestamp=timestamp))
    tb = pd.read_sql(q, engine, params=[person_id])
    assert tb.shape[0] <= 1, "Expected 0 or 1 rows, but got {} rows".format(tb.shape[0])
    if format == "DataFrame":
        return tb
    elif format == "dict":
        if tb.shape[0] == 0:
            return None
        else:
            return tb.iloc[0,:].to_dict()
    else:
        raise RuntimeError("Unknown format: " + format)

def get_patient_search(form, csv=False):
    """This function selects all persons corresponding to the data in the given
    form object. For each person, we select only the most recently updated
    record.
    """
    # Get cursor.
    conn = engine.raw_connection()

    # Get form data for non-date fields.
    date_fields = ["MostRecentTestDateLo", "MostRecentTestDateHi"]
    args = form.data

    if args["PersonType"] == "Patient":
        data = {k: v for (k, v) in args.items() if not is_empty_form_value(v) and k not in date_fields + ["EmplCampus", "EmplWorkLocation"]}
    elif args["PersonType"] == "Employee":
        data = {k: v for (k, v) in args.items() if not is_empty_form_value(v) and k not in date_fields + ["InstitutionName", "WardLocationName"]}
    else:
        data = {k: v for (k, v) in args.items() if not is_empty_form_value(v) and k not in date_fields + ["InstitutionName", "WardLocationName", "EmplCampus", "EmplWorkLocation"]}
 
    # Construct the where clause and params for non-date fields.
    ands = []
    if "AdmitStatus" in data.keys() and data["AdmitStatus"] == "Not Currently Admitted (Never Admitted, Discharged, or Unknown)":
         ands.append("(AdmitStatus in ('never admitted', 'discharged', 'unknown'))")
         del data["AdmitStatus"]
    for k, _ in data.items():
        ands.append("([{}] = ?)".format(k))
    if len(ands) > 0:
        where = "and " + (" and ".join(ands))
    else:
        where = ""   
    params = [v for _, v in data.items()]

    # Construct the where clause and parameters for date fields.
    date_ands = []
    date_params = []
    
    if not is_empty_form_value(form.MostRecentTestDateLo.data):       
        date_ands.append("convert(date, MostRecentTestDateTime) >= ? ")
        date_params.append(form.MostRecentTestDateLo.data)   
    if not is_empty_form_value(form.MostRecentTestDateHi.data):
        date_ands.append("convert(date, MostRecentTestDateTime) <= ? ")
        date_params.append(form.MostRecentTestDateHi.data)
    if len(date_ands) > 0:
        date_where = "and " + (" and ".join(date_ands))
    else:
        date_where = ""

    # If called for patient-search-display, a reduced set of columns is returned to achieve better performance;
    # Otherwise, for patient-search-csv, all columns are returned.
    display_columns = ["SSN4", "LastName", "FirstName", "Sta3n," "MostRecentTestDateTime", "MostRecentTestResult", "PersonType", "InstitutionName", "WardLocationName",
    "EmplCampus", "EmplWorkLocation", "EmplEmployeeRole", "AdmitStatus", "PACT_Provider", "Contacted", "Tracked", "PersonID"]
    if csv:
        select_columns = "*"
    else:
        select_columns = ", ".join(display_columns)
    
    # Execute the main query.
    q = ("select " + select_columns + 
        " from {schema}.PersonCombined ".format(schema=app_schema) +
        "where (MostRecentTestResult is not null) " +
        where + date_where +
        " order by MostRecentTestDateTime desc")
    print(q, params + date_params, file = sys.stderr)
    tb = pd.read_sql(q, conn, params=params + date_params)
    
    tb["MostRecentTestDateTime"] = [correct_nats(x) for x in tb["MostRecentTestDateTime"]]
    tb["Sta3n"] = [correct_nans(y) for y in tb["Sta3n"]]

    return tb
 
def correct_nans(y):
    """ Correct nans so they appear as blanks and convert other choices to int.
    """
    y = str(y)
    if y == "nan":
        return ""
    else:
        y = float(y)
        return int(y)

def correct_nats(x):
    """ Correct NaTs so they sort last.
    """
    x = str(x)
    if x == "NaT":
        return ""
    else:
        return x

def get_patient_search_emp_no_rtw_date(form):
    """Selects all persons with a type of 'Employee' or 'Patient+Employee' for the given station for 
       customized search results.
    """

    conn = engine.raw_connection()
    args = form.data
    params = []
    ands = []  # List of and-ed expressions

    if not is_empty_form_value(form.Sta3n.data):       
        ands.append("Sta3n = ? ")
        params.append(form.Sta3n.data) 
    if not is_empty_form_value(form.MostRecentTestResult.data):       
        ands.append("MostRecentTestResult = ? ")
        params.append(form.MostRecentTestResult.data)  
    if not is_empty_form_value(form.EmplWorkLocation.data):
        ands.append("EmplWorkLocation = ? ")
        params.append(form.EmplWorkLocation.data)
    if not is_empty_form_value(form.SSN4.data):
        ands.append("SSN4 = ? ")
        params.append(form.SSN4.data)
    if len(ands) > 0:
        where = "and " + (" and ".join(ands))
    else:
        where = ""
   
    q = ("select SSN4, LastName, FirstName, Sta3n, MostRecentTestDateTime, MostRecentTestResult, PersonType, EmplWorkLocation, MostRecentQuarantineStartDate," +
        "FirstPositiveTestDate, MostRecentAssignedProvider, MostRecentCovidStatus, MostRecentNumOfConsecutiveNegTestSinceLastPos, PersonID " +
        "from {schema}.PersonCombined ".format(schema=app_schema) +
        "where (EmplReturnToWorkDate is null) and " + 
        "((MostRecentQuarantineStartDate is not null)  or (FirstPositiveTestDate is not null)) and " +
        "(PersonType = 'Employee' or PersonType = 'Patient + Employee')  " + where +
        "order by MostRecentTestDateTime desc")
    tb = pd.read_sql(q, conn, params=params)
    

    # Correct NATs
    tb["FirstPositiveTestDate"] = [correct_nats(x) for x in tb["FirstPositiveTestDate"]]
    # Convert NaNs and floats
    tb["Sta3n"] = [correct_nans(y) for y in tb["Sta3n"]]
    # Convert NaNs to None
    tb["MostRecentNumOfConsecutiveNegTestSinceLastPos"] = tb["MostRecentNumOfConsecutiveNegTestSinceLastPos"].replace(np.NaN, "None", regex=True)

    def days_out(quarantine_start_date, first_positive_test_date):
        """ Returns the number of days out of work, based on two values:
            1) Compute the number of days between today's date and the quaratine start date, if it exists
            -- Otherwise --
            2) Compute the number of days between todays's date and the date of 1st positive test, if it exists.
            If neither exists, return None.
        """
        days_out_of_work = None
        today = datetime.date.today()
        if quarantine_start_date is not None:
            days_out_of_work = (today - quarantine_start_date).days
        elif first_positive_test_date is not None:
            fptd = datetime.datetime.strptime(first_positive_test_date, "%Y-%m-%d %H:%M:%S").date()
            days_out_of_work = (today - fptd).days
        return days_out_of_work

    tb["DaysOut"] = [days_out(qsd, fptd) for qsd, fptd in zip(tb["MostRecentQuarantineStartDate"], tb["FirstPositiveTestDate"])]

    return tb

def get_patient_detail(args):
    person_id = args["PersonID"]
      
    pat_detail_person = get_table_by_person_id("PersonCombined", person_id, schema=app_schema, fields="Detail")
    pat_detail_person = pat_detail_person.loc[:,['SSN4','LastName', 'FirstName',
        'DOB', 'DOD', 'Phone', 'Email', 'PersonType']]
      
    pat_detail_admit = get_table_by_person_id("PersonCombined", person_id, schema=app_schema, fields="Detail")  
    pat_detail_admit = pat_detail_admit.loc[:,['AdmitStatus', 'RoomBed', 'WardLocationName',
        'InstitutionName', 'PACT_Provider', 'PACT_Team', 'PACT_Phone',
        'CDWUpdatedDateTime']] 

    pat_detail_symptoms_user = get_table_by_person_id("PersonEntered_MostRecent_Symptom", person_id, schema=app_schema)
    pat_detail_symptoms_user = pat_detail_symptoms_user.loc[:, ["SymptomType", "SymptomOnsetDate", "SymptomOnsetLocationID", "SymptomResolutionDate",
                "SymptomResolutionLocationID", "SymptomNote", "SymptomNumber"]]
  
    result = {}
    result["Patient"] = pat_detail_person
    result["Admit"] = pat_detail_admit
    result["Order_Results"] = get_table_by_person_id("TestCombined", person_id, schema=app_schema)
    result["Symptoms_User"] = pat_detail_symptoms_user
    result["Symptoms_CDW"] = get_table_by_person_id("Symptoms", person_id)
    result["InpatientVisits"] = get_table_by_person_id("InpatientVisits", person_id)
    return result

def get_PersonCombined_row_by_person_id(args):
    person_id = args["PersonID"]
    tb = get_table_by_person_id("PersonCombined", person_id, schema = app_schema)
    assert tb.shape[0] <= 1, "Expected 1 row, but got {} rows".format(tb.shape[0])
    return tb #.iloc[0,:].to_dict()

def get_search_dropdown_choices(var):
    """This function selects the unique choices for column `var` and returns
    them as a list.
    """
    q = ("select distinct {column} as choices ".format(column=var) + 
         "from {schema}.PersonCombined ".format(schema=app_schema) +
         "where (MostRecentTestResult is not null) and "+
         "{column} is not null".format(column=var))
    print(q, file=sys.stderr)
    tb = pd.read_sql(q, engine)
    return np.sort(tb["choices"].unique()).tolist()    

# Contacted and tracked status requests
# =====================================

def get_patient_contacted_status(args):
    """This function returns the current and historical contacted status for
    the patient matching `args["PersonID"]`.
    """
    person_id = args["PersonID"]
    c = get_most_recent_row_by_person_id("Contacted", person_id,
            timestamp="UpdatedDateTime", schema=app_schema)
    h = get_table_by_person_id("Contacted", person_id,
            schema=app_schema).sort_values(by=["UpdatedDateTime"], ascending=False)
    return {"current": c, "historical": h}

def post_patient_contacted_status(args):
    """This function updates the contacted status for the patient matching
    `args["PersonID"]` with the other elements of `args`.
    """
    q = ("insert into {schema}.Contacted ".format(schema=app_schema) +
         "(PersonID, Contacted, Comment, UpdatedBy, UpdatedDateTime) " +
         "values (?, ?, ?, ?, ?)")
    params = [args["PersonID"],
              args["Contacted"],
              args["Comment"],
              get_current_user(),
              get_current_datetime()]
    engine.execute(q, params)
    return None

def get_patient_tracked_status(args):
    """This function returns the current and historical tracked status for
    the patient matching `args["PersonID"]`.
    """
    person_id = args["PersonID"]
    c = get_most_recent_row_by_person_id("Tracked", person_id,
            timestamp="UpdatedDateTime", schema=app_schema)
    h = get_table_by_person_id("Tracked", person_id,
            schema=app_schema)
    return {"current": c, "historical": h}

def post_patient_tracked_status(args):
    """This function updates the tracked status for the patient matching
    `args["PersonID"]` with the other elements of `args`.
    """
    q = ("insert into {schema}.Tracked ".format(schema=app_schema) +
         "(PersonID, Tracked, Comment, UpdatedBy, UpdatedDateTime) " +
         "values (?, ?, ?, ?, ?)")
    params = [args["PersonID"],
              args["Tracked"],
              args["Comment"],
              get_current_user(),
              get_current_datetime()]
    engine.execute(q, params)
    return None


# Summary pages requests
# ======================

def get_summary():
    tb = pd.read_sql_table("Totals_Report", engine, schema=app_schema)
    return tb

# Patient add and edit
# ====================

def get_patient_lookup_results(form):
    """This function selects all persons corresponding to the data in the given
    form object. For each person, we select only the most recently updated
    record.
    """
    args = form.data
    data = {k: v for (k, v) in args.items() if not is_empty_form_value(v)}
    if (not form.validate()) or (len(data) == 0):
        return {"has_form_data": False, "tb": None}
    where = "where " + (" and ".join("(X.[{}] = ?)".format(k) for k, _ in data.items()))
    params = [v for _, v in data.items()]
    q = ("select top 1000 X.* " +
         "from {schema}.PersonCombined X ".format(schema=app_schema) +
         where)
    tb = pd.read_sql(q, engine, params=params)
    return {"has_form_data": True, "tb": tb}

def get_patient_for_editing(args):
    """This function selects the person corresponding to args["PersonID"] from
    PersonCombined for editing, and returns it as a dictionary. This selects
    only the most recently updated record. If no record is found, None is
    returned. We assume that args may come from GET parameters. We also get
    other data needed for this.
    """

    q = ("select coalesce(p.StreetAddress1, StreetAddress2, StreetAddress3) as StreetAddress, p.City, p.County, p.State, p.Zip " +
         "from {schema}.PersonCrosswalk x ".format(schema=app_schema) +
         "left join {schema}.PersonCDW p on p.PersonID = x.PersonID ".format(schema=staging_schema) +
         "where x.PersonID = ?")
    tb = pd.read_sql(q, engine, params=[args["PersonID"]])

    if tb.shape[0] != 1:
        person_cdw_dict = None
    else:
        person_cdw_dict = tb.iloc[0,:].to_dict()

    # Get person information from PersonCombined.
    tb = get_table_by_person_id("PersonCombined", args["PersonID"], schema=app_schema, fields="Edit")
    if tb.shape[0] != 1:
        person_combined_dict = {} # Set to empty dict
    else:
        person_combined_dict = tb.iloc[0,:].to_dict() 

    # Convert Symptomtype entries to be in a list b/c in the form these fields are multi select fields
    # For situations where we selected multiple symptoms, create a list
    symptoms_fields = ["SymptomType" + str(n) for n in list(range(1, 11))]

    if not person_combined_dict: # for newly added patients w/o VISTA data
        for k in symptoms_fields:
            person_combined_dict[k] = [None]
    else:
        for k in symptoms_fields:
            if person_combined_dict.get(k, None) is None: # if they have no existing values
                person_combined_dict[k] = [None] 
            else:
                if person_combined_dict[k].count("; "): # if they have more than one symptom listed
                    person_combined_dict[k] = person_combined_dict[k].split("; ")
                else:
                    person_combined_dict[k] = [person_combined_dict[k]]
    
    # Get test data from CDW/FileMan via TestCombined.
    q = ("select * " +
         "from {schema}.TestCombined ".format(schema=app_schema) +
         "where PersonID = ? and Source in ('CDW', 'FileMan')")
    test_cdw_tb = pd.read_sql(q, engine, params=[args["PersonID"]])
    test_simplified = coalesce_test_results.combine_results(test_cdw_tb)
    
    # Get Contacted Status - just for displaying on edit page
    person_contacted_dict = get_patient_contacted_status(args)
    if person_contacted_dict["current"] is None:
        person_combined_dict["Contacted"] = ""
        person_combined_dict["Comment"] = ""
    else:
        person_combined_dict["Contacted"] = person_contacted_dict["current"]["Contacted"]
        person_combined_dict["Comment"] = person_contacted_dict["current"]["Comment"]

    # Get LastName and SSN from PersonCrosswalk (new Persons are anchored here initially).
    q = ("select PatientLastName, PatientSSN " +
         "from {schema}.PersonCrosswalk ".format(schema=app_schema) +
         "where PersonID = ?")
    pxwalk_tb = pd.read_sql(q, engine, params=[args["PersonID"]])
    pxwalk_dict = pxwalk_tb.iloc[0,:].to_dict()    

    return {"PersonCombined": person_combined_dict,
            "PersonCrosswalk": pxwalk_dict,
            "TestCDW": test_simplified, 
            "HistoricalContact": person_contacted_dict["historical"],
            "PersonCDW": person_cdw_dict}

def add_repeating_group(target_dict, source_dict, repeating_group):
    """
        Uses the repeating group tuple values to move entries from the source_dict to the target_dict.
        Args:
            source_dict: dictionary to pull columns from
            target_dict: dictionary to push columns to
            repeating_group: tuple where 0th element = number of repetitions, 1st element = column name list
        Returns: None
    """
    if source_dict:
        for i in range(1, repeating_group[0] + 1):
            for column in repeating_group[1]:
                column_name = column + str(i)
                target_dict[column_name] = source_dict[column_name]

def post_patient_add(form):
    """This function adds a person based on the info in form.data["PersonID"].
    If a person with those characteristics already exists, an error is raised.
    """
    # Extract data from the form and add updated info.
    LastName = form.LastName.data
    SSN = form.SSN.data
    UpdatedBy = get_current_user()
    UpdatedDateTime = get_current_datetime()

    # Get cursor.
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Insert a new row into the crosswalk if one doesn't already exist. The
    # locks are used to ensure there are no race conditions. Cf
    # https://stackoverflow.com/questions/3407857/only-inserting-a-row-if-its-not-already-there
    q = ("insert into {schema}.PersonCrosswalk ".format(schema=app_schema) +
         "(PersonID, PatientLastName, PatientSSN, UpdatedBy, UpdatedDateTime) " +
         "select newid(), ?, ?, ?, ? " +
         "where " +
         "  not exists " +
         "  (select 0 " +
         "   from {schema}.PersonCrosswalk with (updlock, holdlock) ".format(schema=app_schema) +
         "   where PatientLastName = ? and PatientSSN = ?)")
    params = [LastName, SSN, UpdatedBy, UpdatedDateTime,
              LastName, SSN]
    cursor.execute(q, params)

    # Determine the PersonID for the patient.
    q = ("select PersonID " +
         "from {schema}.PersonCrosswalk ".format(schema=app_schema) +
         "where PatientLastName = ? and PatientSSN = ?")
    params = [LastName, SSN]
    cursor.execute(q, params)
    x = cursor.fetchone()
    print("x", x, file=sys.stderr)
    person_id = x[0]
    cursor.commit()

    return person_id

def post_patient_edit(form):
    """This function updates the person corresponding to form.data["PersonID"]
    with the rest of the form data. It is assumed that the form is already
    validated. We pass in the form object, not the raw POST data, since we are
    using the keys unescaped in the SQL query and that would be dangerous.
    """
    # Extract the data from the form and add extra fields.

    contacted_fields = ["Contacted", "Comment"]
    disabled_fields = ["NextURL"] + [x for x in form.data.keys() if re.search(r"Disabled", x) is not None]
    data = {k: v for (k, v) in form.data.items() if k not in disabled_fields 
            and k not in contacted_fields}
    data["UpdatedBy"] = get_current_user()
    data["UpdatedDateTime"] = get_current_datetime()

    for k in ["SymptomType" + str(n) for n in list(range(1, 11))]:
        if data[k] != []:
            # keep only values that are not "Select..."
            data[k] = [v for v in data[k] if v not in ["Select...", " ", "",]]
            if data[k] != []:
                data[k] = "; ".join(data[k])
            else:
                data[k] = None
        else:
            data[k] = None

    args = form.data
    cs = get_patient_contacted_status(args)
    try:
        current_cs = cs["current"]["Contacted"]
    except:
        current_cs = ""
    try:
        current_comment = cs["current"]["Comment"]
    except:
        current_comment = ""
    cs_user_entered = form.Contacted.data
    cs_comment_user_entered = form.Comment.data
    if current_cs != cs_user_entered or current_comment != cs_comment_user_entered:
        post_patient_contacted_status(args)
     
    # Look up key data that should not be user-changeable. XXX ideally these
    # columns would simply be excluded from PersonEntered
    q = ("select PatientLastName, PatientSSN " +
         "from {schema}.PersonCrosswalk ".format(schema=app_schema) +
         "where PersonID = ?")
    print("person id", form.PersonID.data, file=sys.stderr)
    tb = pd.read_sql(q, engine, params=[form.PersonID.data])
    assert tb.shape[0] == 1, "Expected 1 row, but got {} rows".format(tb.shape[0])
    d = tb.iloc[0,:].to_dict()
    data["LastName"] = d["PatientLastName"]
    data["SSN"] = d["PatientSSN"]

    # Get cursor.
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Define and execute query to insert a new row.
    keys_str = ", ".join(data.keys())
    vals_str = ", ".join("?" for _ in data.keys())
    params = list(data.values())
    q = ("insert into {schema}.PersonEntered ".format(schema=app_schema) +
         "(" + keys_str + ") " +
         "values (" + vals_str + ")")
    cursor.execute(q, params)

    conn.commit()
    
    return None

def get_update_times():
    conn = engine.raw_connection()
    q = ("select 'FileMan' as Source, MostRecentFileMan as UpdateTime " + 
            " from {schema}.MostRecentReportDates ".format(schema=app_schema)+
            " union all "+
            " select 'CDW',MostRecentCDW "+
            " from {schema}.MostRecentReportDates ".format(schema=app_schema)+
            " union all "+
            " select 'User Entered', MostRecentUserEntered from {schema}.MostRecentReportDates".format(schema=app_schema))
    tb_times = pd.read_sql(q, conn)

    return tb_times
