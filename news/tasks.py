# news/tasks.py

from celery import shared_task
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

from news.scrapy_spiders.headlines_spider import HeadlinesSpider

@shared_task
def run_headlines_spider():
    configure_logging()
    runner = CrawlerRunner()
    deferred = runner.crawl(HeadlinesSpider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
