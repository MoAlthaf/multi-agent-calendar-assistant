from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

from prompts.prompts import availability_checking_prompt
from tools.calendar_tools import availability_check, get_calendar_service

load_dotenv()


@tool("check_availability", return_direct=False)
def check_availability(start_time, end_time):
    """
    Checks the user's calendar for events between the specified start and end times.

    Parameters:
    - start_time: The start time in ISO 8601 format (e.g., "2026-05-26T10:00:00+03:00").
    - end_time: The end time in ISO 8601 format.

    Returns:
    - A message indicating whether the user is available or a list of events found in that time range.
    """
    return availability_check(get_calendar_service(), start_time, end_time)


availability_checking_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt=availability_checking_prompt(datetime.now().strftime("%Y-%m-%d")),
    tools=[check_availability],
)
