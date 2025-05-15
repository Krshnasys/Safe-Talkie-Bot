# Group Manager Bot

A Telegram bot for managing group chats, filtering abusive language, and handling URLs, with commands for user and chat information.

## Features
- Filters messages containing abusive words or URLs in authorized groups.
- Commands: `/start`, `/info`, `/id` (private and group chats).
- Rate limiting to prevent abuse.
- Memory monitoring with graceful shutdown.
- Metrics tracking for messages, errors, and deletions.
- Configurable via `config.json`.

## Setup
1. Clone the repository:
