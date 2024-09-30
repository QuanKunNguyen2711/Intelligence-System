# Scrapy settings for hotel_reviews project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "hotel_reviews"

SPIDER_MODULES = ["hotel_reviews.spiders"]
NEWSPIDER_MODULE = "hotel_reviews.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "hotel_reviews (+http://www.yourdomain.com)"
JOBDIR = 'keep'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1000

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'hotel_booking_com'
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
# #    "hotel_reviews.middlewares.HotelReviewsSpiderMiddleware": 543,
#     # 'scrapy_auto_trans.spidermiddlewares.autotrans.GoogleAutoTranslationMiddleware': 701,
#     'hotel_reviews.middlewares.MyTranslationMiddleware': 701
# }

GOOGLE_CLOUD_API_KEY="AIzaSyCtGzaYZPUeA48_zJv9aubB8ttpPdspHwk"

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "hotel_reviews.middlewares.HotelReviewsDownloaderMiddleware": 543,
# }
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
    # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    # "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "hotel_reviews.pipelines.DataCleaningPipeline": 300,
   "hotel_reviews.pipelines.HotelReviewsPipeline": 400,
    # "hotel_reviews.pipelines.MongodbPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# ROTATING_PROXY_LIST = [
# "mrudjhia:bn3jr3vobz9w@38.154.227.167:5868",
# "mrudjhia:bn3jr3vobz9w@185.199.229.156:7492",
# "mrudjhia:bn3jr3vobz9w@185.199.228.220:7300",
# "mrudjhia:bn3jr3vobz9w@185.199.231.45:8382",
# "mrudjhia:bn3jr3vobz9w@188.74.210.207:6286",
# "mrudjhia:bn3jr3vobz9w@188.74.183.10:8279",
# "mrudjhia:bn3jr3vobz9w@188.74.210.21:6100",
# "mrudjhia:bn3jr3vobz9w@45.155.68.129:8133",
# "mrudjhia:bn3jr3vobz9w@154.95.36.199:6893",
# "mrudjhia:bn3jr3vobz9w@45.94.47.66:8110"

# ]
