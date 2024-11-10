"""Database.py"""
import configparser
from pymongo import MongoClient

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
    if ACCOUNTS.find_one({"user_name":username, "password":password}):
        print("Account Access Granted")
        return True
    else:
        print("Username or password is incorrect")
        return False
    
print(try_account_access("", "e"))

# print(user_exist("NinjaMasterMods"))
# print(get_accounts())
