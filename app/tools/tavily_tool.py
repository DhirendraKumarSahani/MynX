from langchain_tavily import TavilySearch
from app.core.config import settings


def get_tavily_tool():

    base_tool = TavilySearch(
        tavily_api_key=settings.TAVILY_API_KEY,
        max_results=3
    )

    def safe_tavily_search(query: str):
        
        """
        Search the web using Tavily and return summarized results.
        Limits output to avoid large token usage.
        """

        result = base_tool.invoke({
            "query": query,
            "search_depth": "basic",
            "include_images": False
        })

        cleaned_results = []

        for r in result.get("results", [])[:3]:
            cleaned_results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content", "")[:200]
            })

        return str(cleaned_results)

    return safe_tavily_search