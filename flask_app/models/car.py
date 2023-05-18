from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    db_name = 'python_flask_mysql_exam'
    def __init__( self , data ):
        self.id = data['id']
        self.prize = data['prize']
        self.model = data['model']
        self.make = data['content']
        self.year = data['year']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #READ get car by id
    @classmethod
    def get_car_by_id(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users on cars.user_id = users.id WHERE cars.id = %(car_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return results
    
    #READ get all cars
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users on cars.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        cars = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for car in results:
                cars.append(car)
            return cars
        return cars
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (prize, model, make,year, description, user_id) VALUES ( %(prize)s, %(model)s,%(make)s,%(year)s,%(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET prize = %(prize)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #DELETE all purchases
    @classmethod
    def deleteAllPurchases(cls, data):
        query = "DELETE FROM buys WHERE car_id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #CREATE inserting into buys car id and the owner of the car
    @classmethod
    def buyCar(cls, data):
        query = "INSERT INTO buys (car_id, user_id) VALUES ( %(car_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    
    @classmethod
    def get_purchased_cars(cls):
        query = "SELECT car_id as id FROM buys;"
        results= connectToMySQL(cls.db_name).query_db(query)
        soldCars =[]
        if results:
            for car in results:
                soldCars.append(car['id'])
            return soldCars
        return soldCars
    
    #VALIDATION
    @staticmethod
    def validate_car(car):
        is_valid = True
        
        if car['prize'] == '':
            flash('Prize should not be empty!', 'prizeCar')
            is_valid= False
        if car['prize'] != '':
            if int(car['prize']) <0:
                flash('Prize should be less than zero', 'prizeCar')
                is_valid = False
        if len(car['model']) <3:
            flash('Model should be more than 3 characters!', 'modelCar')
            is_valid= False
        if len(car['make']) <3:
            flash('Make should be more than 3 characters!', 'makeCar')
            is_valid= False
        if car['year'] == '':
            flash('Year should not be empty!', 'yearCar')
            is_valid= False
        if len(car['description']) <3:
            flash('Description should be more than 3 characters!', 'descriptionCar')
            is_valid= False
        return is_valid
        