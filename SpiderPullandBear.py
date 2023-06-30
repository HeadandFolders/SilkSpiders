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

class ClothesPullandBearSpider(CrawlSpider):
	name = "clothespullandbearb"
	ROBOTSTXT_OBEY = True
	HTTPCACHE_ENABLED = True
	CONCURRENT_REQUESTS_PER_DOMAIN = 16
	DOWNLOAD_DELAY = 15.0
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
	}
	allowed_domains = ["pullandbear.com"]
	start_urls = [
		'https://www.pullandbear.com/lb/woman/clothing/t-shirts/prints-c1030004029.html',
		'https://www.pullandbear.com/lb/woman/clothing/sweatshirts-%26-hoodies-c29018.html',
		'https://www.pullandbear.com/lb/woman/clothing/jackets-c1030009518.html',
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

		print("procesing:"+response.url)
		#Extract data using css selectors
		product_name=response.css('noscript > ul > li > a > img ~ p:first-of-type::text').extract()
		price=response.css('noscript > ul > li > a > img ~ p ~ p::text').extract()
		#Extract data using xpath
		link=response.css("noscript > ul > li > a::attr(href)").extract()
		#company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()

		row_data=zip(product_name,price,link)

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

