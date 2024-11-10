"""User.py"""
from flask_login import LoginManager, UserMixin
from database import ACCOUNTS

login_manager = LoginManager()

class User(UserMixin):
    """Represents a user"""
    def __init__(self, id, username):
       self.id = id
       self.username = username

    def get_id(self):
       return str(self.id)

# user = User(uuid.uuid4(), "")

# pylint: disable=E0213
@login_manager.user_loader
def load_user(username):
    """Load the user into flask-login."""
    user = User(username=username, id=None)
    user.username = ACCOUNTS.find_one({"user_name":username})
    user.id = ACCOUNTS.find_one({"user_name":username}, ['userid'])
    return user

print(load_user("CastyiGlitchxz"))
