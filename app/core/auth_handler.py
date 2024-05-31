# app/core/auth_handler.py

import os
import time
from typing import Dict
import jwt
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJwt(user_id: str) -> Dict[str, str]:
    payload = {
        "sub": user_id,
        "exp": time.time() + 600  # Set expiration time to 10 minutes from now
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_response(token)

def decodeJwt(token: str) -> Dict[str, str]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
