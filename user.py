"""User.py"""
from flask_login import LoginManager, UserMixin
from database import ACCOUNTS

login_manager = LoginManager()

class User(UserMixin):
    """Represents a user"""

    Users = {}

    def __init__(self, uid, username):
        self.id = uid
        self.username = username
    #    password_hash = ACCOUNTS.

    def get_id(self):
        return str(self.id)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute!')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate

# user = User(uuid.uuid4(), "")

# pylint: disable=E0213
@login_manager.user_loader
def load_user(username):
    """Load the user into flask-login."""
    obj_usrn = ""
    obj_uid = ""

    get_user = ACCOUNTS.find({"user_name":username}, ['user_name'])
    userid = ACCOUNTS.find({"user_name":username}, ['userid'])

    for a in get_user:
        obj_usrn = a['user_name']

    for u in userid:
        obj_uid = u['userid']
    user = User(username=obj_usrn, uid=obj_uid)
    return user
