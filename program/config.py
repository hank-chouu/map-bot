from dotenv import load_dotenv
import os


load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
MAP_API_KEY = os.getenv('MAP_API_KEY')
MONGO_URL = os.getenv('MONGO_URL')

