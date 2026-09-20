"""Telegram command and message handlers."""

from __future__ import annotations

import logging
from pathlib import Path

import telebot

from config import Settings
from rag import TeamKnowledgeBase
from text_utils import split_message


LOGGER = logging.getLogger(__name__)
def register_handlers(bot: telebot.TeleBot, knowledge_base: TeamKnowledgeBase, settings: Settings, bot_username: str | None) -> None:
    @bot.message_handler(commands=["start", "help"])
    def send_help(message):
        bot.reply_to(message, "Olá! Posso responder usando os documentos oficiais da Magic Island Robotics.\n\nComandos: /agenda, /links, /onboarding, /ask <pergunta>, /help\n\nNo privado, envie sua pergunta normalmente. Em grupos, use /ask ou me marque.")

    @bot.message_handler(commands=["agenda", "links", "onboarding"])
    def send_reference(message):
        command = message.text.split()[0].split("@")[0][1:]
        file_map = {"agenda": "team/calendar.md", "links": "team/quick_links.md", "onboarding": "team/onboarding.md"}
        bot.reply_to(message, read_reference(settings.knowledge_dir / file_map[command]))

    @bot.message_handler(commands=["ask"])
    def ask_command(message):
        question = message.text.partition(" ")[2].strip()
        if not question:
            bot.reply_to(message, "Use /ask seguido da sua pergunta. Ex.: /ask Quando é a próxima reunião?")
            return
        reply_to_question(bot, message, knowledge_base, question)

    @bot.message_handler(content_types=["text"], func=lambda _message: True)
    def answer_message(message):
        text = (message.text or "").strip()
        if message.chat.type == "private":
            reply_to_question(bot, message, knowledge_base, text)
        elif bot_username and f"@{bot_username.lower()}" in text.lower():
            question = text.replace(f"@{bot_username}", "").strip()
            if question:
                reply_to_question(bot, message, knowledge_base, question)


def read_reference(path: Path) -> str:
    if not path.exists():
        return "Esse conteúdo ainda não foi configurado. Avise um responsável."
    return path.read_text(encoding="utf-8").strip()


def reply_to_question(bot: telebot.TeleBot, message, knowledge_base: TeamKnowledgeBase, question: str) -> None:
    bot.send_chat_action(message.chat.id, "typing")
    try:
        answer, sources = knowledge_base.answer(question)
        if sources:
            answer += "\n\nFonte(s): " + ", ".join(sources)
        for part in split_message(answer):
            bot.reply_to(message, part)
    except Exception:
        LOGGER.exception("Could not answer a Telegram message")
        bot.reply_to(message, "Não consegui responder agora. Confirme se o LM Studio está em execução e tente novamente.")

