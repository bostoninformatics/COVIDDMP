import os
import sys

sys.path.insert(0, 'D:/Projects/COVID19/covid_app_virtualenv/Lib/site-packages')
sys.path.insert(0, 'D:/Projects/COVID19/Live_COVID19trackingapp/Dashboard/web')

os.environ["COVID_APP_IS_LIVE"] = "Yes"

from app import app as application
