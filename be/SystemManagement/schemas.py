from pydantic import BaseModel, EmailStr
from fastapi import UploadFile

from CustomerManagement.models import Gender

class LoginSchema(BaseModel):
    email: EmailStr
    pwd: str
    
class HotelOwnerSchema(BaseModel):
    name: str
    email: EmailStr
    pwd: str
    address: str
    city: str
    
    
class CustomerSchema(BaseModel):
    name: str
    email: EmailStr
    pwd: str
    gender: Gender
    city: str
    phone_number: str