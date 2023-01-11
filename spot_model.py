from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
from flask_app.models import fish_model
import re

# Class that cotains all database information regarding sitings


class Spot:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.attributes = data['attributes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# method that insterts a new spot into our database

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO spots (name, location, attributes, user_id)
            VALUES (%(name)s, %(location)s, %(attributes)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# method that gathers every piece of information from spots/users and links together

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM spots JOIN users ON spots.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_spots = []
        if results:
            for row in results:
                this_spot = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_spot.witness = this_user
                all_spots.append(this_spot)
        return all_spots

# similar to prior but only gathers information on a user/spot that matches with the id chosen

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM spots LEFT JOIN fish ON spots.id = fish.spot_id
                WHERE spots.id = %(id)s;
            """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            spot_instance = cls(results[0])
            catches_list = []
            for row_in_db in results:
                if row_in_db['fish.id'] == None:
                    return spot_instance
                fish_data = {
                    'id': row_in_db['fish.id'],
                    'type': row_in_db['type'],
                    'length': row_in_db['length'],
                    'weight': row_in_db['weight'],
                    'nickname': row_in_db['nickname'],
                    'bait': row_in_db['bait'],
                    'date': row_in_db['date'],
                    'moon_phase': row_in_db['moon_phase'],
                    'tide': row_in_db['tide'],
                    'weather': row_in_db['weather'],
                    'trophy': row_in_db['trophy'],
                    'spot_id': row_in_db['spot_id'],
                    'created_at': row_in_db['created_at'],
                    'updated_at': row_in_db['updated_at']
                }
                fish_instance = fish_model.Fish(fish_data)
                catches_list.append(fish_instance)
            spot_instance.fish = catches_list
            return spot_instance
        return False

# method that updates information on a previously created user/spot

    @classmethod
    def update(cls, data):
        query = """
            UPDATE spots SET name = %(name)s, location = %(location)s, attributes = %(attributes)s
            WHERE spots.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# method that deletes entire information of a certain id from database

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM spots WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# our only static method, validates our users input to ensure it meets our guidelines before proceeding to the next page

    @classmethod
    def spots_Desc(cls):
        query = """
            SELECT * FROM spots 
            ORDER BY name DESC;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_spots = []
        if results:
            for row in results:
                this_spot = cls(row)
                all_spots.append(this_spot)
        return all_spots

    @classmethod
    def spots_Asc(cls):
        query = """
            SELECT * FROM spots 
            ORDER BY name ASC;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_spots = []
        if results:
            for row in results:
                this_spot = cls(row)
                all_spots.append(this_spot)
        return all_spots

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 1:
            flash('name required')
            is_valid = False
        if len(form_data['location']) < 1:
            flash('location required')
            is_valid = False
        if len(form_data['attributes']) < 1:
            flash('attributes required')
            is_valid = False
        return is_valid
