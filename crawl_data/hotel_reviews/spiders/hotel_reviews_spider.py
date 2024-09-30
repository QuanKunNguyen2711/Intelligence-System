import re
import time
import scrapy
from googletrans import Translator
from .enums import DestName
from .constants import DEST_IDS
from hotel_reviews.items import HotelDetailsItem, HotelReviewItem

# translator = Translator(service_urls=['translate.google.com'])
# translator.raise_Exception = True

class HotelReviewsSpiderSpider(scrapy.Spider):
    name = "hotel_reviews_spider"
    allowed_domains = ["booking.com"]
    city = DestName.HCM.value
    dest_id = DEST_IDS.get(city)
    start_urls = [f"https://www.booking.com/searchresults.vi.html?label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEquAEXyAEM2AEB6AEB-AELiAIBqAIDuALo5J-vBsACAdICJDE2NDIyNjllLTJiMTItNGI5ZS1iMWY5LTJkYmIyOTk3Njc2MNgCBuACAQ&sid=ef86872486014d90bf14e50bc6e89d0b&aid=304142&dest_id={dest_id}&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&offset=0"]
    
    page_offset = 25
    count_page = 0
    count_reviews = 0 

    def parse(self, response):
        match_dest = re.search(r"(?<=dest_id=)[\w-]+", response.url)
        match_offset = re.search(r"(?<=offset=)\d+", response.url)
        if match_dest and match_offset:
            current_dest = match_dest.group(0)
            current_offset = match_offset.group(0)
            yield({"start": current_dest, "offset": current_offset})
            
        for hotel_selector in response.css(
            "div.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.c6710787a4"
        ):
            
            hotel_href = hotel_selector.css("h3.aab71f8e4e a.a78ca197d0")
            yield response.follow(
                hotel_href.attrib["href"],
                callback=self.parse_hotel_details,
                meta={"props_data": response.meta.get("props_data", {"city": self.city})},
                # meta={"props_data": {"city": self.city}}
            )

        # Handle pagination
        list_pages = response.css("button.a83ed08757.a2028338ea::text").getall()
        if list_pages:
            last_page = list_pages[len(list_pages)-1]
            last_page = int(last_page)
            if self.count_page < last_page - 1:
                self.count_page += 1
                following_link = response.url
                if match_offset:
                    new_offset = self.count_page*self.page_offset
                    following_link = re.sub(r'(?<=offset=)\d+', str(new_offset), following_link)
                else:
                    following_link += f"&offset={self.count_page*self.page_offset}"

                yield response.follow(
                    following_link,
                    callback=self.parse,
                    # meta={"props_data": response.meta.get("props_data", {"city": self.city})}
                )
                
    def parse_hotel_details(self, response):
        data = response.meta.get("props_data")
        hotel_detail_items = HotelDetailsItem()
        hotel_id = self.parse_hotel_id(response.url)
        
        yield {"hotel": hotel_id}
        
        hotel_detail_items["hotel_id"] = hotel_id
        hotel_detail_items["address"] = response.css("span.hp_address_subtitle::text").get()
        hotel_detail_items["avg_score"] = response.css("div.a3b8729ab1.d86cee9b25::text").get()
        hotel_detail_items["city"] = data.get("city")
        hotel_detail_items["name"] = response.css("h2.d2fee87262.pp-header__title::text").get()
        hotel_detail_items["total_reviews"] = response.css(
            "a[data-testid='Property-Header-Nav-Tab-Trigger-reviews'] span[class='a53cbfa6de']::text"
        ).get()
        # description = response.css("p.a53cbfa6de.b3efd73f69::text").get()
        yield hotel_detail_items

        review_page = "https://www.booking.com/reviewlist.vi.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEquAEXyAEM2AEB6AEB-AELiAIBqAIDuAKo9IuvBsACAdICJGFiZmJhOTZhLTQ2MWEtNDg3Mi1iNGVlLWRlYWVhNzI2OTY4ZNgCBuACAQ&sid=ef86872486014d90bf14e50bc6e89d0b&cc1=vn;dist=1;"
        review_page += f"pagename={hotel_id};type=total" + "&&" + f"offset=0;rows=25"
        yield response.follow(review_page, callback=self.parse_hotel_reviews)
        
        
    def parse_hotel_reviews(self, response):
        match_id = re.search(r"(?<=pagename=)[\w-]+", response.url)
        match_review_offset = re.search(r"(?<=offset=)\d+", response.url)
        if match_id and match_review_offset:
            hotel_id = match_id.group(0)
            current_review_offset = match_review_offset.group(0)
            hotel_review_items = HotelReviewItem()

            yield {"review": hotel_id, "offset": current_review_offset}
            
            for review_block in response.css("li.review_list_new_item_block"):
                hotel_review_items["hotel"] = hotel_id
                hotel_review_items["name"] = review_block.css("span.bui-avatar-block__title::text").get()
                hotel_review_items["country"] = review_block.css("span.bui-avatar-block__subtitle::text").get()
                hotel_review_items["room"] = review_block.css("a.c-review-block__room-link div.bui-list__body::text").get()
                nights_long = review_block.css("ul.c-review-block__stay-date div.bui-list__body::text").get()
                stay_date = review_block.css("ul.c-review-block__stay-date div.bui-list__body span.c-review-block__date::text").get()
                hotel_review_items["booking_date"] = nights_long + " " + stay_date
                hotel_review_items["review_date"] = review_block.css("div.c-review-block__right span.c-review-block__date::text").get()
                hotel_review_items["title_lang"] = review_block.css("div.c-review-block__right h3.c-review-block__title.c-review__title--ltr::attr(lang)").get()
                hotel_review_items["title"] = review_block.css("div.c-review-block__right h3.c-review-block__title.c-review__title--ltr::text").get()
                hotel_review_items["avg_score"] = review_block.css("div.c-review-block__right div.bui-review-score__badge::text").get()        
                
                for review in review_block.css("div.c-review-block__right div.c-review__row"):
                    if review.css("span.bui-u-sr-only::text").get() == "Thích":
                        hotel_review_items["pos_rw_lang"] = review.css("span.c-review__body::attr(lang)").get()
                        hotel_review_items["pos_rw"] = review.css("span.c-review__body::text").get()
                        
                    elif review.css("span.bui-u-sr-only::text").get() == "Không thích":
                        hotel_review_items["neg_rw_lang"] = review.css("span.c-review__body::attr(lang)").get()
                        # if review.css("span.c-review__body::attr(lang)").get() != "vi":
                            # neg_rw = translator.translate(neg_rw, dest='vi').text
                            # time.sleep(0.8)
                        hotel_review_items["neg_rw"] = review.css("span.c-review__body::text").get()

                yield hotel_review_items
            
            next_page = response.css("div.bui-pagination__item.bui-pagination__next-arrow a.pagenext::attr(href)").get()
            if next_page is not None:
                url = "https://www.booking.com" + next_page
                yield response.follow(url, callback=self.parse_hotel_reviews)
            
        
    def parse_hotel_id(self, url: str):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path = parsed_url.path

        splitted_path = path.split("/")
        hotel_str = splitted_path[3]
        if "vi.html" in hotel_str:
            hotel_parts = hotel_str.split(".")
            return hotel_parts[0]
        
