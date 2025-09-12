from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = "WIXYAhAfU6tLOloxqHgI4thAAo6kshkK"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    from ..schemas.user import User
    from ..utils.db import fetch_one

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # 데이터베이스에서 사용자 조회
    user_row = await fetch_one("SELECT * FROM users WHERE username = ?", (username,))

    if user_row is None:
        raise credentials_exception

    user = User(
        id=user_row["id"],
        username=user_row["username"],
        email=user_row["email"],
        password_hash=user_row["password_hash"],
        salt=user_row["salt"],
        created_at=user_row["created_at"],
        profile_image_path=user_row["profile_image_path"],
        is_active=user_row["is_active"],
    )

    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
