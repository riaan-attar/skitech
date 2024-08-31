import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class FarmingSpider(scrapy.Spider):
    name = 'farming'
    allowed_domains = ['business-standard.com']
    start_urls = ['https://www.business-standard.com/search/news/keywords/farming']

    def parse(self, response):
        headlines = response.xpath('//h2/text()').extract()
        for headline in headlines:
            yield {'headline': headline}

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FarmingSpider)
    process.start()