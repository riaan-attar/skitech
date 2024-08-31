from django.core.management.base import BaseCommand
from news.spiders.farming_spider import run_spider

class Command(BaseCommand):
    help = 'Run the Scrapy spider to scrape news'

    def handle(self, *args, **kwargs):
        run_spider()
        self.stdout.write(self.style.SUCCESS('Successfully ran the spider'))
