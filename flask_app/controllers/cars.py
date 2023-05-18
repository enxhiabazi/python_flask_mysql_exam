from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car

from flask import render_template, redirect, session, request, flash
#ADD CAR
@app.route('/add/car')
def addCar():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('addCar.html', user = user)
    return redirect('/')

#CREATE CAR
@app.route('/create/car', methods = ['POST'])
def createCar():
    if 'user_id' in session:
        if not Car.validate_car(request.form):
            return redirect(request.referrer)
        data = {
            'prize': request.form.get('prize',''),
            'model': request.form['model'],
            'make': request.form['make'],
            'year': request.form.get('year',''),
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        Car.save(data)
        return redirect('/dashboard')
    return redirect('/')

#EDIT CAR
@app.route('/edit/car/<int:id>')
def editCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        user = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        if user['id'] == car['user_id']:
            return render_template('editCar.html', user = user, car= car)
        return redirect('/dashboard')
    return redirect('/')

#UPDATE CAR
@app.route('/update/car/<int:id>', methods = ['POST'])
def updateCar(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'car_id': id
        }
        user = User.get_user_by_id(data1)
        car = Car.get_car_by_id(data1)
        if user['id'] == car['user_id']:
            if not Car.validate_car(request.form):
                return redirect(request.referrer)
            data = {
            'prize': request.form['prize'],
            'model': request.form['model'],
            'make': request.form['make'],
            'year': request.form['year'],
            'description': request.form['description'],
            'car_id': id
            }
            Car.update(data)
            return redirect('/')
        return redirect('/dashboard')
    return redirect('/')

#VIEW CAR
@app.route('/view/<int:id>')
def viewCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        user = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        soldCars = Car.get_purchased_cars()
        if car['id'] in soldCars:
            return redirect('/dashboard')
        return render_template('showOne.html', user = user, car= car, soldCars = soldCars)
    return redirect('/')

#DELETE CAR
@app.route('/delete/car/<int:id>')
def deleteCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        user = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        if user['id'] == car['user_id']:
            Car.deleteAllPurchases(data)
            Car.delete(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

#BUY CAR
@app.route('/purchase/<int:id>')
def buyCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        soldCars = Car.get_purchased_cars()
        if id not in soldCars:
            Car.buyCar(data)
            return redirect('/dashboard')
        return redirect(request.referrer)
    return redirect('/')


