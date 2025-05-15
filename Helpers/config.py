import json
import os
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class Config:
    schema = {
        "type": "object",
        "properties": {
            "telegram_api_id": {"type": "string"},
            "telegram_api_hash": {"type": "string"},
            "telegram_bot_token": {"type": "string"},
            "DELETE_URLS": {"type": "boolean"},
            "ADMINS": {"type": "array", "items": {"type": "integer"}},
            "USE_AUTH": {"type": "boolean"},
            "AUTH_GROUPS": {"type": "array", "items": {"type": "integer"}},
            "MEMORY_THRESHOLD": {"type": "number", "minimum": 100},
            "MESSAGE_RATE_LIMIT": {"type": "number", "minimum": 10}
        },
        "required": ["telegram_api_id", "telegram_api_hash", "telegram_bot_token"]
    }

    def __init__(self):
        self.data = self._load_config()
        validate(instance=self.data, schema=self.schema)
        self.telegram_api_id = self.data["telegram_api_id"]
        self.telegram_api_hash = self.data["telegram_api_hash"]
        self.telegram_bot_token = self.data["telegram_bot_token"]
        self.delete_urls = self.data.get("DELETE_URLS", False)
        self.admins = self.data.get("ADMINS", [])
        self.use_auth = self.data.get("USE_AUTH", False)
        self.auth_groups = self.data.get("AUTH_GROUPS", [])
        self.memory_threshold = self.data.get("MEMORY_THRESHOLD", 450)
        self.message_rate_limit = self.data.get("MESSAGE_RATE_LIMIT", 100)

    def _load_config(self):
        config_file = os.getenv("CONFIG_FILE", "config.json")
        try:
            with open(config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {config_file}")
            raise
        except KeyError as e:
            logger.error(f"Missing key in {config_file}: {e}")
            raise
        except ValidationError as e:
            logger.error(f"Config validation failed: {e.message}")
            raise

    def load_bad_words(self):
        try:
            with open("bad_words.txt", "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file if line.strip()]
        except FileNotFoundError:
            logger.warning("bad_words.txt not found, using empty bad words list")
            return []
        except UnicodeDecodeError:
            logger.error("Encoding error in bad_words.txt")
            raise

def load_config():
    return Config()
