import mysql.connector
from datetime import datetime
from flask import request, redirect, url_for, render_template, session
import random


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        #password="password",  # Uncomment and set your password here
        database="mood_monsters"
    )


# Common function to get cursor with dictionary results
# def get_cursor(conn):
#     return conn.cursor(dictionary=True)
def get_cursor(conn):
    return conn.cursor(dictionary=True, buffered=True)


# Function for adding family, grown up, and child data into the database
def add_family(adult_info, child_info, shared_pin):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("INSERT INTO family (shared_pin) VALUES (%s)", (shared_pin,))
        family_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO grown_up (family_id, first_name, last_name, username, email, relationship_to_child)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (family_id, adult_info['first_name'], adult_info['last_name'], adult_info['username'], adult_info['email'],
              adult_info['relationship']))

        cursor.execute("""
            INSERT INTO child (family_id, first_name, last_name, username, date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
        """, (family_id, child_info['first_name'], child_info['last_name'], child_info['username'], child_info['dob']))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


# Login function for grownup with security measures
def grownup_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        conn = get_db_connection()
        cursor = get_cursor(conn)
        try:
            sql = """
                SELECT grown_up.*, family.shared_pin FROM grown_up
                JOIN family ON grown_up.family_id = family.family_id
                WHERE grown_up.username = %s AND family.shared_pin = %s;
                """
            val = (username, pin)
            cursor.execute(sql, val)
            grown_up = cursor.fetchone()

            if grown_up:
                session['username'] = username
                session['user_type'] = 'grownup'
                session['family_id'] = grown_up['family_id']
                session['first_name'] = grown_up['first_name']
                return redirect(url_for('grownup_dashboard', family_id=grown_up['family_id']))
            else:
                return render_template('2_login.html', title='Login', show_error_grownup=True, show_error_child=False)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=False)


# Fetch grownup info based on family ID
def get_grownup_info_by_family_id(family_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Make sure to use dictionary cursor
    try:
        cursor.execute("SELECT * FROM grown_up WHERE family_id = %s", (family_id,))
        result = cursor.fetchone()
        cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()


# Child login function with improved error handling and redirection

def child_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        conn = get_db_connection()
        cursor = get_cursor(conn)
        try:
            sql = """
                    SELECT child.*, family.shared_pin FROM child
                    JOIN family ON child.family_id = family.family_id
                    WHERE child.username = %s AND family.shared_pin = %s;
                    """
            val = (username, pin)
            cursor.execute(sql, val)
            child = cursor.fetchone()
            cursor.fetchall()  # Ensure all results are fetched and cursor is cleared
            if child:
                session['username'] = username
                session['user_type'] = 'child'
                session['family_id'] = child['family_id']
                session['child_id'] = child['child_id']
                session['first_name'] = child['first_name']
                return redirect(url_for('child_dashboard', family_id=child['family_id']))
            else:
                return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=True)
        finally:
            cursor.close()
            conn.close()


