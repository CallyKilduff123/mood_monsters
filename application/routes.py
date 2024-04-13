from flask import Flask, render_template, request, redirect, url_for, session
from application.data_access import child_login, grownup_login, add_family, get_child_info_by_family_id, get_grownup_info_by_family_id
from datetime import datetime, timedelta
from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home', body_class="pink-body")


# registration app route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        adult_info = {
            'first_name': request.form['adult_first_name'],
            'last_name': request.form['adult_last_name'],
            'username': request.form['adult_username'],
            'email': request.form['adult_email'],
            'relationship': request.form['relationship']
        }
        child_info = {
            'first_name': request.form['child_first_name'],
            'last_name': request.form['child_last_name'],
            'username': request.form['child_username'],
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


# login app route
# @app.route('/login', methods=['GET', 'POST'])
# def login_route():
#     if request.method == 'POST':
#         if request.form.get('login_type') == 'grownup':
#             return grownup_login()
#         elif request.form.get('login_type') == 'child':
#             return child_login()
#     return render_template('2_login.html', title='Login')
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        print("Login type:", login_type)  # Debugging output

        if login_type == 'grownup':
            return grownup_login()
        elif login_type == 'child':
            return child_login()
    return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=False)

# @app.route('/grownup_dashboard')
# def grownup_dashboard():
#     return render_template('4_grownup_dashboard.html', title='Dashboard')
#

# @app.route('/child_dashboard/<int:family_id>')
# def child_dashboard(family_id):
#     return render_template('5_child_dashboard.html', title='Dashboard')


# dashboards
@app.route('/child_dashboard/<int:family_id>')
def child_dashboard(family_id):
    # Verify the family_id stored in session to prevent unauthorized access
    if 'family_id' in session and session['family_id'] == family_id:
        # Fetch child and related family information using family_id
        child_info = get_child_info_by_family_id(family_id)
        first_name = session.get('first_name', 'Unknown')  # Default to 'Unknown' if not set
        return render_template('5_child_dashboard.html', child_info=child_info, first_name=first_name, family_id=family_id)
    else:
        return redirect(url_for('login'))  # Redirect to login page if unauthorized


@app.route('/grownup_dashboard/<int:family_id>')
def grownup_dashboard(family_id):
    # Optional: Verify that the user logged in has access to this family_id
    if 'family_id' in session and session['family_id'] == family_id:
        grownup_info = get_grownup_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Assuming first_name is stored in the session
        return render_template('4_grownup_dashboard.html', first_name=first_name, family_id=family_id)
    else:
        return redirect(url_for('login'))  # or redirect to login


@app.route('/sad_page')
def sad_page():
    return render_template('6_sad_page.html')