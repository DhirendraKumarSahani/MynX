from langchain_groq import ChatGroq
from app.core.config import settings
import logging

from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    Factory class responsible for creating LLM instances.

    This abstraction allows switching between providers
    like Groq, OpenAI, Claude without modifying agent code.
    """

    @staticmethod
    def get_groq_llm():

        try:

            llm = ChatGroq(
                model="qwen/qwen3-32b",
                api_key= settings.GROQ_API_KEY,
                temperature=0.2,
                max_tokens=2200
            )

            logger.info("Groq LLM initialized successfully")

            return llm
        
        except Exception as e:
            logger.error(f"Failed to initialize Groq LLM : {str(e)}")

            raise

class LLMService:
    
    def __init__(self):

        self.llm = LLMFactory.get_groq_llm()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )

    def invoke(self, messages):

        try:

            response = self.llm.invoke(messages)

            return response
        
        except Exception as e:

            logger.error(f"LLM invocation failed: {str(e)}")

            raise

    def with_structured_output(self, schema):

        try: 

            structured_llm = self.llm.with_structured_output(schema)

            return structured_llm
        
        except Exception as e  :

            logger.error("Failed to create structured output LLM")

            raise