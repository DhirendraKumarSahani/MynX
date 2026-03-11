"""
Memory Manager

Handles conversation memory for the AI agent.
Supports thread-based sessions and future persistence.
"""

import logging

from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Production Memory Manager
    """

    def __init__(self):

        logger.info("Initializing Memory Manager")

        # In-memory checkpoint storage
        self.memory = MemorySaver()

    def get_memory(self):
        """
        Return memory instance for agent
        """

        return self.memory


# Global singleton instance
memory_manager = MemoryManager()


def get_memory():
    """
    Access global memory instance
    """

    return memory_manager.get_memory()