import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv('.env')

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_URL = os.path.join(BASE_DIR, 'images')

vk_api_token = os.getenv("TOKEN")
group_id = os.getenv('GROUP_ID')
test_data = os.getenv('TEST_DATA')
DB_URL = os.getenv('DB_URL')
