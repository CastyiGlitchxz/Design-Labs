"""Database.py"""
import configparser
import uuid
import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

config = configparser.ConfigParser()
config.read("config/service.config")
DATABASE_KEY = config["database"]["access_key"]

CLIENT = MongoClient(DATABASE_KEY)

DB = CLIENT["Accounts"]
ACCOUNTS = DB["users"]

def get_accounts():
    """Gets all database user. Confirmed, this does not work."""
    for users in ACCOUNTS.find({}):
        return users

def user_exist(username: str) -> str:
    """Checks to see if a user exists"""
    if ACCOUNTS.find_one({"user_name":username}):
        print(f"The user: {username} exists")
        return True
    print("The provided username is not linked to an account")
    return False

def try_account_access(username: str, password: str):
    """Attempts to gain access to an account by providing a username and password"""
    try:
        if ACCOUNTS.find_one({"user_name":username}):
            if check_password_hash( pwhash=ACCOUNTS.find_one({"user_name": username})["password"],
                    password=password ):
                print("Account Access Granted")
                return True
        print("Username or password is incorrect")
        return False
    except TypeError:
        return False
    
def get_user(username: str):
    return ACCOUNTS.find_one({"user_name": username})

def add_account(username: str, password: str):
    """Adds an user to the database"""
    if user_exist(username=username) is True:
        return "User exists"

    todays_date = datetime.datetime.now()
    uuid_gen = str(uuid.uuid4())
    user_details = {
        "user_name":username,
        "password":generate_password_hash(password),
        "userid":uuid_gen,
        "creation_date": todays_date.strftime("%c"),
        "permissions": [],
        "email": "",
    }
    ACCOUNTS.insert_one(user_details)
    return True
