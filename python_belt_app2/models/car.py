from python_belt_app2 import app
from python_belt_app2.config.mysqlconnection import connectToMySQL
import re
import datetime

class Car:
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    # GET FUNCTIONS
    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars"
        cars_db = connectToMySQL().query_db(query)
        cars = []
        for c in cars_db: cars.append(cls(c))
        return cars
        
    @classmethod
    def get_all_cars_sold_ids(cls):
        query = "SELECT car_id FROM purchases"
        cars_db = connectToMySQL().query_db(query)
        cars = []
        for c in cars_db:
            cars.append(c["car_id"])
        return cars

    @classmethod
    def get_car(cls, data):
        # print("------", data)
        query = "SELECT * FROM cars WHERE cars.id = %(car_id)s"
        show_db =  connectToMySQL().query_db(query, data)
        return cls(show_db[0])

    @classmethod
    def get_car_seller_name(cls, data):
        # print("------", data)
        query = "SELECT users.first_name, users.last_name FROM users JOIN cars ON users.id = cars.user_id WHERE cars.id = %(car_id)s"
        name_db =  connectToMySQL().query_db(query, data)
        print(name_db)
        return f"{name_db[0]['first_name']} {name_db[0]['last_name']}"

    @classmethod
    def get_all_cars_of_a_user(cls, data):
        # print("-----------", data)
        query = "SELECT cars.id, cars.price, cars.model, cars.make, cars.year, cars.description, cars.created_at, cars.updated_at, cars.user_id FROM users JOIN purchases ON users.id = purchases.user_id JOIN cars ON purchases.car_id = cars.id WHERE users.id = %(user_id)s"
        cars_db = connectToMySQL().query_db(query, data)
        cars = []
        for c in cars_db: cars.append(cls(c))
        return cars

    # VALIDATION FUNCTIONS
    @staticmethod
    def price_is_valid(data):
        if data["price"]:
            return int(data["price"]) > 0
        else:
            return False

    @staticmethod
    def model_is_valid(data):
        MODEL_REGEX = re.compile(r"^.+$")
        return (MODEL_REGEX.match(data["model"]))

    @staticmethod
    def make_is_valid(data):
        MAKE_REGEX = re.compile(r"^.+$")
        return (MAKE_REGEX.match(data["make"]))

    @staticmethod
    def description_is_valid(data):
        DESCRIPTION_REGEX = re.compile(r"^.+$")
        return (DESCRIPTION_REGEX.match(data["description"]))

    @staticmethod
    def year_is_valid(data):
        if data["year"]:
            return int(data["year"]) > 0
        else:
            return False

    # CREATE FUNCTIONS
    @classmethod
    def add_car(cls, data):
        # print("GMSLKMDGFLKMSDKLFMSDKL", data)
        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def add_purchase(cls, data):
        query = "INSERT INTO purchases (created_at, updated_at, user_id, car_id) VALUES (NOW(), NOW(), %(user_id)s, %(car_id)s)"
        return connectToMySQL().query_db(query, data)

    # EDIT FUNCTIONS
    @classmethod
    def edit_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, updated_at = NOW() WHERE cars.id = %(car_id)s"
        connectToMySQL().query_db(query, data)

    # DELETE FUNCTIONS
    @classmethod
    def delete_car(cls, data):
        print(data)
        query = "DELETE FROM cars WHERE cars.id = %(car_id)s"
        connectToMySQL().query_db(query, data)

    # EXTRA FUNCTIONS
    def format_car_price(self):
        # print("zzzzzzzzzzzzzzzz", car)
        new_price = "{:,}".format(self.price)
        # print("tttttttttttttttt", new_price)
        self.price = new_price