from app.tools.weather_tool import get_weather
from app.tools.web_search_tool import web_search
from app.tools.tavily_tool import get_tavily_tool


class ToolRegistry:

    @staticmethod
    def get_tools():

        tavily_tool = get_tavily_tool()

        tools = [
            get_weather,
            web_search,
            tavily_tool
        ]

        return tools