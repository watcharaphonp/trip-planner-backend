from crewai import Agent
from tools.search_duckduckgo_tools import DuckDuckGoSearchTools
from tools.web_scraper_tools import WebScraperTools
from tools.search_weather_info_tools import WeatherSearchTools
from tools.calculator_tools import CalculatorTools
from configs.model import Models


class TravelAgents:

    def __init__(self):
        self.model_configs = Models.claude3Haiku()
        self.llm = self.model_configs["model"]
        self.max_rpm = self.model_configs["max_rpm"]
        self.max_iter = self.model_configs["max_iter"]

    def city_selection_agent(self):
        return Agent(
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                WebScraperTools.scrape_and_summarize_website,
                WeatherSearchTools.summarize_weather_info_from_web,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
            allow_delegation=True,
        )

    def local_expert(self):
        return Agent(
            role="Local Expert at this city",
            goal="Provide the BEST insights about the selected city",
            backstory="""A knowledgeable local guide with extensive information about the city, it's attractions and customs""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                WebScraperTools.scrape_and_summarize_website,
                WeatherSearchTools.summarize_weather_info_from_web,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
            allow_delegation=True,
        )

    def travel_concierge(self):
        return Agent(
            role="Amazing Travel Concierge",
            goal="""Create the most amazing travel itineraries with budget and packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with decades of experience""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                WebScraperTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
                WeatherSearchTools.summarize_weather_info_from_web,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
            allow_delegation=True,
        )
