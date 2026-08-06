import threading

from telegram.ext import (
    Application,
    CommandHandler,
    ChatJoinRequestHandler,
)

from config import BOT_TOKEN, LOG_LEVEL
from database import init_database
from verification import start
from webserver import run_webserver
from scheduler import handle_join_request
from admin import admin_panel

import logging

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def main():

    init_database()

    threading.Thread(
        target=run_webserver,
        daemon=True
    ).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("✅ Bot Started")

    app.run_polling()

if __name__ == "__main__":
    main()
