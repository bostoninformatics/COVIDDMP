import pandas as pd
import request_proxy
import connect

engine, staging_schema, app_schema = connect.sql_connect()

def is_authorized_for_csv():
    
     # Get user_id from request proxy
     user_id = request_proxy.get_current_user() 
     
     # Get table of user id and export authorization status
     # Note user id is converted to caps to match case returned by get_current_user()
     authorized_users = pd.read_sql_table("User", engine, schema=app_schema)
     authorized_users['UserID'] = authorized_users['UserID'].str.upper()
     
     # determine if user is authorized
     get_auth_status = authorized_users.loc[authorized_users["UserID"] == user_id,"CSVAuthorized"]
     if get_auth_status.empty: 
         is_authorized = False
     else: 
         is_authorized = (get_auth_status == "Yes").all() 
     return is_authorized