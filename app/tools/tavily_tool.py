from langchain_tavily import TavilySearch
from app.core.config import settings


def get_tavily_tool():

    tool = TavilySearch(
        tavily_api_key=settings.TAVILY_API_KEY,
        max_results=3
    )

    return tool