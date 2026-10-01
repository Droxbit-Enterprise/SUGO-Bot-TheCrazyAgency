import os
from dotenv import load_dotenv
load_dotenv()
DJANGO_TOKEN = os.getenv("DJANGO_TOKEN")
TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
URL_STATIC = os.getenv("URL_STATIC")
URL_MEDIA = os.getenv("URL_MEDIA")
BASE_URL = os.getenv("BASE_URL")
BOT_NAME = os.getenv("BOT_NAME")
ORIGIN_BOT = os.getenv("ORIGIN_BOT")