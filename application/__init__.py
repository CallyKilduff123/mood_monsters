from flask import Flask

app = Flask(__name__)
# have to set a secret key for application for session to work,
# secret key is required for securely signing the session data.
app.secret_key = 's3cr3t'

from application import routes
