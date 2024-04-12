import mysql.connector
from datetime import datetime
from flask import request, redirect, url_for, render_template, session


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mood_monsters"
    )
    return mydb


# registering family
def add_family(adult_info, child_info, shared_pin):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO family (shared_pin) VALUES (%s)", (shared_pin,))
        family_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO grown_up (family_id, first_name, last_name, email, relationship_to_child)
            VALUES (%s, %s, %s, %s, %s)
        """, (family_id, adult_info['first_name'], adult_info['last_name'], adult_info['email'], adult_info['relationship']))

        cursor.execute("""
            INSERT INTO child (family_id, first_name, last_name, date_of_birth)
            VALUES (%s, %s, %s, %s)
        """, (family_id, child_info['first_name'], child_info['last_name'], child_info['dob']))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def grownup_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM Person WHERE Username = %s AND PIN = %s AND Type = '2'"  # Check if grown-up
        val = (username, pin)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        if person:
            session['username'] = username  # Store username in session
            session['user_type'] = 'grownup'
            return redirect(url_for('grownup_dashboard'))  # Redirect to grown-up dashboard
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('2_login.html', title='Login', show_error_grownup=True, show_error_child=False)
    else:
        return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=False)


def child_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM Person WHERE Username = %s AND PIN = %s AND Type = '1'"
        val = (username, pin)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        if person:
            session['username'] = username  # Store username in session
            session['user_type'] = 'child'
            return redirect(url_for('child_dashboard'))  # Redirect to child dashboard
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=True)
    else:
        return render_template('2_login.html', title='Login', show_error_grownup=False, show_error_child=False)



