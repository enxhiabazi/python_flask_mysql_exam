from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car

from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#ROOT ROOT
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

#OPENS register.html
@app.route('/registerPage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')

#SAVE-ing the data
@app.route('/register', methods = ['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    
    if User.get_user_by_email(request.form):
        flash('This email already exists', 'emailRegister')
        return redirect(request.referrer)

    if not User.validate_user(request.form):
        flash('You have some errors! Fix them to sign Up', 'registrationFailed')
        return redirect(request.referrer)

    # line- i know for sure that my validate_user was true. User had all the required info
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    return redirect('/loginPage')

#OPEN-ing login.html
@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

#SAVE-ing the login data
@app.route('/login', methods = ['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    if not User.get_user_by_email(request.form):
        flash('This email does not appear to be in our system! Try another one!', 'emailLogin')
        return redirect(request.referrer)
    
    user = User.get_user_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            flash('Wrong Password', 'passwordLogin')
            return redirect(request.referrer)
    
    session['user_id'] = user['id']
    return redirect('/')

#DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    cars = Car.get_all()
    soldCars = Car.get_purchased_cars()
    return render_template('dashboard.html', cars = cars, user=user, soldCars= soldCars)

#Profile
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    boughtCars = User.get_bought_cars(data)
    return render_template('usersPurchasedCars.html', boughtCars = boughtCars, user=user)

#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')

