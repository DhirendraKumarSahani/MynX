from langchain.tools import tool
from app.tools.weather_tool import get_weather
from app.tools.web_search_tool import web_search
from app.tools.tavily_tool import get_tavily_tool


class ToolRegistry:

    @staticmethod
    def get_tools():

        tavily_tool = get_tavily_tool()

        tools = [
            tool("get_weather")(get_weather),
            tool("web_search")(web_search),
            tavily_tool
        ]

        return tools