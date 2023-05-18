from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'python_flask_mysql_exam'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #READ- getting user by id
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    #READ- getting users by email if needed
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    #READ-getting all users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for user in results:
                users.append(user)
            return users
        return users
    
    #CREATE- saving data to database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #READ- getting cars that a user has bought
    @classmethod
    def get_bought_cars(cls, data):
        query="SELECT cars.make as make, cars.model as model, cars.year as year FROM buys LEFT JOIN cars ON buys.car_id = cars.id WHERE buys.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        boughtCars = []
        if results:
            for row in results:
                boughtCars.append(row)
            return boughtCars
        return boughtCars
    
    #VALIDATING THE USER
    @staticmethod
    def validate_user(user):
        is_valid = True
        
        if len(user['first_name']) <3:
            flash('First name should be more than 3 characters!', 'firstNameRegister')
            is_valid= False
        if len(user['last_name']) <3:
            flash('Last name should be more than 3 characters!', 'lastNameRegister')
            is_valid= False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) <8:
            flash('Password should be more then 8 characters!', 'passwordRegister')
            is_valid= False
        if user['password'] != user['confirmPassword']:
            flash('Passwords do not match!', 'confirmPasswordRegister')
            is_valid = False
        return is_valid
        