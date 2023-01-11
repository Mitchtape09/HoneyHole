from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_app.models import spot_model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Class that cotains all database information regarding users


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# method that insterts a new user into our database

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# similar to prior but only gathers information on a user/spot that matches with the id chosen

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM users
            LEFT JOIN spots ON spots.user_id = users.id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            user_instance = cls(results[0])
            spot_list = []
            for row in results:
                spot_data = {
                    **row,
                    'id': row['spots.id'],
                    'created_at': row['spots.created_at'],
                    'updated_at': row['spots.updated_at']
                }
                this_spot_instance = spot_model.Spot(spot_data)
                spot_list.append(this_spot_instance)
            user_instance.witness = spot_list
            return user_instance
        return False

# method that gets all the users where the email id matches

    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

# our only static method, validates our users input to ensure it meets our guidelines before proceeding to the next page

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("first name must be at least 2 chars", 'reg')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("last name must be at least 2 chars", 'reg')
            is_valid = False
        if len(form_data['email']) < 2:
            flash("email required", 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("email invalid", 'reg')
            is_valid = False
        else:
            data = {
                'email': form_data['email']
            }
            potential_user = User.get_by_id(data)
            if potential_user:
                flash("email already exists", 'reg')
                is_valid = False
        if len(form_data['password']) < 8:
            flash("password name must be at least 8 chars", 'reg')
            is_valid = False
        elif not form_data['password'] == form_data['confirm_pass']:
            flash("passwords must match", 'reg')
            is_valid = False

        return is_valid
