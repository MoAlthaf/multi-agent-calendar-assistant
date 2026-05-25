from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

from prompts.prompts import schedule_event_prompt
from tools.calendar_tools import create_event, get_calendar_service

load_dotenv()


@tool("schedule_event", return_direct=True)
def schedule_event(summary: str, description: str, start_time_iso: str, end_time_iso: str) -> str:
    """
    Schedules an event in the user's calendar using the provided details.

    Parameters:
    - summary: A brief title for the event.
    - description: A detailed description of the event.
    - start_time_iso: The start time of the event in ISO 8601 format
      (e.g., "2026-05-26T10:00:00+03:00").
    - end_time_iso: The end time of the event in ISO 8601 format.

    Returns:
    - A confirmation message with a link to the created event in the calendar.
    """
    calendar_service = get_calendar_service()
    event_link = create_event(calendar_service, summary, description, start_time_iso, end_time_iso)
    return f"✅ Event '{summary}' scheduled successfully! You can view it here: {event_link}"


scheduler_agent = create_agent(
    model="gpt-4o-mini",
    tools=[schedule_event],
    system_prompt=schedule_event_prompt(datetime.now().strftime("%Y-%m-%d")),
)
