# ============================================================
# Telegram24hBot V2
# File: admin.py
# Version: 2.0.0
# ============================================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import ContextTypes

from config import OWNER_ID


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update.effective_user.id):
        return

    keyboard = [

        [
            InlineKeyboardButton(
                "? Add Promotion",
                callback_data="promotion_add",
            )
        ],

        [
            InlineKeyboardButton(
                "?? Statistics",
                callback_data="statistics",
            )
        ],

        [
            InlineKeyboardButton(
                "?? Active Promotions",
                callback_data="promotion_active",
            )
        ],

        [
            InlineKeyboardButton(
                "? Remove Promotion",
                callback_data="promotion_remove",
            )
        ],

        [
            InlineKeyboardButton(
                "?? Broadcast",
                callback_data="broadcast",
            )
        ],

        [
            InlineKeyboardButton(
                "?? Settings",
                callback_data="settings",
            )
        ],

    ]

    await update.message.reply_text(
        "??? **Admin Panel**\n\nChoose an option below.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
