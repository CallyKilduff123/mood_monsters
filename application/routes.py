from flask import Flask, render_template, request, redirect, url_for, session
from application.data_access import child_login, grownup_login, add_family
from datetime import datetime, timedelta
from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        adult_info = {
            'first_name': request.form['adult_first_name'],
            'last_name': request.form['adult_last_name'],
            'email': request.form['adult_email'],
            'relationship': request.form['relationship']
        }
        child_info = {
            'first_name': request.form['child_first_name'],
            'last_name': request.form['child_last_name'],
            'dob': request.form['child_dob']
        }
        shared_pin = request.form['shared_pin']

        # Call the correct data access function
        success = add_family(adult_info, child_info, shared_pin)
        if success:
            return redirect(url_for('login_route'))
        else:
            return 'Registration Failed', 500

    return render_template('3_register.html', title='Register')



@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        if request.form.get('login_type') == 'grownup':
            return grownup_login()
        elif request.form.get('login_type') == 'child':
            return child_login()
    return render_template('2_login.html', title='Login')


@app.route('/grownup_dashboard')
def grownup_dashboard():
    return render_template('4_grownup_dashboard.html', title='Dashboard')


@app.route('/child_dashboard')
def child_dashboard():
    return render_template('5_child_dashboard.html', title='Dashboard')
