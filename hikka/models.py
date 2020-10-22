from datetime import datetime
from pony import orm

db = orm.Database("sqlite", "../hkkio.db", create_db=True)

class User(db.Entity):
    _table_ = "hikka_users"

    created = orm.Optional(datetime, default=datetime.utcnow)
    reset = orm.Optional(datetime, default=datetime.utcnow)
    login = orm.Optional(datetime, default=datetime.utcnow)
    activated = orm.Optional(bool, default=False)
    username = orm.Required(str, index=True)
    email = orm.Required(str, index=True)
    password = orm.Required(str)


db.generate_mapping(create_tables=True)
