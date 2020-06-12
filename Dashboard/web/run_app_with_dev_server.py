import sys

if len(sys.argv) != 2:
    print("Usage: %s PORT" % sys.argv[0])
    sys.exit(1)
port = int(sys.argv[1])

sys.path.insert(0, 'X:/COVID19/covid_app_virtualenv/Lib/site-packages')
sys.path.insert(0, '.')

from app import app as application

application.run(host="127.0.0.1", port=port, debug=True)
