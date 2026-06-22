"""
AI integration service: wraps calls to the Groq chat-completions API.
"""

import logging

import httpx

from app.config import AI_MODEL, GROQ_API_KEY, GROQ_API_URL, REQUEST_TIMEOUT
from app.data.texts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


async def ask_ai(history: list[dict], user_message: str, system: str = SYSTEM_PROMPT) -> str:
    """Send a chat-completion request to Groq and return the assistant's reply.

    Args:
        history: Prior conversation turns as a list of
            {"role": "user"|"assistant", "content": str} dicts.
        user_message: The newest user message to append to the conversation.
        system: System prompt defining the assistant's persona/behavior.

    Returns:
        The assistant's text reply, or a user-friendly error message if the
        request failed (timeout, HTTP error, or other connection issue).
    """
    messages = [{"role": "system", "content": system}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except httpx.TimeoutException:
        return "⏳ Took too long, try again!"
    except httpx.HTTPStatusError as e:
        logger.error("Groq error %s: %s", e.response.status_code, e.response.text)
        return "⚠️ AI error. Try again in a moment."
    except Exception as e:
        logger.error("Error: %s", e)
        return "🔌 Connection issue. Please try again."
