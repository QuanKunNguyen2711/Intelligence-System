from SystemManagement.enums import SystemRole
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum

from app.common.utils import get_current_datetime


class Contact(BaseModel):
    id: str = Field(..., alias="_id")
    sid: str
    ref_id: str # ref to _id of 
    
    created_at: str = Field(..., alias="created_at", default_factory=get_current_datetime)
    
    model_config = ConfigDict(
        populate_by_name=True
    )
    
class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    