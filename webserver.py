import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask, request
import sqlite3
import requests

from config import BOT_TOKEN, INVITE_LINK, DATABASE_NAME

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is Running ✅"

@app.route("/verify")
def verify():

    user_id = request.args.get("user_id")

    logging.info(f"/verify called for user_id={user_id}")

    if not user_id:
        return "Missing user_id", 400

    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()

        cur.execute("SELECT status FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()

        logging.info(f"Current status: {row}")

        if row and row[0] in ("verified", "joined"):
            logging.info("Already verified - skipping sendMessage")
            return "<h2>Already Verified ✅</h2>"

        cur.execute(
            "UPDATE users SET status='verified', verify_time=CURRENT_TIMESTAMP WHERE user_id=?",
            (user_id,),
        )
        conn.commit()

    logging.info("Sending Telegram message...")

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": user_id,
            "text": "🎉 Verification Successful!\n\nClick below to join the channel.",
            "reply_markup": {
                "inline_keyboard": [[
                    {
                        "text": "🔑 Join Channel",
                        "url": INVITE_LINK
                    }
                ]]
            }
        },
        timeout=20,
    )

    logging.info("Telegram message sent.")

    return "<h2>Verification Successful ✅</h2>"

def run_webserver():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)
