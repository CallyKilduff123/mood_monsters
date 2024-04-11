from flask import url_for, render_template, request, redirect, session
from datetime import datetime, timedelta


from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home')
