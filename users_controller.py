from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.spot_model import Spot

bcrypt = Bcrypt(app)

# our main route to get us to the log in/registration page


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# the route to post our registration information into our database and bring us to our dashboard


@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass,
        'confirmed_password': hashed_pass
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect('/dashboard')

# the route to post our log-in information into our database and ensure it matches with an already created user and bring us to our dashboard


@app.route('/users/login', methods=['POST'])
def log_user():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credentials", 'log')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# route that brings us back to the reg/login page


@app.route('/users/logout')
def log_out():
    del session['user_id']
    return redirect('/')

# our central page once logged in, main data source for sitings


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_spots = Spot.get_all()
    context = {
        'logged_user': logged_user,
        'all_spots': all_spots
    }
    return render_template('welcome.html', **context)
