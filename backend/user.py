"""User.py"""
class UserManager:
    """Represents a logged in user"""
    def __init__(self, uid, username):
        self.id = uid
        self.username = username

    is_logged_in = False

    def get_id(self):
        """Gets the user's id"""
        return str(self.id)

    def get_username(self):
        """Gets the user's username"""
        return str(self.username)
