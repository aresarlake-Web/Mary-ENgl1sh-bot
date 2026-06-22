# 📚 Mary English — Group Manager Bot

A Telegram bot that welcomes new group members and teaches English using
an AI-powered teacher persona ("Mary"), backed by Groq's `llama-3.3-70b-versatile`
model.

## Features

- 👋 **Welcome system** — greets new group members and asks for their English level
  (Beginner / Intermediate / Advanced) via inline buttons.
- 🧠 **AI teacher** — answers grammar/vocabulary questions, corrects mistakes kindly,
  and keeps replies concise and engaging.
- 💾 **Conversation memory** — keeps the last 20 messages of context per user
  (private chats) and per group (shared group chats).
- 📝 **Quizzes** — `/quiz` posts a random multiple-choice grammar question;
  answering `a`, `b`, or `c` in the group checks it automatically.
- 📖 **Lessons, words, tips, text checking** — `/lesson`, `/word`, `/tip`, `/check`.
- 💬 **Smart group triggers** — responds when mentioned (`@botname`), replied to,
  or addressed by name ("Alex ...").

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

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets**

   Copy the example env file and fill in your real values:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

   - Get a Telegram bot token from [@BotFather](https://t.me/BotFather).
   - Get a Groq API key from the [Groq Console](https://console.groq.com/keys).

3. **Run the bot**

   ```bash
   python main.py
   ```

## Using the Bot

### Commands

| Command   | Description                                  |
|-----------|-----------------------------------------------|
| `/start`  | Intro message                                  |
| `/help`   | Show all commands                              |
| `/quiz`   | Random grammar quiz (answer with `a`/`b`/`c`)  |
| `/lesson` | A short English lesson on a random topic       |
| `/word`   | Word of the day with examples                  |
| `/check`  | Check text for errors, e.g. `/check I goes to school` |
| `/tip`    | A quick grammar tip                            |
| `/reset`  | Clear your/the group's conversation memory     |

### In a group

1. Add the bot to your group.
2. Make it an **admin** (required for the welcome-member event to fire).
3. Tag it (`@YourBotUsername`), reply to one of its messages, or start your
   message with "Alex" to get a response.

### In a private chat

Just send a message — every message gets an AI reply with conversation context.

## Notes on Architecture

- Conversation memory and active quizzes are stored **in-process, in memory**
  (matching the original bot's behavior). They reset when the bot restarts and
  are not shared across multiple bot instances/processes.
- All secrets are loaded from environment variables via `python-dotenv`;
  none are hardcoded in source. `main.py` validates that required variables
  are present before starting and exits with a clear error if they're missing.
