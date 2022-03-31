"""

In development you could start me directly 
with "FLASK_APP=start_webhooks flask run -p 9443"
or use the vscode debugger!! (See launch.json)

"""
from app import app
import waitress

# This is only for production mode,
# in development we always run in flask.
if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=9443, threads=16)
