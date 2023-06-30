import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
# this is from realpython.com/Webscrapingwithpython&MongoDB

class ClothesLeftiesSpider(CrawlSpider):
	name = "clotheslefties"
	DOWNLOAD_DELAY = 10.0
	AUTOTHROTTLE_ENABLED = True
	ROBOTSTXT_OBEY = True
	HTTPCACHE_ENABLED = True
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
	}
	allowed_domains = ["lefties.com"]
	start_urls = [
		"https://www.lefties.com/ae/woman/clothing/t-shirts/basic-t-shirts-c1030267507.html"
	]
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)

	def start_requests(self): 
			for url in self.start_urls: 
				yield SplashRequest(url, self.parse_item, 
					endpoint='render.json', 
					args={'wait': 5}, 
			)
		
	def parse_item(self,response):
		#self.logger.info('Hi, this is an item page! %s', response.text)
		names = response.css('noscript > ul > li > a > img::attr(alt)').extract()
		#data-product-2 > div.info-element.future-hidden > div.name
		#data-product-2 > div.info-element.future-hidden > div.product-colors > div.product-color-image.active > img
		price = response.css('noscript > ul > li > a > p ~ p::text').extract()
		#data-product-2 > div.info-element.future-hidden > div.price-wrapper > div > span
		src = response.css('noscript > ul > li > a > img::attr(src)').extract()
		#data-product-2 > div.img-container > img
		#txt = " at {} you'll find {} selling for {} "
		#print(txt.format(src, names, price))

		row_data=zip(names,price,src)

		#Making extracted data row wise
		for item in row_data:
			#create a dictionary to store the scraped info
			scraped_info = {
				#key:value
				'page':response.url,
				'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
				'price' : item[1],
				'link' : item[2],
			}
			

			#yield or give the scraped info to scrapy
			yield scraped_info