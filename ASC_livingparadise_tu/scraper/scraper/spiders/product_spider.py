from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.scraper.items import ScraperItem

from scrapy.spiders import CrawlSpider


class ProductSpider(CrawlSpider):
    name = 'crawl_shop'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    rules = (
        Rule(LinkExtractor(allow=r'page/.*'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = ScraperItem()
        print("===========+++++++++============== 53223525 ----------")
        print(response.url)
        item['body'] = response.xpath('//span[has-class("text")]/text()').get()
        item['name'] = response.xpath('//small[has-class("author")]/text()').get()
        yield item
