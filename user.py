from flask_login import UserMixin
from werkzeug import check_password_hash, generate_password_hash


# UserMixin supplies needed properties and methods to the User class for the
# Flask-Login extension
class User(UserMixin):
    # Unique user id via class variable
    counter = 1
    # Enforce user uniqueness with class variable
    usernames = set()

    def __init__(self, username, passwd, passwd_hash=None):
        if username in User.usernames:
            raise ValueError(f'Username "{username}" already in use!')
        self.username = username
        User.usernames.add(username)
        if passwd_hash is None:
            self.passwd_hash = generate_password_hash(passwd)
        else:
            self.passwd_hash = passwd_hash
        self.id = User.counter
        User.counter += 1

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username})>'

    def check_password(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    @staticmethod
    def exists(username):
        return username in User.usernames

