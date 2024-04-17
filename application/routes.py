from flask import Flask, render_template, request, redirect, url_for, session, flash
from application.data_access import (child_login, grownup_login, add_family,
                                     get_child_info_by_family_id, get_grownup_info_by_family_id,
                                     log_mood_to_db, get_logged_moods, send_message, get_messages_for_child,
                                     validate_child_family_association, get_random_activity_for_mood,
                                     get_awarded_badges, log_activity, check_badge_criteria,
                                     get_mood_id_by_mood_logged_id)
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
        grown_up_info = get_grownup_info_by_family_id(family_id)
        messages = get_messages_for_child(child_info['child_id'])
        return render_template('5_child_dashboard.html', child_info=child_info,
                               first_name=first_name, grown_up_info=grown_up_info, messages=messages, family_id=family_id)
    else:
        return redirect(url_for('login_route'))  # Redirect to login page if unauthorized


@app.route('/grownup_dashboard/<int:family_id>')
def grownup_dashboard(family_id):
    # Optional: Verify that the user logged in has access to this family_id
    if 'family_id' in session and session['family_id'] == family_id:
        grownup_info = get_grownup_info_by_family_id(family_id)
        first_name = session.get('first_name')  # Assuming first_name is stored in the session
        child_info = get_child_info_by_family_id(family_id)
        if child_info:
            logged_moods = get_logged_moods(child_info['child_id'])
            last_mood = logged_moods[0] if logged_moods else None
        else:
            last_mood = None
        return render_template('4_grownup_dashboard.html', grown_up_info=grownup_info,
                               first_name=first_name, child_info=child_info, last_mood=last_mood, family_id=family_id)
    else:
        return redirect(url_for('login'))


# activity pages:

@app.route('/sad_page/<int:family_id>')
def sad_page(family_id):
    # Check if the user has the right family_id in their session
    if 'family_id' in session and session['family_id'] == family_id:
        child_id = session.get('child_id')
        if not child_id:
            flash('No child ID found, please log in again.', 'error')
            return redirect(url_for('login_route'))

        # Validate that the child belongs to the correct family
        if not validate_child_family_association(child_id, family_id):
            flash('Access denied. You are not authorized to access this page.', 'error')
            return redirect(url_for('login_route'))

        first_name = session.get('first_name', 'Unknown')  # Provide a default name if not found

        # Log the mood when navigating to the sad page
        # if log_mood_to_db(child_id, 'Sad'):
        #     flash('Mood logged successfully.', 'success')
        # else:
        #     flash('Failed to log mood.', 'error')
        mood_logged_id = log_mood_to_db(child_id, 'Sad')
        print(session)
        if mood_logged_id:
            flash('Mood logged successfully.', 'success')
        # Get a random activity associated with the "Sad" mood
        activity = get_random_activity_for_mood('2')  # Assume '2' is the ID for 'Sad'
        return render_template('6_sad_page.html', first_name=first_name, family_id=family_id,
                               child_id=child_id, activity=activity, mood_logged_id=mood_logged_id)
    else:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('login_route'))

# @app.route('/sad_page/<int:family_id>')
# def sad_page(family_id):
#     if 'family_id' in session and session['family_id'] == family_id:
#         child_id = session.get('child_id')
#         first_name = session.get('first_name')
#         if not child_id:
#             return redirect(url_for('login_route'))
#
#         # Log the mood when navigating to the sad page
#         log_mood_to_db(child_id, 'Sad')  # Log the mood without checking the success
#         # get random activity in activity section
#         activity = get_random_activity_for_mood('2')
#
#         return render_template('6_sad_page.html', first_name=first_name, family_id=family_id,
#                                child_id=child_id, activity=activity)
#     else:
#         return redirect(url_for('login_route'))


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


@app.route('/mood_diary/', defaults={'child_id': None})
@app.route('/mood_diary/<int:child_id>')
def mood_diary(child_id):
    family_id = session.get('family_id')

    if not family_id:
        return redirect(url_for('login_route'))

    # Use the session child_id if no child_id is passed as a parameter (child accessing their own diary)
    if child_id is None:
        child_id = session.get('child_id')

    if not child_id:
        # If there's still no child_id, redirect to login or an error page
        flash("No child specified.", "error")
        return redirect(url_for('grownup_dashboard', family_id=family_id))

    # Validate that the requested child belongs to the logged-in user's family
    if not validate_child_family_association(child_id, family_id):
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('grownup_dashboard', family_id=family_id))

    moods = get_logged_moods(child_id)
    return render_template('10_mood_diary.html', moods=moods, family_id=family_id, child_id=child_id)


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


# badges page and logic:

