#FAILLLLLLL 
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
# this is from realpython.com/Webscrapingwithpython&MongoDB

class Product(scrapy.Item):
	product_name = scrapy.Field()
	price = scrapy.Field()
	link = scrapy.Field()

class ClothesBershkaSpider(CrawlSpider):
	name = "clothesbershka"
	ROBOTSTXT_OBEY = True
	HTTPCACHE_ENABLED = True
	CONCURRENT_REQUESTS_PER_DOMAIN = 16
	DOWNLOAD_DELAY = 10.0
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
	}
	allowed_domains = ["bershka.com"]
	start_urls = [
		'https://www.bershka.com/qa/women/clothes/t-shirts-c1010193217.html',
		#'https://www.bershka.com/qa/women/clothes/jackets-and-coats-c1010193212.html',
	]
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)

	def start_requests(self): 
		for url in self.start_urls: 
				yield SplashRequest(url, self.parse_item, 
					endpoint='render.html', 
					args={'wait': 0.5}, 
				)
		
	def parse_item(self, response):

		#self.logger.info('Hi, this is an item page! %s', response.text)
		print("procesing:"+response.url)
		print("WOWOWOWWWWWWWWWWWWWWWWWWWWWWWWWWSOOOOOOOOOOOOOOOCOLLLLLLLLLLLLLLLLLLLLL")
		pdt_img = response.css('div.product-image > div.product-media-wrapper > span > img').extract()
		#Extract data using css selectors
		product_name=response.css('div.product-content > div > div > div.product-text > p:first-of-type::text').extract()
		price=response.css('div.product-content > div > div > div.price-elem.price-grid > span').extract()
		#img_link = response.css('#main-content > div > div > div.sticky-body > section.category-grid.full-container > div > ul > li:nth-child(2) > div > a > div > div.product-image > div.product-media-wrapper > span > img')
		#Extract data using xpath
		link=response.css("section.category-grid.full-container > div > ul > li:nth-child(3) > div > a::attr(href)").extract()
		#company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()

		row_data=zip(pdt_img,product_name,price,link)

		#Making extracted data row wise
		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info = {
				#key:value
				'page':response.url,
				'product_image': item[0],
				'product_name' : item[1], #item[0] means product in the list and so on, index tells what value to assign
				'price' : item[2],
				'link' : item[3],
			}
			

			#yield or give the scraped info to scrapy
			yield scraped_info
			