from datetime import datetime, timedelta
from hikka import utils
import hashlib
import config
import bcrypt
import base58
import hmac
import json

def hashpwd(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()

def checkpwd(password, bcrypt_hash) -> bool:
    return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))

# https://gist.github.com/darelf/190bc97b29e91509534d7535ebde4762
class JWT():
    @classmethod
    def create_signed_token(cls, key, data):
        """
        Create a complete JWT token. Exclusively uses blake2b
        HMAC.
        """
        header = json.dumps({"typ": "JWT", "alg": "BLK2B"}).encode("utf-8")
        henc = base58.b58encode_check(header).decode()

        payload = json.dumps(data).encode("utf-8")
        penc = base58.b58encode_check(payload).decode()

        hdata = henc + "." + penc

        d = hmac.new(key, hdata.encode("utf-8"), digestmod=hashlib.blake2b)
        dig = d.digest()
        denc = base58.b58encode_check(dig).decode()

        token = hdata + "." + denc
        return token

    @classmethod
    def verify_signed_token(cls, key, token):
        """
        Validate token HMAC signature.
        """
        try:
            (header, payload, sig) = token.split(".")
            hdata = header + "." + payload

            d = hmac.new(key, hdata.encode("utf-8"), digestmod=hashlib.blake2b)
            dig = d.digest()
            denc = base58.b58encode_check(dig).decode()

            return hmac.compare_digest(sig, denc)

        except Exception:
            return False

    @classmethod
    def decode_payload(cls, token):
        """
        Decodes the payload in the token and returns a dict.
        """
        try:
            (header, payload, sig) = token.split(".")
            return json.loads(base58.b58decode_check(payload).decode())

        except Exception:
            return {}

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
