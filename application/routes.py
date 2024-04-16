from flask import Flask, render_template, request, redirect, url_for, session, flash

from application.data_access import (child_login, grownup_login, add_family,
                                                   get_child_info_by_family_id, get_grownup_info_by_family_id,
                                                   log_mood_to_db, get_logged_moods, send_message,
                                                   get_messages_for_child,
    # ADDED FUNCTIONS FOR BADGES FROM DATA.ACCESS
                                                   get_activity_id_by_name, is_first_activity_for_mood,
                                                   log_activity_and_mood,
                                                   award_badge, get_earned_badges)
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
    session.clear()  # Clear the session, removing stored user information
    return redirect(url_for('home'))  # Redirect to home page


# dashboards
@app.route('/child_dashboard/<int:family_id>')
def child_dashboard(family_id):
    # Verify the family_id stored in session to prevent unauthorized access
    if 'family_id' in session and session['family_id'] == family_id:
        # Fetch child and related family information using family_id
        child_info = get_child_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Default to 'Unknown' if not set
        grown_up_info = get_grownup_info_by_family_id(family_id)
        messages = get_messages_for_child(child_info['child_id'])
        return render_template('5_child_dashboard.html', child_info=child_info,
                               first_name=first_name, grown_up_info=grown_up_info, messages=messages,
                               family_id=family_id)
    else:
        return redirect(url_for('login'))  # Redirect to login page if unauthorized


@app.route('/grownup_dashboard/<int:family_id>')
def grownup_dashboard(family_id):
    # Optional: Verify that the user logged in has access to this family_id
    if 'family_id' in session and session['family_id'] == family_id:
        grownup_info = get_grownup_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Assuming first_name is stored in the session
        child_info = get_child_info_by_family_id(family_id)
        return render_template('4_grownup_dashboard.html', grown_up_info=grownup_info, first_name=first_name,
                               child_info=child_info, family_id=family_id)
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
        first_name = session.get('first_name')
        if not child_id:
            return redirect(url_for('login_route'))

        # Log the mood when navigating to the sad page
        log_mood_to_db(child_id, 'Sad')  # Log the mood without checking the success
        return render_template('6_sad_page.html', first_name=first_name, family_id=family_id)
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


@app.route('/send_message', methods=['POST'])
def send_message_route():
    if 'family_id' not in session:
        return redirect(url_for('login'))

    child_id = request.form['child_id']
    grown_up_id = request.form['grown_up_id']
    message = request.form['message']

    # Assuming send_message is imported correctly and working
    if send_message(child_id, grown_up_id, message):
        # Assume a flash method or similar feedback mechanism
        flash("Message sent successfully!", "success")
    else:
        flash("Failed to send message. Please try again.", "error")

    return redirect(url_for('grownup_dashboard', family_id=session['family_id']))


# TODO: LETICIA TEST AND FIND HOW TO GET IT WORKING
# TODO: NEED TO ADD OTHER ACTIVITIES RELATED TO MOOD
@app.route('/submit_journal', methods=['POST'])
def submit_journal():
    # checks if the family_id and child_id are present in the session
    if 'family_id' not in session or 'child_id' not in session:
        return redirect(url_for('login'))

    # retrieves the child_id, mood_id and journal_entry from the session
    # todo - consider changing it to activity_id (have to think and ask questions around this one)
    child_id = session['child_id']
    mood_id = request.form['mood_id']
    # TODO:
    journal_entry = request.form['journal_entry']

    # It calls the get_activity_id_by_name function from the data_access module to get the activity_id for the "Journal Entry" activity.
    # Get the activity_id for 'Journal Entry'
    activity_id = get_activity_id_by_name('Journal Entry')  # Implement this function in data_access

    # Log the activity and mood
    if log_activity_and_mood(child_id, activity_id, mood_id):
        # Check if it's the first journal entry for this mood
        is_first_entry = is_first_activity_for_mood(child_id, activity_id,
                                                    mood_id)  # Implement this function in data_access

        if is_first_entry:
            # Award the corresponding badge
            award_badge(child_id, activity_id, mood_id)

        # todo: Save the journal entry to the database (code for this step not shown)

        return redirect(url_for('achievements', child_id=child_id))
    else:
        # Handle error
        flash("Error logging activity and mood", "error")
        return redirect(url_for('child_dashboard', family_id=session['family_id']))


# Add a new route for the achievements page
@app.route('/achievements/<int:child_id>')
def achievements(child_id):
    if 'family_id' not in session or 'child_id' not in session or session['child_id'] != child_id:
        return redirect(url_for('login'))

    earned_badges = get_earned_badges(child_id)  # Implement this function in data_access
    return render_template('achievements.html', earned_badges=earned_badges)


@app.route('/add_badge/<mood>')
def add_badge(mood):
    return redirect(url_for('badges_page', family_id=session['family_id']))