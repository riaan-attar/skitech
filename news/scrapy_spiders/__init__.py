# news/scrapy_spiders/__init__.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skitech.settings')
django.setup()
