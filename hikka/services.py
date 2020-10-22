from hikka.models import User
from pony import orm

class UserService(object):
    @classmethod
    def get_by_username(cls, username):
        return orm.select(
            c for c in User if c.username == username
        ).first()

    @classmethod
    def get_by_email(cls, email):
        return orm.select(
            c for c in User if c.email == email
        ).first()

    @classmethod
    def create(cls, username, password, email):
        return User(
            username=username,
            password=password,
            email=email
        )
