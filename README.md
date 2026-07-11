# 📚 Mary English — Group Manager Bot

A Telegram bot that welcomes new group members and teaches English using
an AI-powered teacher persona ("Mary"), backed by OpenRouter's `Qwen And Deepseek`
model.

## Features

- **Welcome system** — greets new group members and asks for their English level
  (Beginner / Intermediate / Advanced) via inline buttons.
- **AI teacher** — answers grammar/vocabulary questions, corrects mistakes kindly,
  and keeps replies concise and engaging.
-  **Conversation memory** — keeps the last 20 messages of context per user
  (private chats) and per group (shared group chats).
- **Quizzes** — `/quiz` posts a random multiple-choice grammar question;
  answering `a`, `b`, or `c` in the group checks it automatically.
- **Lessons, words, tips, text checking** — `/lesson`, `/word`, `/tip`, `/check`.
- **Smart group triggers** — responds when mentioned (`@Mary_Engl1sh_Bot`), replied to,
  or addressed by name ("Mary ...").

## Project Structure

```
project/
├── app/
│   ├── handlers/
│   │   ├── commands.py      # /start, /help, /quiz, /lesson, /word, /check, /tip, /reset
│   │   ├── messages.py      # free-text message handling (private + group)
│   │   └── members.py       # welcome new members + level selection callback
│   │
│   ├── services/
│   │   ├── ai_service.py     # Groq chat-completion API wrapper
│   │   ├── memory_service.py # per-user / per-group conversation memory
│   │   └── quiz_service.py   # active quiz state + answer checking
│   │
│   ├── data/
│   │   ├── quizzes.py        # static quiz question bank
│   │   └── texts.py          # system prompt, welcome messages, static copy
│   │
│   ├── keyboards/
│   │   └── welcome_keyboard.py  # inline keyboard for level selection
│   │
│   └── config.py             # env-based configuration + logging setup
│
├── main.py                   # entry point — builds the Application and runs polling
├── requirements.txt
├── .env.example
└── README.md
```

