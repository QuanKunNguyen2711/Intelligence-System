# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from googletrans import Translator
from scrapy import signals
import pymongo

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy_auto_trans.spidermiddlewares.autotrans import AutoTranslationMiddlewareBase
import scrapy
import types
from . import exceptions as excs
from urllib.parse import quote as urlquote, unquote as urlunquote
import requests
import json
import logging

class HotelReviewsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class HotelReviewsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# translator = Translator(service_urls=['translate.google.com'])

class MyTranslationMiddleware(AutoTranslationMiddlewareBase):
    def translate(self, field_name, item, **kwargs):
        source_field_name = kwargs['source']
        source_language = item.get(source_field_name+"_lang")
        target_field_name = field_name
        target_field = item.fields[target_field_name]
        item_source = item.get(source_field_name)
        if source_language != "vi":
            # return translator.translate(item_source, dest=target_field['language']).text
            res = self.language_translate(source_language, target_field['language'], item_source if item_source else '')
            print(res)
            return res
        
        return item_source if item_source else ''
        
    def language_translate(self, source_lang_code, target_lang_code, text):
        return scrapy.Request(
            url = self.get_translate_url( source_lang_code, target_lang_code, text)
        ), self.get_translate_result
    
    def get_translate_url(self, source_lang_code, target_lang_code, text, **kwargs):
        quoted_text = urlquote(text.encode('utf8'))
        key = self.get_api_key()
        return \
            'https://translation.googleapis.com/language/translate/v2?key={key}' \
            '&q={quoted_text}' \
            '&target={target_lang_code}' \
            '&source={source_lang_code}'.format(
                key=key, 
                quoted_text=quoted_text, 
                target_lang_code=target_lang_code, 
                source_lang_code=source_lang_code
            )

    def get_translate_result(self, response, field_name, item, **kwargs):
        return urlunquote(json.loads(response.text)['data']['translations'][0]['translatedText'])

    def get_api_key(self):
        if hasattr(self, 'api_key') and bool(self.api_key):
            return self.api_key

        key = self.settings.get('GOOGLE_CLOUD_API_KEY')
        if key:
            return key
        
        

