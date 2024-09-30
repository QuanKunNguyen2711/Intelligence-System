from fastapi import APIRouter, HTTPException
from SystemManagement.enums import SystemRole
from SystemManagement.schemas import CustomerSchema, HotelOwnerSchema, LoginSchema
from SystemManagement.services import SystemManagementService
from app.common.authentication import protected_route
from app.common.dependencies import AuthCredentialDepend


router = APIRouter()

@router.post("/login")
async def login(login_info: LoginSchema):
    try:
        system_management_service = SystemManagementService()
        login_info = login_info.model_dump()
        return await system_management_service.validate_user(email=login_info.get("email"), pwd=login_info.get("pwd"))
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, Exception):
            raise HTTPException(400, str(e))

@router.post("/register/hotel-owner")
async def register_hotel_owner(
    hotel_owner: HotelOwnerSchema,
):
    try:
        system_management_service = SystemManagementService()
        hotel_owner = hotel_owner.model_dump()
        return  await system_management_service.create_account(SystemRole.HOTEL_OWNER, hotel_owner)
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, Exception):
            raise HTTPException(400, str(e))
        
@router.post("/register/customer")
async def register_customer(
    customer: CustomerSchema,
):
    try:
        system_management_service = SystemManagementService()
        hotel_owner = hotel_owner.model_dump()
        return await system_management_service.create_account(SystemRole.CUSTOMER, hotel_owner)
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, Exception):
            raise HTTPException(400, str(e))