# @app.route('/log_activity/<int:child_id>/<int:mood_logged_id>', methods=['POST'])
# def log_activity_route(child_id, mood_logged_id):
#     family_id = session.get('family_id')
#
#     if not validate_child_family_association(child_id, family_id):
#         flash('Unauthorized access.', 'error')
#         return redirect(url_for('login_route'))
#
#     # Retrieve mood_id and mood name from mood_logged_id before logging the activity
#     mood_id, mood_name = get_mood_id_and_name_by_mood_logged_id(mood_logged_id)
#     if mood_name is None:
#         flash('Mood not found.', 'error')
#         return redirect(url_for('child_dashboard', family_id=family_id))
#
#     activity_id = request.form.get('activity_id', type=int)
#     journal_text = request.form.get('journal_text') if activity_id == 1 else None
#
#     track_activity_id = log_activity(child_id, mood_logged_id, mood_id, activity_id, journal_text)
#
#     if track_activity_id:
#         check_badge_criteria(child_id, track_activity_id)
#         flash('Activity logged successfully! Check for new badges.')
#     else:
#         flash('Failed to log activity.')
#
#     # Redirect to the specific mood page based on the mood_name
#     return redirect(url_for(f'{mood_name}_page', family_id=family_id))


@app.route('/log_activity/<int:child_id>/<int:mood_logged_id>', methods=['POST'])
def log_activity_route(child_id, mood_logged_id):
    family_id = session.get('family_id')

    if not validate_child_family_association(child_id, family_id):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('login_route'))

    # Retrieve mood_id from mood_logged_id before logging the activity
    mood_id = get_mood_id_by_mood_logged_id(mood_logged_id)
    if mood_id is None:
        flash('Mood not found.', 'error')
        return redirect(url_for('child_dashboard', family_id=family_id))

    # Map mood_id to specific page routes
    mood_page_map = {
        2: 'sad_page',  # Assuming '2' is the ID for 'Sad'
        3: 'angry_page',  # Assuming '3' is the ID for 'Angry'
        4: 'worried_page'  # Assuming '4' is the ID for 'Worried'
    }

    # Check if the activity is a journal entry; assume activity_id = 1 is for journals
    activity_id = request.form.get('activity_id', type=int)
    journal_text = request.form.get('journal_text') if activity_id == 1 else None

    # Log the activity; handle journal text only if it's a journal entry
    track_activity_id = log_activity(child_id, mood_logged_id, mood_id, activity_id, journal_text)

    if track_activity_id:
        # Now pass both child_id and track_activity_id to check_badge_criteria
        check_badge_criteria(child_id, track_activity_id)
        message = 'Activity logged successfully! Check for new badges.'
    else:
        message = 'Failed to log activity.'

    flash(message)

    # Redirect to the specific mood page based on the mood_id
    mood_page_route = mood_page_map.get(mood_id, 'child_dashboard')  # Default to dashboard if mood_id is not mapped
    return redirect(url_for(mood_page_route, family_id=family_id))

# @app.route('/log_activity/<int:child_id>/<int:mood_logged_id>', methods=['POST'])
# def log_activity_route(child_id, mood_logged_id):
#     family_id = session.get('family_id')
#
#     # Check for authorization
#     if not validate_child_family_association(child_id, family_id):
#         flash('Unauthorized access.', 'error')
#         return redirect(url_for('login_route'))
#
#     # Retrieve mood_id from mood_logged_id before logging the activity
#     mood_id = get_mood_id_by_mood_logged_id(mood_logged_id)
#     if mood_id is None:
#         flash('Mood not found.', 'error')
#         return redirect(url_for('child_dashboard', family_id=family_id))
#
#     # Check if the activity is a journal entry; assume activity_id = 1 is for journals
#     activity_id = request.form.get('activity_id', type=int)
#     journal_text = request.form.get('journal_text') if activity_id == 1 else None
#
#     # Log the activity; handle journal text only if it's a journal entry
#     track_activity_id = log_activity(child_id, mood_logged_id, mood_id, activity_id, journal_text)
#
#     if track_activity_id:
#         # Now pass both child_id and track_activity_id to check_badge_criteria
#         check_badge_criteria(child_id, track_activity_id)
#         message = 'You have a new badge!'
#     else:
#         message = 'Failed to log activity.'
#
#     flash(message)
#     return redirect(url_for('mood_page', family_id=family_id, mood=mood_id))


@app.route('/badges_page/<int:child_id>')
def badges_page(child_id):
    # Retrieve family_id from session
    family_id = session.get('family_id')

    # First, check if the family_id exists in the session
    if not family_id:
        flash("Unauthorized access or missing family information.", "error")
        return redirect(url_for('login_route'))

    # Validate that the requested child belongs to the logged-in user's family
    if not validate_child_family_association(child_id, family_id):
        flash('You do not have permission to view this page.', "error")
        return redirect(url_for('grownup_dashboard', family_id=family_id))

    # If everything is valid, retrieve and display the badges
    badges = get_awarded_badges(child_id)
    return render_template('11_badges_page.html', badges=badges, child_id=child_id, family_id=family_id)