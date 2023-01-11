from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
from flask_app.models import spot_model
from flask_app.models import fish_model
import re

# Class that cotains all database information regarding sitings


class Fish:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.type = data['type']
        self.length = data['length']
        self.weight = data['weight']
        self.nickname = data['nickname']
        self.bait = data['bait']
        self.date = data['date']
        self.moon_phase = data['moon_phase']
        self.tide = data['tide']
        self.weather = data['weather']
        self.trophy = data['trophy']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.spot_id = data['spot_id']

    @classmethod
    def create(self, data):
        query = """
            INSERT INTO fish (type, length, weight, nickname, bait, date, moon_phase, tide, weather, trophy, spot_id)
            VALUES (%(type)s, %(length)s, %(weight)s, %(nickname)s, %(bait)s, %(date)s, %(moon_phase)s, %(tide)s, %(weather)s, %(trophy)s, %(spot_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_trophies(cls):
        query = """
                SELECT * FROM fish 
                WHERE fish.trophy = 'yes';
            """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        trophies_list = []
        for row in results:
            trophies_list.append(cls(row))
            print(trophies_list)
        return trophies_list

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM spots LEFT JOIN fish ON spots.id = fish.spot_id
                WHERE spots.id = %(id)s;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            spot_instance = cls(results[0])
            catches_list = []
            for row_in_db in results:
                fish_data = {
                    'id': row_in_db['fish.id'],
                    'type': row_in_db['type'],
                    'spot_id': row_in_db['spot_id'],
                    'created_at': row_in_db['created_at'],
                    'updated_at': row_in_db['updated_at']
                }
                # fish_data = {
                #     **row_in_db,

                # }
                fish_instance = fish_model.Fish(fish_data)
                catches_list.append(fish_instance)
            spot_instance.fish = catches_list
            return spot_instance
        return False

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * FROM fish JOIN spots ON fish.spot_id = spots.id
            WHERE fish.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            row = results[0]
            this_fish = cls(row)
            spots_data = {
                **row,
                'id': row['spots.id'],
                'created_at': row['spots.created_at'],
                'updated_at': row['spots.updated_at']
            }
            this_spot = spot_model.Spot(spots_data)
            this_spot.witness = this_spot
            return this_fish
        return False

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM fish WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
