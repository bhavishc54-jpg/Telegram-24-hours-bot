# ============================================================
# Telegram24hBot V2
# File: scheduler.py
# Version: 2.0.0
# ============================================================

import sqlite3

from telegram import Update
from telegram.ext import ContextTypes

from config import (
    DATABASE_NAME,
)


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.chat_join_request.from_user.id

    with sqlite3.connect(DATABASE_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status
            FROM users
            WHERE user_id=?
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        if row and row[0] == "verified":

            await update.chat_join_request.approve()

            cursor.execute(
                """
                UPDATE users
                SET
                    status='joined',
                    join_time=CURRENT_TIMESTAMP
                WHERE user_id=?
                """,
                (user_id,),
            )

            conn.commit()

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "?? Welcome!\n\n"
                    "Your join request has been approved.\n\n"
                    "Your 24-hour access has now started."
                ),
            )

        else:

            await update.chat_join_request.decline()

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "? You haven't verified yet.\n\n"
                    "Please send /start and complete verification first."
                ),
            )
