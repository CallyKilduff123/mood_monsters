from flask import url_for, render_template, request, redirect, session
from datetime import datetime, timedelta


from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home')



@app.route('/login-register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        print("Username:", username)
        print("PIN:", pin)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM person WHERE Username = %s AND (PIN = %s OR (Type = 'Child' AND PIN IS NULL))"
        val = (username, pin)
        print("SQL query:", sql)
        print("Values:", val)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        print("Person:", person)
        if person:
            if person[5] == 'Grown-up':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('child_dashboard'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('2_register.html', title='Login/Register', error_message=error_message)
    else:
        return render_template('2_register.html', title='Login/Register')



@app.route('/child_dashboard')
def dashboard():
    return render_template('3_childdashboard.html', title='Dashboard')
