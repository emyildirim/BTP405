# This file contains authentication and authorization functions
from dotenv import load_dotenv
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

load_dotenv('./.env')

#replace the secret key with yours in the .env
SECRET = os.getenv('JWT_SECRET')

class JWTHandler:
    @staticmethod
    def generate_token(data, expire_duration=60):
        exp = datetime.utcnow() + timedelta(minutes=expire_duration)
        data.update({"exp": exp})
        token = jwt.encode(data, SECRET, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {"message": "token expired. pls log in again."}
        except jwt.InvalidTokenError:
            return {"message": "invalid token. pls log in again."}


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))