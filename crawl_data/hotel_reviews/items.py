# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_auto_trans import FailureAction

class HotelDetailsItem(scrapy.Item):
    hotel_id = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    avg_score = scrapy.Field()
    total_reviews = scrapy.Field()
    
class HotelReviewItem(scrapy.Item):
    name = scrapy.Field()
    hotel = scrapy.Field()
    country = scrapy.Field()
    title = scrapy.Field()
    pos_rw = scrapy.Field()
    neg_rw = scrapy.Field()
    # lang
    title_lang = scrapy.Field()
    pos_rw_lang = scrapy.Field()
    neg_rw_lang = scrapy.Field()
    # translated
    # title_vi = scrapy.Field(auto_translate=True, source="title", language="vi")
    # pos_rw_vi = scrapy.Field(auto_translate=True, source="pos_rw", language="vi")
    # neg_rw_vi = scrapy.Field(auto_translate=True, source="neg_rw", language="vi")
    avg_score = scrapy.Field()
    room = scrapy.Field()
    booking_date = scrapy.Field()
    review_date = scrapy.Field()
    