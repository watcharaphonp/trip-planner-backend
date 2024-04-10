from crewai import Task
from textwrap import dedent
from job_manager import append_task_output, append_event
from utils.logging import logger


class TravelTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_name, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_name + " has been finished")
        append_task_output(self.job_id, task_output.exported_output, task_name)

    def identify_task(self, agent, origin, cities, interests, range):
        task_name = "identify_task"
        return Task(
            description=dedent(
                f"""Analyze and select the best city for the trip based on specific criteria such as weather patterns, seasonal events, and travel costs. This task involves comparing multiple cities, considering factors like current weather conditions, upcoming cultural or seasonal events, and overall travel expenses.
            Your final answer must be a detailed report on the chosen city, and everything you found out about it, including the actual flight costs, weather forecast and attractions.
            
            {self.__tip_section()}
            
            {self.__important()}

            Traveling from: {origin}
            City Options: {cities}
            Trip Date: {range}
            Traveler Interests: {interests}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown that highlights topics in bold"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def gather_task(self, agent, origin, cities, interests, range):
        task_name = "gather_task"
        return Task(
            description=dedent(
                f"""As a local expert on this city you must compile an in-depth guide for someone traveling there and wanting to have THE BEST trip ever!

            Gather information about  key attractions, local customs, special events, and daily activity recommendations. Find the best spots to go to, the kind of place only a local would know.

            This guide should provide a thorough overview of what the city has to offer, including hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high level costs.
            
            The final answer must be a comprehensive city guide, rich in cultural insights and practical tips, tailored to enhance the travel experience.
            
            {self.__tip_section()}
            
            {self.__important()}

            Trip Date: {range}
            Traveling from: {origin}
            City Options: {cities}
            Traveler Interests: {interests}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown that highlights topics in bold"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def plan_task(self, agent, origin, cities, interests, range):
        task_name = "plan_task"
        return Task(
            description=dedent(
                f"""Expand this guide into a travel itinerary with detailed per-day plans, including weather forecasts, places to eat, packing suggestions, and a budget breakdown.
            
            You MUST suggest actual places to visit, actual hotels to stay and actual restaurants to go to.
            
            This itinerary should cover all aspects of the trip, from arrival to departure, integrating the city guide information with practical travel logistics.
            
            Your final answer MUST be a complete expanded travel plan, formatted as markdown, encompassing a daily schedule, anticipated weather conditions, recommended clothing and items to pack, and a detailed budget, ensuring THE BEST TRIP EVER, Be specific and give it a reason why you picked up each place, what make them special!
            
            {self.__tip_section()}
            
            {self.__important()}

            Trip Date: {range}
            Traveling from: {origin}
            City Options: {cities}
            Traveler Interests: {interests} """
            ),
            agent=agent,
            expected_output=dedent("""Markdown that highlights topics in bold"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"

    def __important(self):
        return f"""To do this task, you understand the following rules:
        1. Find weather information from searching the internet using the word that start with \"Accuweather\" and appending it with the city name and month for which you want to know weather information only. Then use the first result from the first url as your final answer.
        2. If weather information is not found, You must continue to search and provide information on other topics without considering the weather information.
        3. All information such as weather, special events and best place to visit must be shared between agents. There will be no duplicate searches on the internet for existing data.
        """
