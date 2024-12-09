"""Database.py"""
import configparser
import uuid
import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

config = configparser.ConfigParser()
config.read("config/service.config")
DATABASE_KEY = config["database"]["access_key"]

CLIENT = MongoClient(DATABASE_KEY)

DB = CLIENT["Accounts"]
ACCOUNTS = DB["users"]

def get_accounts():
    """Gets all database users"""
    for user in ACCOUNTS.find():
        return user

def user_exist(username) -> str:
    """Checks to see if a user exists"""
    if ACCOUNTS.find_one({"user_name":username}):
        print(f"The user: {username} exists")
        return True
    else:
        print("The provided username is not linked to an account")
        return False

def try_account_access(username, password):
    """Tries to access and account"""
    if ACCOUNTS.find_one({"user_name":username, "password":password}):
        print("Account Access Granted")
        return True
    else:
        print("Username or password is incorrect")
        return False

def add_account(username, password):
    """Adds an user to the database"""
    todays_date = datetime.datetime.now()
    x = str(uuid.uuid4())
    user_details = {
        "user_name":username,
        "password":generate_password_hash(password),
        "userid":x,
        "creation_date": todays_date.strftime("%c"),
        "email": "",
    }
    ACCOUNTS.insert_one(user_details)
