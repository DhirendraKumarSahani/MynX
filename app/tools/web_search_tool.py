from langchain_core.tools import tool
from serpapi import GoogleSearch
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


@tool
def web_search(query: str) -> str:
    """
    Search Google using SerpAPI and return results.
    """

    try:

        params = {
            "engine": "google",
            "q": query,
            "api_key": settings.SERP_API_KEY,
            "num": 5
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        organic = results.get("organic_results", [])

        if not organic:
            return "No results found."

        formatted = []

        for i, item in enumerate(organic[:5], start=1):

            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")

            formatted.append(
                f"{i}. {title}\n{snippet}\n{link}"
            )

        return "\n\n".join(formatted)

    except Exception as e:

        logger.error(f"Web search tool error: {str(e)}")

        return "Search service unavailable"