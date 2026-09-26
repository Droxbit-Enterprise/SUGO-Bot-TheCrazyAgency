import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
URL_STATIC= "https://panel.thecrazyagency.com/static/"