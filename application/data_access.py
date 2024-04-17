import mysql.connector
from datetime import datetime
from flask import request, redirect, url_for, render_template, session
import random


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        # password="password",  # Uncomment and set your password here
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


def log_mood_to_db(child_id, mood_name):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Find the mood_id from the mood table using a safe, parameterized query
            cursor.execute("SELECT mood_id FROM mood WHERE mood_name = %s", (mood_name,))
            mood_id = cursor.fetchone()
            if mood_id:
                # Insert the mood log with the retrieved mood_id
                cursor.execute("INSERT INTO mood_logged (mood_id, child_id, date_logged) VALUES (%s, %s, NOW())", (mood_id['mood_id'], child_id))
                conn.commit()
                return True
        return False
    except Exception as e:
        print(f"Error logging mood: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_logged_moods(child_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT mood_name, mood_image_url, date_logged
            FROM mood_logged
            JOIN mood ON mood_logged.mood_id = mood.mood_id
            WHERE mood_logged.child_id = %s
            ORDER BY date_logged DESC
        """, (child_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching moods: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


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

# def get_random_activity_for_mood(mood_name):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     # Establish a new database connection
#     try:
#         query = """
#         SELECT activity_id, activity_name, activity_image_url, description, instructions
#         FROM activity
#         JOIN mood_and_activity ON activity.activity_id = mood_and_activity.activity_id
#         JOIN mood ON mood_and_activity.mood_id = mood.mood_id
#         WHERE mood.mood_name = %s
#         """
#         cursor.execute(query, (mood_name,))
#
#         activities = cursor.fetchall()
#         if activities:
#             activity = random.choice(activities)
#         else:
#             activity = None
#         return activity
#     except Exception as e:
#         print(f"Error fetching activity: {e}")
#         return None
#
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
