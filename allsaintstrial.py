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
	colors = scrapy.Field()
	img_src = scrapy.Field()

class ClothesAllSaints(CrawlSpider):
	name = "clothesallsaints"
	ROBOTSTXT_OBEY = True
	HTTPCACHE_ENABLED = True
	CONCURRENT_REQUESTS_PER_DOMAIN = 16
	DOWNLOAD_DELAY = 10.0
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
	}
	allowed_domains = ["allsaints.com"]
	start_urls = [
		'https://www.allsaints.com/women/sweatshirts-and-hoodies/',
		'https://www.allsaints.com/men/sweatshirts-and-hoodies/',
	]
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)

	def start_requests(self): 
			for url in self.start_urls: 
				yield SplashRequest(url, self.parse_item, 
					endpoint='render.json', 
					args={'wait': 0.5}, 
				)
	def parse_item(self, response):
		#self.logger.info('Hi, this is an item page! %s', response.text)
		print("procesing:"+response.url)
		#Extract data using css selectors
		product_name=response.xpath('//div[@class="product-item__info__inner"]/div[1]/span[1]/span[2]/text()').get()
		price=response.xpath('//div[@class="product-item__info__inner"]/div[1]/span[2]/text()').get()
		#Extract data using xpath
		link=response.xpath('//div[@class="product-item__photos-container"]/a/@href').get()
		#company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()
		#colors=response.css('a.colour-swatches__swatch > img::attr(alt)').extract()
		img_src=response.xpath('//div[@class="product-item__photo next-carousel__item next-carousel__item--current"]/picture[1]/img/@src').get()
		print(img_src)

"""
		row_data=zip(product_name,price,link,img_src)

		#Making extracted data row wise
		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info={
				#key:value
				'page':response.url,
				'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
				'price' : item[1],
				'link' : item[2],
				'img_src' : item[3],
			}

			#yield or give the scraped info to scrapy
			yield scraped_info
"""