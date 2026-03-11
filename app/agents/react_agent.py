"""
ReAct Agent Module

Responsible for:
- registering tools
- initializing agent
- attaching memory
- running reasoning loop
"""

import logging

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from app.models.llm_model import LLMService
from app.tools.tool_registry import ToolRegistry
from app.memory.memory_manager import get_memory


logger = logging.getLogger(__name__)


class ReactAgentBuilder:
    """
    Production-ready ReAct Agent Builder
    """

    def __init__(self):

        logger.info("Initializing ReAct Agent")

        SYSTEM_PROMPT = """
        You are MYNX — a professional AI Assistant designed for speed, intelligence, and creativity.

        Return the final response only.
        Do not output intermediate reasoning steps.

        Your goal is to provide clear, structured, and professional answers that are easy to read and useful for learning and problem solving.

        RESPONSE GUIDELINES

        Always follow these formatting rules:

        1. Use clean Markdown formatting.
        2. Use headings when explaining topics.
        3. Use numbered lists or bullet points when listing concepts.
        4. Use code blocks when writing code.
        5. Use examples when explaining technical topics.
        6. Keep explanations concise but informative.
        7. Avoid unnecessary repetition.

        NUMBERED LIST FORMAT

        Always format numbered lists like this:

        1. Learning from Data
        2. Types of Machine Learning
        3. Applications of Machine Learning

        Never break numbering like this:

        1.
        Learning from Data

        CODE FORMAT

        When writing code always use proper markdown code blocks.

        Example:

        ```python
        print("Hello World")
        """

        # Initialize LLM
        self.llm_service = LLMService()

        # Load tools
        self.tools = ToolRegistry.get_tools()

        # Load memory
        self.memory = get_memory()

        # Create agent
        self.agent = create_react_agent(
            model=self.llm_service.llm,
            tools=self.tools,
            checkpointer=self.memory,
            prompt=SYSTEM_PROMPT,
        )

    def run(self, query: str, thread_id: str = "default"):
        """
        Execute agent with reasoning loop
        """

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = self.agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            config=config
        )

        return result