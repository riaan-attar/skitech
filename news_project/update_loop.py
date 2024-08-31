import time
import subprocess

while True:
    subprocess.call(['python', 'news/update_news.py'])
    time.sleep(1800)  # Sleep for 30 minutes
