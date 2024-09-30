from fastapi import UploadFile
from SystemManagement.enums import SystemRole
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum

from app.common.utils import get_current_datetime

class SystemUserBase(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    role: SystemRole
    email: EmailStr
    pwd: str
    
    created_at: str = Field(..., alias="created_at", default_factory=get_current_datetime)
    
    model_config = ConfigDict(
        populate_by_name=True
    )

class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    
class CustomerModel(SystemUserBase):
    gender: Gender
    city: str
    phone_number: str
    
class HotelOwnerModel(SystemUserBase):
    db: str
    address: str
    city: str
    