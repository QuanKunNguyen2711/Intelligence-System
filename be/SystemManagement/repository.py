from SystemManagement.enums import DB_ROOT
from SystemManagement.models import HotelOwnerModel
from app.common.db_collections import RootCollections
from app.common.db_connector import client

class SystemManagementRepository:
    def __init__(self):
        global client
        self.db =  client.get_database(DB_ROOT)
        self.users_coll = self.db.get_collection(RootCollections.USERS)
        
    async def is_existed_email(self, email: str) -> bool:
        return True if await self.find_one_by_email(email) else False
    
    async def find_one_by_email(self, email: str, proj: dict = {}) -> dict:
        return await self.users_coll.find_one({"email": email}, proj)
    
    async def create_hotel_owner(self, hotel_owner: HotelOwnerModel) -> str:
        doc = await self.users_coll.insert_one(hotel_owner)
        return doc.inserted_id
        
    