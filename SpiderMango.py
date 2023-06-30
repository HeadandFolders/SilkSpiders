import scrapy
from shutil import which
from scrapy_selenium import SeleniumRequest
#from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
# this is from realpython.com/Webscrapingwithpython&MongoDB

class Product(scrapy.Item):
	product_name = scrapy.Field()
	price = scrapy.Field()
	link = scrapy.Field()
	img_src = scrapy.Field()

class ClothesMango(CrawlSpider):
	name = "clothesmango"
	ROBOTSTXT_OBEY = True
	HTTPCACHE_ENABLED = True
	CONCURRENT_REQUESTS_PER_DOMAIN = 16
	DOWNLOAD_DELAY = 10.0
	SELENIUM_DRIVER_NAME = 'chrome'
	SELENIUM_DRIVER_EXECUTABLE_PATH = which('C:/Users/ItsJa/.wdm/drivers/chromedriver/win32/96.0.4664.45/driver/chromedriver.exe')
	SELENIUM_DRIVER_ARGUMENTS=['--headless']
	DOWNLOADER_MIDDLEWARES = {
		'scrapy_selenium.SeleniumMiddleware': 800
	}
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
	}
	def start_requests(self):
		yield SeleniumRequest(
			url = "https://shop.mango.com/us/women/jackets-and-suit-jackets_c16573202",
			wait_time = 3,
			#screenshot = True,
			callback = self.parse_item,
			dont_filter = True
		)

	def parse_item(self, response):
		self.logger.info('Hi, this is an item page! %s', response.text)
		print("procesing:"+response.url)
		#Extract data using css selectors
		product_name = response.css('div.ql2j2 > div.UznSa> span::text').extract()
		price=response.css('div.ql2j2 > div.prices-container Mc_iY > span::text').extract()
		#Extract data using xpath
		img_src=response.css('div.swiper-wrapper > div.swiper-slide.swiper-no-swiping.swiper-slide-active > img::attr(src)').extract()
		print(len(img_src))
		
		