import os
from typing import Union
import bcrypt
from bson import ObjectId
from pydantic import EmailStr
import jwt
from SystemManagement.enums import SystemRole
from SystemManagement.models import CustomerModel, HotelOwnerModel
from SystemManagement.repository import SystemManagementRepository
from app.common.utils import generate_db_business


class SystemManagementService:
    def __init__(self):
        self.repo = SystemManagementRepository()
        
    async def validate_user(self, email: EmailStr, pwd: str) -> Union[str, None]:
        user = await self.repo.find_one_by_email(email, {"created_at": 0})
        if user and not self.is_valid_password(pwd, user.get("pwd")):
            raise Exception("Invalid password")
        
        if user and self.is_valid_password(pwd, user.get("pwd")):
            user.pop("pwd")
            return self.encode_jwt(user)
            
        return None
    
    def encode_jwt(self, obj: dict) -> str:
        return jwt.encode(obj, os.environ.get("SECRET_SALT"), algorithm=os.environ.get("JWT_ALGORITHM"))
       
    def decode_jwt(self, encoded_jwt: str) -> dict:
        return jwt.decode(encoded_jwt, os.environ.get("SECRET_SALT"), algorithms=[os.environ.get("JWT_ALGORITHM")])
    
    def is_valid_password(self, raw_pwd: str, hashed_pwd: str) -> bool:
        encoded_raw_pwd, encoded_hashed_pwd = raw_pwd.encode("utf-8"), hashed_pwd.encode("utf-8")
        return bcrypt.checkpw(encoded_raw_pwd, encoded_hashed_pwd)
            
    async def create_account(self, role: SystemRole, detail: dict) -> str:
        raw_pwd = detail.get("pwd")
        name = detail.get("name")
        email = detail.get("email")
        if await self.repo.is_existed_email(email):
            raise Exception(f"Email {email} has already been used.")
        
        # Hashing pwd
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(raw_pwd.encode('utf-8'), salt).decode("utf-8")
        
        if role is SystemRole.HOTEL_OWNER:
            db_hotel_owner = generate_db_business(name)
            
            model = HotelOwnerModel(
                _id = str(ObjectId()),
                name = name,
                email = email,
                pwd = hashed_pwd,
                db = db_hotel_owner,
                role = SystemRole.HOTEL_OWNER,
                address = detail.get("address"),
                city = detail.get("city"),
            )
            
            return await self.repo.create_hotel_owner(model.model_dump(by_alias=True))
        
        elif role is SystemRole.CUSTOMER:
            model = CustomerModel(
                _id = str(ObjectId()),
                name = name,
                email = email,
                pwd = hashed_pwd,
                gender = detail.get("gender"),
                role = SystemRole.CUSTOMER,
                phone_number = detail.get("phone_number"),
                city = detail.get("city"),
            )
            
            return await self.repo.create_customer(model.model_dump(by_alias=True))
        
        return ""