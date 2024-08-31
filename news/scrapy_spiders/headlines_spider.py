# news/scrapy_spiders/headlines_spider.py

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime

from news.models import Headline

class HeadlinesSpider(scrapy.Spider):
    name = "headlines"
    allowed_domains = ["business-standard.com"]
    start_urls = [
        'https://www.business-standard.com/industry/agriculture'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    def parse(self, response):
        articles = response.css('div.card')  # Adjust selector based on actual website structure
        for article in articles:
            title = article.css('h2 a::text').get()
            url = response.urljoin(article.css('h2 a::attr(href)').get())
            published_at_str = article.css('span.date::text').get()
            published_at = datetime.strptime(published_at_str, '%d %b %Y')  # Adjust date format accordingly

            # Save to database
            Headline.objects.get_or_create(
                title=title,
                url=url,
                published_at=published_at
            )

            yield {
                'title': title,
                'url': url,
                'published_at': published_at_str
            }
