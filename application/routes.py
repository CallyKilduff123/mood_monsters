from flask import Flask, render_template, request, redirect, url_for, session
from application.data_access import child_login, grownup_login
from datetime import datetime, timedelta
from application import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('1_home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        if request.form.get('login_type') == 'grownup':
            return grownup_login()
        elif request.form.get('login_type') == 'child':
            return child_login()
    return render_template('2_login.html', title='Login')

# route to database














# @app.route('/register')
# def register():
#     return render_template('3_register.html', title='Register')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         child-firstname = request.form['child firstname']
#         child-lastname = request.form['child lastname']
#         child-username = request.form['child username']
#         child-age = request.form['child age']
#         grownup-firstname = request.form['grownup-firstname']
#         grownup-lastname = request.form['grownup-lastname']
#         grownup-username = request.form['grownup-username ']
#         email = request.form['email']

        # # Call person from data_access.py to insert the person into the database
        # add_baby_to_db(firstname, lastname, gender, date_of_birth, gestational_age_at_birth_weeks,
        #          gestational_age_at_birth_days, birthweight_grams)

    #     # Redirect to the baby list page after adding a new baby
    #     return redirect(url_for('all_babies_from_db'))
    #
    # return render_template('7_add_baby.html', title='Add baby to list')






@app.route('/grownup_dashboard')
def grownup_dashboard():
    return render_template('4_grownup_dashboard.html', title='Dashboard')

@app.route('/child_dashboard')
def child_dashboard():
    return render_template('5_child_dashboard.html', title='Dashboard')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get data from the form
    child_firstname = request.form['child_firstname']
    child_lastname = request.form['child_lastname']
    child_username = request.form['child_username']
    age = request.form['age']
    grownup_firstname = request.form['grownup_firstname']
    grownup_lastname = request.form['grownup_lastname']
    grownup_username = request.form['grownup_username']
    email = request.form['email']
    nominated = 'nomination' in request.form

    # Create records in the database
    # Assuming you have models for Person, Child, and GrownUp
    # You can also handle the nomination status as needed
    Child = Child(firstname=child_firstname, lastname=child_lastname, username=child_username, age=age)
    grown_up = Grown_Up(firstname=grownup_firstname, lastname=grownup_lastname, username=grownup_username, email=email)
    Person = Person(nominated=nominated, child=child, grownup=grownup)

    # Commit to the database
    # Assuming you have a database session set up
    session.add(person)
    session.commit()

    return 'Registration successful'
