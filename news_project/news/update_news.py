import os
import django
from django.utils import timezone
from datetime import timedelta
from news.models import Headline

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

def update_news():
    # Import the command to run the spider
    from django.core.management import call_command

    now = timezone.now()
    thirty_minutes_ago = now - timedelta(minutes=30)

    # Run the spider to get latest news
    call_command('run_spider')

    # Optional: Implement logic to compare and check if news is updated
    # For simplicity, we will not include it here, as it needs to be handled
    # according to your specific comparison logic.

if __name__ == "__main__":
    update_news()
