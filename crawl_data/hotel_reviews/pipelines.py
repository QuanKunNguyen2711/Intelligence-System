# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pymongo
import re
from datetime import datetime

from hotel_reviews.items import HotelDetailsItem, HotelReviewItem

city = "nhatrang"

class DataCleaningPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        # Removing '\n' room, booking_date, review_date, address
        for field in fields:
            if field in ["room", "booking_date", "review_date", "address", "title"]:
                value = adapter.get(field)
                adapter[field] = value.replace("\n", "") if value else ""
                
        if isinstance(item, HotelDetailsItem):
            # Convert "avg_score": "7,2" into 7.2
            value = adapter.get("avg_score")
            adapter["avg_score"] = float(value.replace(",", ".")) if value else None
            
            # Convert "total_reviews": "Đánh giá của khách (106)" into 106
            value = adapter.get("total_reviews")
            splitted = value.split("(") if value else ""
            val = splitted[-1][:-1] if value else ""
            val = val.replace(".", "") if "." in val else val
            adapter["total_reviews"] = int(val) if val else 0
            # adapter["total_reviews"] = int(re.search(r'\d+', value).group()) if value else 0
        
        elif isinstance(item, HotelReviewItem):
            # Convert "review_date": "Đã đánh giá: ngày 9 tháng 10 năm 2022" into "2022/10/09"
            value = adapter.get("review_date")
            date_string = value.split(": ")[-1]
            date = datetime.strptime(date_string, "ngày %d tháng %m năm %Y")
            adapter["review_date"] = date.strftime("%Y-%m-%d")
            
            # Convert "avg_score": " 6,0 " into 6.0
            value = adapter.get("avg_score")
            value = value.strip() if value else None
            value = value.replace(",", ".") if value else None
            adapter["avg_score"] = float(value) if value else None
            
            # Convert "booking_date": "2 đêm ·  tháng 8/2022" into "2 đêm`08/2022"
            value = adapter.get("booking_date")
            # Remove extra spaces and newlines
            value = re.sub(r'\s+', ' ', value)
            # Extract the desired components using regular expressions
            value = re.findall(r'\d+|\d+/\d+', value) # ["2", "8", "2022"]
            date = datetime(int(value[2]), int(value[1]), 1)
            date_str = date.strftime("%m/%Y")
            adapter["booking_date"] = value[0] + " đêm ` " + date_str
        
        return item

class MongodbPipeline:
    # Collections
    HOTEL = "Hotels"
    REVIEW = "Reviews"
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, HotelDetailsItem):
            self.db[self.HOTEL].insert_one(dict(item))
        elif isinstance(item, HotelReviewItem):
            self.db[self.REVIEW].insert_one(dict(item))
            
        return item
    

class HotelReviewsPipeline:
    def open_spider(self, spider):
        self.filelog = open(f"log_{city}.json", "w", encoding = 'utf-8')
        self.file1 = open(f"hotels_{city}_v1.json", "w", encoding = 'utf-8')
        self.file2 = open(f"reviews_{city}_v1.json", "w", encoding = 'utf-8')

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()
        self.filelog.close()

    def process_item(self, item, spider):
        if isinstance(item, HotelDetailsItem):
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file1.write(line)
        elif isinstance(item, HotelReviewItem):
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file2.write(line)
        else:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.filelog.write(line)
            
        return item

    def decode_vietnamese(self, item):
        for field_name in item.fields:
            field_value = item[field_name]
            if isinstance(field_value, str):
                decoded_value = field_value.encode().decode("unicode_escape")
                item[field_name] = decoded_value
                
        return item
