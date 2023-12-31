from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.database.db_manager import get_user_by_username
from app.models.token import TokenData

SECRET_KEY = "your_secret_key"  # This should be securely stored and not hardcoded
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_token(username: str):
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expiration, "sub": username}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Security(oauth2_scheme)):
    print(f"Token received: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"Username extracted from token: {username}")
        if username is None:
            print("Username is None")
            raise credentials_exception
        token_data = TokenData(username=username)
        print(f"Token data extracted: {token_data}")
    except (ValueError, KeyError, jwt.exceptions.DecodeError) as e:
        print(f"Exception raised: {e}")
        raise credentials_exception from e
    user = get_user_by_username(token_data.username)
    print(f"User retrieved from database: {user}")
    if user is None:
        print("User is None")
        raise credentials_exception
    return user
