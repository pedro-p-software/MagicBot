"""Magic Island Robotics' Telegram bot entry point."""

import logging
import time

import telebot

from config import Settings
from handlers import register_handlers
from rag import TeamKnowledgeBase


def main() -> None:
    settings = Settings.from_environment()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    bot = telebot.TeleBot(settings.telegram_bot_token)
    knowledge_base = TeamKnowledgeBase(settings)
    knowledge_base.build_or_load()

    # Telegram provides the authoritative username, avoiding a stale hard-coded name.
    try:
        bot_username = bot.get_me().username
    except Exception:
        logging.getLogger(__name__).warning("Could not retrieve the bot username; using BOT_USERNAME fallback.")
        bot_username = settings.bot_username

    register_handlers(bot, knowledge_base, settings, bot_username)
    logging.info("Bot is listening for messages.")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception:
            logging.exception("Polling failed; retrying in 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    main()
