# """
# Memory Manager

# Handles conversation memory for the AI agent.
# Supports thread-based sessions and future persistence.
# """

# import logging

# from langgraph.checkpoint.memory import MemorySaver

# logger = logging.getLogger(__name__)


# class MemoryManager:
#     """
#     Production Memory Manager
#     """

#     def __init__(self):

#         logger.info("Initializing Memory Manager")

#         # In-memory checkpoint storage
#         self.memory = MemorySaver()

#     def get_memory(self):
#         """
#         Return memory instance for agent
#         """

#         return self.memory


# # Global singleton instance
# memory_manager = MemoryManager()


# def get_memory():
#     """
#     Access global memory instance
#     """

#     return memory_manager.get_memory()



"""
Memory Manager

Handles conversation memory for the AI agent.
Supports thread-based sessions with LIMITED history (production safe).
"""

import logging
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)


class LimitedMemorySaver(MemorySaver):
    """
    MemorySaver with message limit (prevents token overflow)
    """

    MAX_MESSAGES = 6   # ✅ Safe limit (5–8 recommended)

    def put(self, config, checkpoint, metadata, new_versions):
        try:
            # ✅ Limit stored messages
            if "messages" in checkpoint:
                checkpoint["messages"] = checkpoint["messages"][-self.MAX_MESSAGES:]

            return super().put(config, checkpoint, metadata, new_versions)

        except Exception as e:
            logger.error(f"Memory limit error: {str(e)}")
            return super().put(config, checkpoint, metadata, new_versions)


class MemoryManager:
    """
    Production Memory Manager
    """

    def __init__(self):
        logger.info("Initializing Limited Memory Manager")

        # ✅ USE LIMITED MEMORY (IMPORTANT CHANGE)
        self.memory = LimitedMemorySaver()

    def get_memory(self):
        """
        Return memory instance for agent
        """
        return self.memory


# Global singleton
memory_manager = MemoryManager()


def get_memory():
    """
    Access global memory instance
    """
    return memory_manager.get_memory()