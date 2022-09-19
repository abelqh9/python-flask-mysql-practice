from python_belt_app2 import app, bcrypt
from python_belt_app2.config.mysqlconnection import connectToMySQL
import re

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # GET FUNCTIONS
    @classmethod
    def get_user(cls, data):
        query = "SELECT id, first_name, last_name, email, created_at, updated_at FROM users WHERE users.id = %(user_id)s"
        user_db =  connectToMySQL().query_db(query, data)
        return cls(user_db[0])

    @classmethod
    def get_other_users(cls, data):
        query = "SELECT id, first_name, last_name, email FROM users WHERE NOT users.id = %(user_id)s"
        users_db =  connectToMySQL().query_db(query, data)
        users = []
        for u in users_db: users.append(cls(u))
        return users

    @classmethod
    def get_user_id_by_email(cls, data):
        query = "SELECT id FROM users WHERE users.email = %(email)s"
        user_db =  connectToMySQL().query_db(query, data)
        return user_db[0]["id"]

    @classmethod
    def get_user_password_by_email(cls, data):
        query = "SELECT password FROM users WHERE users.email = %(email)s"
        user_db =  connectToMySQL().query_db(query, data)
        return user_db[0]["password"]

    @classmethod
    def get_all_emails(cls):
        query = "SELECT email FROM users"
        emails_db = connectToMySQL().query_db(query)
        emails = []
        for e in emails_db: emails.append(e["email"])
        return emails

    # VALIDATION FUNCTIONS
    @staticmethod
    def first_name_is_valid(data):
        FIRST_REGEX = re.compile(r"^.{3,}$")
        return (FIRST_REGEX.match(data["first_name"]))

    @staticmethod
    def last_name_is_valid(data):
        LAST_REGEX = re.compile(r"^.{3,}$")
        return (LAST_REGEX.match(data["last_name"]))

    @staticmethod
    def email_is_valid(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        return (EMAIL_REGEX.match(data["email"]))
            
    @classmethod
    def email_exist(cls, data):
        return (data["email"] in cls.get_all_emails())

    @staticmethod
    def password_is_valid(data):
        PASSWORD_REGEX = re.compile(r"^.{8,}$")
        return PASSWORD_REGEX.match(data["password"])

    @classmethod
    def password_is_correct(cls, data):
        password_db = cls.get_user_password_by_email(data)
        return bcrypt.check_password_hash(password_db, data["password"])

    # CREATE FUNCITONS
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def create_password(cls, data):
        return bcrypt.generate_password_hash(data["password"])