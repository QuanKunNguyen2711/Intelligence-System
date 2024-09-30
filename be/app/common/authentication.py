from typing import List
from fastapi import HTTPException, status
from app.common.db_collections import RootCollections
from SystemManagement.enums import DB_ROOT, SystemRole
from functools import wraps
from app.common.db_connector import client
import jwt
import os


def protected_route(role: List[SystemRole]):
    def auth_required(func):
        @wraps(func)
        async def wrapper(**kwargs):
            token = kwargs.get("CREDENTIALS").credentials
            # authen_service = kwargs.get("AUTHEN_SERVICE")
            current_user = await get_user_by_token(token, {"pwd": 0, "created_at": 0})
            kwargs["CURRENT_USER"] = current_user
            if current_user.get("role") not in role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid System Role!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return await func(**kwargs)
        return wrapper
    return auth_required


async def get_user_by_token(access_token: str, projection: dict = {}) -> dict:
    payload = jwt.decode(access_token, os.environ.get("SECRET_SALT"), algorithms=[os.environ.get("JWT_ALGORITHM")])
    user_id = payload.get("_id")
    user_db = payload.get("db")
    db = client.get_database(DB_ROOT)
    col = db.get_collection(RootCollections.USERS)
    user = await col.find_one({"_id": user_id, "db": user_db}, projection)
    return user