import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import Headline

class FarmingNewsPipeline:
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not Headline.objects.filter(headline=item['headline']).exists():
            Headline.objects.create(headline=item['headline'])
        return item
