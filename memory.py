"""
Conversation Memory — AuraAI
Author: Abhay Sharma | github.com/KAZURIKAFU
LangChain-style sliding window conversation memory
"""

from datetime import datetime
from collections import deque


class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.history   = deque(maxlen=max_turns)
        self.metadata  = {
            "created_at":   datetime.now().isoformat(),
            "total_turns":  0,
            "topics_seen":  [],
        }

    def add(self, user_msg: str, ai_response: str):
        """Add a conversation turn to memory."""
        turn = {
            "turn":      self.metadata["total_turns"] + 1,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user":      user_msg,
            "response":  ai_response,
        }
        self.history.append(turn)
        self.metadata["total_turns"] += 1

    def get_context(self, last_n: int = 5) -> list:
        """Return last N conversation turns."""
        history_list = list(self.history)
        return history_list[-last_n:] if len(history_list) >= last_n else history_list

    def get_full_history(self) -> list:
        """Return full conversation history."""
        return list(self.history)

    def clear(self):
        """Clear conversation memory."""
        self.history.clear()
        self.metadata["total_turns"] = 0

    def get_stats(self) -> dict:
        """Return memory statistics."""
        return {
            "total_turns":    self.metadata["total_turns"],
            "window_size":    len(self.history),
            "max_turns":      self.max_turns,
            "session_start":  self.metadata["created_at"],
        }

    def format_for_prompt(self) -> str:
        """Format recent history as context string."""
        context = self.get_context(3)
        if not context:
            return ""
        lines = []
        for turn in context:
            lines.append(f"User: {turn['user']}")
            lines.append(f"AI: {turn['response'][:100]}...")
        return "\n".join(lines)
