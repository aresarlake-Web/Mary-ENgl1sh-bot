"""
Quiz service: manages active quizzes and answer checking.
"""

import random

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.data.quizzes import QUIZ_BANK

# Active quizzes: { chat_id: { "answer": ..., "explanation": ... } }
_active_quizzes: dict[int, dict] = {}


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pick a random quiz question and post it to the chat."""
    chat_id = update.effective_chat.id

    quiz = random.choice(QUIZ_BANK)
    _active_quizzes[chat_id] = {
        "answer": quiz["answer"],
        "explanation": quiz["explanation"],
    }

    await update.message.reply_text(
        f"📝 *Quiz Time!*\n\n{quiz['question']}\n\nReply with *a*, *b*, or *c*!",
        parse_mode=ParseMode.MARKDOWN,
    )


async def check_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if an incoming message answers an active quiz in this chat.

    Returns:
        True if the message was consumed as a quiz answer (and a reply was
        sent), False otherwise so the caller can continue normal handling.
    """
    chat_id = update.effective_chat.id
    text = update.message.text.strip().lower()

    if chat_id not in _active_quizzes:
        return False

    if text not in ["a", "b", "c"]:
        return False

    quiz = _active_quizzes[chat_id]
    name = update.effective_user.first_name or "friend"

    if text == quiz["answer"]:
        await update.message.reply_text(
            f"🎉 *Correct, {name}!* Well done!\n\n💡 {quiz['explanation']}",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await update.message.reply_text(
            f"Not quite, {name}! The correct answer is *{quiz['answer'].upper()}*.\n\n💡 {quiz['explanation']}",
            parse_mode=ParseMode.MARKDOWN,
        )

    del _active_quizzes[chat_id]
    return True
