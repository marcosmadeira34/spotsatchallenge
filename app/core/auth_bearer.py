# Arquivo responsável por implementar a classe JWTBearer que é responsável por verificar se o token JWT é válido ou não.

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decodeJwt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        try:
            if credentials:
                logging.info(f"Token received: {credentials.credentials}")
                
                if not credentials.scheme == "Bearer":
                    logging.error("Invalid authentication scheme.")
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
                
                if not self.verify_jwt(credentials.credentials):
                    logging.error("Invalid token or expired token.")
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                
                return credentials.credentials
            else:
                logging.error("Invalid authorization code.")
                raise HTTPException(status_code=403, detail="Invalid authorization code.")
        except Exception as e:
            logging.error(f"An exception occurred: {str(e)}")
            raise HTTPException(status_code=403, detail="An error occurred while processing the request.")
        

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            isTokenValid: bool = False
            payload = decodeJwt(jwtoken)
            logging.info(f"Decoded payload: {payload}")
            if payload:
                isTokenValid = True
            return isTokenValid
        except Exception as e:
            logging.error(f"An exception occurred with the token: {str(e)}")
            return False
