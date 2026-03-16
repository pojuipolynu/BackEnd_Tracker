import time
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from core.config import settings
from uuid import UUID
from fastapi import HTTPException, status
from core.config import settings

class UserToken:
    def __init__(self):
        self.config = settings

    def sign_token(self, user: UUID):
        payload = {"email": user, "exp": time.time() + 5184000}
        try:
            token = jwt.encode(payload, self.config.JWT_SECRET, algorithm=self.config.JWT_ALGORITHM)
            return token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error encoding token")

    def decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(token, self.config.JWT_SECRET, algorithms=[self.config.JWT_ALGORITHM])
            return decoded_token
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        

user_token = UserToken()