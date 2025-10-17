import os
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
HEADER = os.getenv('HEADER')
ACCESS_TOKEN_LIFETIME_MINUTES = int(os.getenv('ACCESS_TOKEN_LIFETIME_MINUTES', 60))
REFRESH_TOKEN_LIFETIME_DAYS = int(os.getenv('REFRESH_TOKEN_LIFETIME_DAYS', 7))


def create_access_token(payload: dict):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES)
    payload.update({'exp': expire})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def create_refresh_token(payload: dict):
    expire = datetime.now(tz=timezone.utc) + timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS)
    payload.update({"exp": expire})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


async def verify_jwt(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith(f'{HEADER}'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found or incorrect format.'
        )
    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        request.state.user = payload
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid or expired.'
        )
    
