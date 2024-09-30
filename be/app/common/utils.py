from datetime import datetime
import pytz
from unidecode import unidecode
import random

def get_current_datetime():
    hcm_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    return datetime.now(hcm_timezone).strftime('%Y-%m-%d %H:%M:%S')

def convert_str(name: str = "") -> str:
    return unidecode(name).lower().replace(" ", "")

def generate_model_id(name: str = "") -> str:
    rand_num = random.randint(0, 999999)
    rand_6_digits = f"{rand_num:06}"
    return "model_" + convert_str(name) + f"_{rand_6_digits}"

def generate_db_business(name: str = "") -> str:
    """
        Generate unique business's db with format "db_nhuatienphong_123456"
    """
    rand_num = random.randint(0, 999999)
    rand_6_digits = f"{rand_num:06}"
    return "db_" + convert_str(name) + f"_{rand_6_digits}"