from urllib.parse import quote
import sqlite3
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import (
    SHRINKPE_API_KEY,
    RENDER_URL,
    DATABASE_NAME,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO users(user_id,status)
            VALUES(?, 'started')
            """,
            (user_id,),
        )
        conn.commit()

    verify_url = f"{RENDER_URL}/verify?user_id={user_id}"

    try:
        response = requests.get(
            f"https://shrink.pe/api?api={SHRINKPE_API_KEY}&url={quote(verify_url)}",
            timeout=20,
        )

        data = response.json()

        short_url = data.get("shortenedUrl", verify_url)

    except Exception:
        short_url = verify_url

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Get 24-Hour Pass",
                url=short_url,
            )
        ]
    ]

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Click the button below to verify your access.\n\n"
        "⚠️ The Join Channel button will appear only after verification.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