def get_child_info_by_family_id(family_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM child WHERE family_id = %s", (family_id,))
        result = cursor.fetchone()
        cursor.fetchall()  # Ensure any additional results are fetched to clear the cursor
        return result
    finally:
        cursor.close()
        conn.close()


# LETICIA NEW LOGIC
def log_mood_to_db(child_id, mood_name):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch the mood_id from the database
            cursor.execute("SELECT mood_id FROM mood WHERE mood_name = %s", (mood_name,))
            result = cursor.fetchone()
            if not result:
                print(f"Mood name '{mood_name}' not found in database.")
                return None  # Mood name not found in database

            mood_id = result['mood_id']

            # Log the mood
            cursor.execute("INSERT INTO mood_logged (mood_id, child_id, date_logged) VALUES (%s, %s, NOW())",
                           (mood_id, child_id))
            conn.commit()
            print(f"Mood logged successfully: {mood_id}")
            return mood_id
    except Exception as e:
        print(f"Error logging mood: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


# CALLY CODE
# only shows one mood per date in the mood diary:

def get_logged_moods(child_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT mood_name, mood_image_url, date_logged
            FROM (
                SELECT mood.mood_name, mood.mood_image_url, mood_logged.date_logged,
                    ROW_NUMBER() OVER (PARTITION BY DATE(mood_logged.date_logged) ORDER BY mood_logged.date_logged DESC) AS row_num
                FROM mood_logged
                JOIN mood ON mood_logged.mood_id = mood.mood_id
                WHERE mood_logged.child_id = %s
                ORDER BY mood_logged.date_logged DESC
            ) AS subquery
            WHERE row_num = 1
            ORDER BY date_logged DESC
            LIMIT 24;
        """, (child_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching moods: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# shows all moods logged - including with activities:
# def get_logged_moods(child_id):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     try:
#         cursor.execute("""
#             SELECT mood_name, mood_image_url, date_logged
#             FROM mood_logged
#             JOIN mood ON mood_logged.mood_id = mood.mood_id
#             WHERE mood_logged.child_id = %s
#             ORDER BY date_logged DESC
#             LIMIT 24
#         """, (child_id,))
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching moods: {e}")
#         return None
#     finally:
#         cursor.close()
#         conn.close()


def validate_child_family_association(child_id, family_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM child
                WHERE child_id = %s AND family_id = %s
            """, (child_id, family_id))
            result = cursor.fetchone()
            return bool(result)
    except Exception as e:
        print(f"Error validating family association: {e}")
        return False
    finally:
        conn.close()


def send_message(grown_up_id, child_id, message):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Verify if both grown-up and child belong to the same family before sending a message
            verify_sql = """
                SELECT 1 FROM grown_up
                JOIN child ON grown_up.family_id = child.family_id
                WHERE grown_up.grown_up_id = %s AND child.child_id = %s
            """
            cursor.execute(verify_sql, (grown_up_id, child_id))
            if cursor.fetchone() is None:
                print("Error: Grown-up and child do not belong to the same family.")
                return False

            # Proceed with inserting the message if verification is successful
            sql = """
                INSERT INTO message (child_id, grown_up_id, message, date_sent)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(sql, (child_id, grown_up_id, message))
            conn.commit()
            return True

    except Exception as e:
        print("Error during sending message:", e)
        conn.rollback()
        return False

    finally:
        conn.close()


def get_messages_for_child(child_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
            SELECT message.message, message.date_sent, grown_up.first_name AS from_name
            FROM message
            JOIN grown_up ON message.grown_up_id = grown_up.grown_up_id
            WHERE message.child_id = %s
            ORDER BY message.date_sent DESC
            LIMIT 1
        """
        cursor.execute(sql, (child_id,))
        messages = cursor.fetchall()
        return messages
    finally:
        cursor.close()
        conn.close()


def get_notifications_for_child(child_id):
    conn = get_db_connection()
    notifications = None
    try:

        with conn.cursor(dictionary=True) as cursor:  # Use dictionary=True to fetch rows as dictionaries
            cursor.execute("""SELECT notification_id, message_id, date_logged, is_read 
                              FROM notifications WHERE child_id = %s""", (child_id,))
            notifications = cursor.fetchall()
    except Exception as e:
        print(f"Error while fetching notifications: {e}")
    finally:
        if conn:
            conn.close()
    return notifications


def create_notification(child_id, message_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO notifications (child_id, message_id, date_logged, is_read) 
                              VALUES (%s, %s, NOW(), FALSE)
                              """, (child_id, message_id))
            conn.commit()
    except Exception as e:
        print(f"Error while creating notification: {e}")
    finally:
        if conn:
            conn.close()


def mark_notification_as_read(notification_id):
    # Function to mark a notification as read
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""UPDATE notifications SET is_read = TRUE WHERE notification_id = %s""",
                           (notification_id,))
            conn.commit()
            print("Notification marked as true")
    except Exception as e:
        # Handle exceptions, log errors, etc.
        print(f"Error while marking notification as read: {e}")
    finally:
        if conn:
            conn.close()


def get_random_activity_for_mood(mood_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Query to get all activity_ids associated with the mood_id
        query = """
        SELECT activity_id
        FROM mood_and_activity
        WHERE mood_id = %s
        """
        cursor.execute(query, (mood_id,))
        activity_ids = cursor.fetchall()

        # Randomly select one activity_id from the list
        if activity_ids:
            selected_activity_id = random.choice(activity_ids)['activity_id']

            # Fetch the details of the selected activity
            activity_query = """
            SELECT activity_id, activity_name, activity_image_url, description, instructions
            FROM activity
            WHERE activity_id = %s
            """
            cursor.execute(activity_query, (selected_activity_id,))
            activity = cursor.fetchone()
            return activity
        else:
            return None
    except Exception as e:
        print(f"Error fetching activity: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# testing badge logic:
def log_activity(child_id, mood_id, activity_id, journal_text=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO track_activity (child_id, mood_id, activity_id, journal_text, date_completed)
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(sql, (child_id, mood_id, activity_id, journal_text))
            conn.commit()
            return cursor.lastrowid  # Returns the ID of the newly inserted row
    except Exception as e:
        print("Error logging activity:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


# def log_activity(child_id, mood_logged_id, mood_id, activity_id, journal_text=None):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             # Updated SQL query to include mood_id
#             sql = """
#             INSERT INTO track_activity (child_id, mood_logged_id, mood_id, activity_id, journal_text, date_completed)
#             VALUES (%s, %s, %s, %s, %s, NOW())
#             """
#             cursor.execute(sql, (child_id, mood_logged_id, mood_id, activity_id, journal_text))
#             conn.commit()
#             return cursor.lastrowid  # Returns the ID of the newly inserted row
#     except mysql.connector.Error as e:
#         print("Error logging activity:", e)
#         return None
#     finally:
#         cursor.close()
#         conn.close()


# def get_mood_id_and_name_by_mood_logged_id(mood_logged_id):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT mood_id, mood_name FROM mood_logged JOIN mood ON mood.mood_id = mood_logged.mood_id WHERE mood_logged_id = %s", (mood_logged_id,))
#             result = cursor.fetchone()
#             return result['mood_id'], result['mood_name'] if result else (None, None)
#     except mysql.connector.Error as e:
#         print("Database error while fetching mood_id and name:", e)
#         return None, None
#     finally:
#         cursor.close()
#         conn.close()

# change to get mood name by logged mood
# join mood and mood logged tables - return mood name
# pass new variable into the log activity app route so that the mood is fetched by name
# so that when you return a mood-specific page, you do not log that mood to the database
def get_mood_id_by_mood_logged_id(mood_logged_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT mood_id FROM mood_logged WHERE mood_logged_id = %s", (mood_logged_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except mysql.connector.Error as e:
        print("Database error while fetching mood_id:", e)
        return None
    finally:
        cursor.close()
        conn.close()


# ADDED FOR AN ERROR - LETICIA
def check_badge_criteria(child_id):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # retrieves information about badge criteria and completed activities for a given child.
            # It counts the completed activities associated with each badge and checks if the count meets the required criteria for awarding the badge.
            # The LEFT JOIN with the track_activity table ensures that all badge criteria are considered,
            # even if there are no matching completed activities.
            sql = """
               SELECT 
                    bc.badge_id, 
                    b.badge_name, 
                    COUNT(bc.criteria_id) AS required_count,
                    COUNT(DISTINCT ta.track_activity_id) AS completed_count,
                    MAX(CASE WHEN ta.activity_id = bc.activity_id AND ta.mood_id = bc.mood_id THEN ta.track_activity_id END) AS track_activity_id
                FROM 
                    badge_criteria bc
                JOIN 
                    badge b ON bc.badge_id = b.badge_id
                LEFT JOIN 
                    track_activity ta ON (ta.activity_id = bc.activity_id OR ta.mood_id = bc.mood_id) AND ta.child_id = %s
                GROUP BY 
                    bc.badge_id
                HAVING 
                    completed_count >= required_count

            """
            cursor.execute(sql, (child_id,))
            eligible_badges = cursor.fetchall()

            # Logging
            # Logging
            print("Eligible Badges:")
            for badge in eligible_badges:
                print(f"Badge ID: {badge['badge_id']}, Badge Name: {badge['badge_name']}")
                print(f"Required Count: {badge['required_count']}, Completed Count: {badge['completed_count']}")

            # Award badges
            for badge in eligible_badges:
                track_activity_id = badge.get('track_activity_id')
                if track_activity_id:
                    badge_updated = update_badge_awarded(child_id, badge['badge_id'], track_activity_id)
                    if badge_updated:
                        badge_recently_added = True  # Set the variable to True if update is successful
                    else:
                        badge_recently_added = False
                        print(f"Failed to update badge progress for Badge ID: {badge['badge_id']}")
                else:
                    print(f"No matching activity found for Badge ID: {badge['badge_id']}")

                return eligible_badges, badge_recently_added
    except Exception as e:
        print(f"Error checking badge criteria for Child {child_id}: {e}")
        return None
    finally:
        conn.close()  # Close the connection, as cursor will be closed by 'with' statement


# LETICIA - NEW CODE UPDATED
def update_badge_awarded(child_id, badge_id, track_activity_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Ensure the badge has not been previously awarded
            check_awarded_sql = """
            SELECT 1 FROM badge_progress
            WHERE child_id = %s AND badge_id = %s AND award_badge = TRUE
            """
            cursor.execute(check_awarded_sql, (child_id, badge_id))
            if cursor.fetchone():
                print(f"Badge already awarded. Child ID: {child_id}, Badge ID: {badge_id}")
                return False  # Badge already awarded, so return False

            # Award the badge
            insert_sql = """
            INSERT INTO badge_progress (child_id, badge_id, track_activity_id, award_badge, date_completed)
            VALUES (%s, %s, %s, TRUE, NOW())
            """
            cursor.execute(insert_sql, (child_id, badge_id, track_activity_id))
            conn.commit()
            print(f"Badge awarded successfully. Child ID: {child_id}, Badge ID: {badge_id}")
            return True  # Badge successfully awarded, so return True
    except Exception as e:
        print(f"Error updating badge progress: {e}")
        conn.rollback()
        return False  # Return False in case of any error
    finally:
        cursor.close()
        conn.close()



# CALLY CODE
# def update_badge_awarded(child_id, badge_id):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             # Ensure the badge has not been previously awarded
#             check_awarded_sql = """
#             SELECT 1 FROM badge_progress
#             WHERE child_id = %s AND badge_id = %s AND award_badge = TRUE
#             """
#             cursor.execute(check_awarded_sql, (child_id, badge_id))
#             if cursor.fetchone():
#                 print(f"Badge already awarded. Child ID: {child_id}, Badge ID: {badge_id}")
#                 return
#
#             # Award the badge
#             insert_sql = """
#             INSERT INTO badge_progress (child_id, badge_id, award_badge, date_completed)
#             VALUES (%s, %s, TRUE, NOW())
#             """
#             cursor.execute(insert_sql, (child_id, badge_id))
#             conn.commit()
#             print(f"Badge awarded successfully. Child ID: {child_id}, Badge ID: {badge_id}")
#     except Exception as e:
#         print(f"Error updating badge progress: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()


# def update_badge_awarded(child_id, badge_id, track_activity_id):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             # Check if an entry exists in the badge_progress table for the given child and badge
#             check_sql = """
#             SELECT badge_progress_id FROM badge_progress
#             WHERE child_id = %s AND badge_id = %s
#             """
#             cursor.execute(check_sql, (child_id, badge_id))
#             existing_entry = cursor.fetchone()
#
#             if existing_entry:
#                 # Update the existing entry to mark the badge as awarded
#                 update_sql = """
#                 UPDATE badge_progress
#                 SET award_badge = TRUE, date_completed = NOW()
#                 WHERE badge_progress_id = %s
#                 """
#                 cursor.execute(update_sql, (existing_entry[0],))
#             else:
#                 # Insert a new entry in the badge_progress table
#                 insert_sql = """
#                 INSERT INTO badge_progress (child_id, badge_id, track_activity_id, award_badge, date_completed)
#                 VALUES (%s, %s, %s, TRUE, NOW())
#                 """
#                 cursor.execute(insert_sql, (child_id, badge_id, track_activity_id))
#
#             conn.commit()
#     except mysql.connector.Error as e:
#         print(f"Error updating badge progress: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()


def get_awarded_badges(child_id):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
            SELECT badge.badge_id, badge.badge_name, badge.badge_image_url, badge.badge_description
            FROM badge_progress
            JOIN badge ON badge_progress.badge_id = badge.badge_id
            WHERE badge_progress.child_id = %s AND badge_progress.award_badge = TRUE
            """
            cursor.execute(sql, (child_id,))
            badges = cursor.fetchall()
            return badges
    finally:
        cursor.close()
        conn.close()
