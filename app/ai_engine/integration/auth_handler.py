import logging
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

logger = logging.getLogger(__name__)

# In production, load this securely from environment variables matching HealTrack backend secret
JWT_SECRET_KEY = "super-secret-production-jwt-key-change-this-in-env"
JWT_ALGORITHM = "HS256"

security = HTTPBearer()

class AuthHandler:
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token provided.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token provided.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )