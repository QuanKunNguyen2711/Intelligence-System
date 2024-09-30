from pydantic import BaseModel, EmailStr
from fastapi import UploadFile

from CustomerManagement.models import Gender

class TrainModelSchema(BaseModel):
    name: str
    description: str
    batch_size: int = 64
    hidden_size: int = 64
    num_epochs: int = 30
    