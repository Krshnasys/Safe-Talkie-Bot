import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.message_count = 0
        self.error_count = 0
        self.url_deletions = 0
        self.abuse_deletions = 0
        self.memory_usages = []
        self.start_time = None

    def record_bot_start(self):
        self.start_time = datetime.now()
        logger.info(f"Bot started at {self.start_time}")

    def increment_message_count(self):
        self.message_count += 1

    def increment_error_count(self):
        self.error_count += 1

    def increment_url_deletions(self):
        self.url_deletions += 1

    def increment_abuse_deletions(self):
        self.abuse_deletions += 1

    def record_memory_usage(self, usage):
        self.memory_usages.append(usage)
        if len(self.memory_usages) > 100:
            self.memory_usages.pop(0)
