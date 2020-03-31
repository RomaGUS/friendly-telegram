from datetime import datetime, timedelta
from hikka.tools.jwt import JWT
from hikka import utils
import config
import bcrypt

def hashpwd(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()

def checkpwd(password, bcrypt_hash) -> bool:
    return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))

class Token():
    @classmethod
    def create(cls, action, meta, time=None, secret=None):
        delta = time if time else timedelta(days=3)
        expire = int(datetime.timestamp(datetime.now() + delta))
        key = secret if secret else config.secret
        return JWT.create_signed_token(utils.blake2b(key), {
            "action": action,
            "expire": expire,
            "meta": meta
        })

    @classmethod
    def validate(cls, token, secret=None):
        key = secret if secret else config.secret
        valid = JWT.verify_signed_token(utils.blake2b(key), token)
        payload = JWT.decode_payload(token)

        if "expire" not in payload:
            valid = False

        else:
            if payload["expire"] < int(datetime.timestamp(datetime.now())):
                valid = False

        return valid

    @classmethod
    def payload(cls, token):
        return JWT.decode_payload(token)
