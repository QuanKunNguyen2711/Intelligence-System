from enum import Enum

class SystemRole(str, Enum):
    CUSTOMER = 'customer'
    HOTEL_OWNER = 'hotel_owner'
    DATA_SCIENTIST = 'data_scientist'
    
DB_ROOT = "travel_booking_agencies_root"