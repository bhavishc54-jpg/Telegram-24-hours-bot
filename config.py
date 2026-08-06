import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
INVITE_LINK = os.getenv("INVITE_LINK", "")
SHRINKPE_API_KEY = os.getenv("SHRINKPE_API_KEY", "")
RENDER_URL = os.getenv("RENDER_URL", "http://127.0.0.1:8080")

DATABASE_NAME = "bot_database.db"

LOG_LEVEL = "INFO"
