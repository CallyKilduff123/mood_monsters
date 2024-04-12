from flask import Flask, render_template, request, redirect, url_for, session
from application.data_access import child_login, grownup_login
from datetime import datetime, timedelta
from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        if request.form.get('login_type') == 'grownup':
            return grownup_login()
        elif request.form.get('login_type') == 'child':
            return child_login()
    return render_template('2_login.html', title='Login')

@app.route('/register')
def register():
    return render_template('3_register.html', title='Register')


@app.route('/grownup_dashboard')
def grownup_dashboard():
    return render_template('4_grownup_dashboard.html', title='Dashboard')

@app.route('/child_dashboard')
def child_dashboard():
    return render_template('5_child_dashboard.html', title='Dashboard')
