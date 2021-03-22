import scrapy

from scrapy.loader import ItemLoader

from ..items import DwpbankdeItem
from itemloaders.processors import TakeFirst


class DwpbankdeSpider(scrapy.Spider):
	name = 'dwpbankde'
	start_urls = ['https://www.dwpbank.de/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="retinaiconbox"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2//text()[normalize-space()]').get()
		description = response.xpath('//div[@class="post-excerpt"]//text()[normalize-space()]|//div[@class="entry"]//text()[normalize-space() and not(ancestor::h2 | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="meta-date"]/time/text()').get()

		item = ItemLoader(item=DwpbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
