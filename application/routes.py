from flask import Flask, render_template, request, redirect, url_for, session, flash
from application.data_access import (child_login, grownup_login, add_family,
                                     get_child_info_by_family_id, get_grownup_info_by_family_id,
                                     log_mood_to_db, get_logged_moods)
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


@app.route('/logout')
def logout():
    session.clear() # Clear the session, removing stored user information
    return redirect(url_for('home'))  # Redirect to home page


# dashboards
@app.route('/child_dashboard/<int:family_id>')
def child_dashboard(family_id):
    # Verify the family_id stored in session to prevent unauthorized access
    if 'family_id' in session and session['family_id'] == family_id:
        # Fetch child and related family information using family_id
        child_info = get_child_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Default to 'Unknown' if not set
        return render_template('5_child_dashboard.html', child_info=child_info, first_name=first_name, family_id=family_id)
    else:
        return redirect(url_for('login'))  # Redirect to login page if unauthorized


@app.route('/grownup_dashboard/<int:family_id>')
def grownup_dashboard(family_id):
    # Optional: Verify that the user logged in has access to this family_id
    if 'family_id' in session and session['family_id'] == family_id:
        grownup_info = get_grownup_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Assuming first_name is stored in the session
        return render_template('4_grownup_dashboard.html', grown_up_info=grownup_info, first_name=first_name, family_id=family_id)
    else:
        return redirect(url_for('login'))

# activity pages:
# @app.route('/sad_page/<int:family_id>')
# def sad_page(family_id):
#     # You can now use family_id within this function to fetch specific data, perform checks, etc.
#     # Fetch child and related family information using family_id
#     first_name = session.get('first_name')  # Default to 'Unknown' if not set
#     return render_template('6_sad_page.html', first_name=first_name, family_id=family_id)
#
#
# @app.route('/worried_page/<int:family_id>')
# def worried_page(family_id):
#     return render_template('8_worried_page.html', family_id=family_id)
#
#
# @app.route('/angry_page/<int:family_id>')
# def angry_page(family_id):
#     return render_template('7_angry_page.html', family_id=family_id)


# cally - testing logging mood to mood diary

@app.route('/sad_page/<int:family_id>')
def sad_page(family_id):
    if 'family_id' in session and session['family_id'] == family_id:
        child_id = session.get('child_id')
        if not child_id:
            return redirect(url_for('login_route'))

        # Log the mood when navigating to the sad page
        log_mood_to_db(child_id, 'Sad')  # Log the mood without checking the success
        return render_template('6_sad_page.html', family_id=family_id)
    else:
        return redirect(url_for('login_route'))


@app.route('/angry_page/<int:family_id>')
def angry_page(family_id):
    if 'family_id' in session and session['family_id'] == family_id:
        child_id = session.get('child_id')
        if not child_id:
            return redirect(url_for('login_route'))

        # Log the mood when navigating to the sad page
        log_mood_to_db(child_id, 'Angry')  # Log the mood without checking the success
        return render_template('7_angry_page.html', family_id=family_id)
    else:
        return redirect(url_for('login_route'))

# @app.route('/angry_page/<int:family_id>')
# def angry_page(family_id):
#     if 'family_id' in session and session['family_id'] == family_id:
#         return render_template('7_angry_page.html', family_id=family_id)
#     else:
#         return redirect(url_for('login_route'))


@app.route('/worried_page/<int:family_id>')
def worried_page(family_id):
    if 'family_id' in session and session['family_id'] == family_id:
        child_id = session.get('child_id')
        if not child_id:
            return redirect(url_for('login_route'))

        # Log the mood when navigating to the sad page
        log_mood_to_db(child_id, 'Worried')  # Log the mood without checking the success
        return render_template('8_worried_page.html', family_id=family_id)
    else:
        return redirect(url_for('login_route'))

# @app.route('/worried_page/<int:family_id>')
# def worried_page(family_id):
#     if 'family_id' in session and session['family_id'] == family_id:
#         return render_template('8_worried_page.html', family_id=family_id)
#     else:
#         return redirect(url_for('login_route'))


@app.route('/mood_diary/<int:family_id>')
def mood_diary(family_id):
    if 'family_id' in session and session['family_id'] == family_id:
        child_id = session.get('child_id')
        if not child_id:
            return redirect(url_for('login'))

        moods = get_logged_moods(child_id)
        return render_template('10_mood_diary.html', moods=moods, family_id=family_id)
    else:
        return redirect(url_for('login'))


@app.route('/printable-journal/<int:family_id>')
def printable_journal(family_id):
    return render_template('9_printable_journal_page.html', family_id=family_id)
