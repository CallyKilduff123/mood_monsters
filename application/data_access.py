import mysql.connector
from flask import request, redirect, url_for, render_template


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="",
        database="mood_monsters"
    )
    return mydb


def grownup_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        print("Username:", username)
        print("PIN:", pin)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM Person WHERE Username = %s AND PIN = %s AND Type = '2'"  # Check if grown-up
        val = (username, pin)
        print("SQL query:", sql)
        print("Values:", val)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        print("Person:", person)
        if person:
            return redirect(url_for('grownup_dashboard'))  # Redirect to grown-up dashboard
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('2_login.html', title='Login', show_error_grownup= True, show_error_child=False)
    else:
        return render_template('2_login.html', title='Login', show_error_grownup= False, show_error_child=False)


def child_login():
    if request.method == 'POST':
        username = request.form.get('username')
        print("Username:", username)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM Person WHERE Username = %s AND Type = '1'"
        val = (username,)
        print("SQL query:", sql)
        print("Values:", val)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        print("Person:", person)
        if person:
            return redirect(url_for('child_dashboard'))  # Redirect to child dashboard
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('2_login.html', title='Login', show_error_grownup= False, show_error_child=True)
    else:
        return render_template('2_login.html', title='Login', show_error_grownup= False, show_error_child=False)
