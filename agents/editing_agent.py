from langchain.agents import create_agent
from prompts.prompts import editing_prompt
from tools.calendar_tools import modify_event as modify_an_event,get_calendar_service
from langchain.tools import tool

@tool("modify_event", return_direct=True)
def modify_event(event_id, summary=None, description=None, start_time_iso=None, end_time_iso=None):
    """
    Modifies an existing calendar event with the provided details.

    Parameters:
    - event_id: The ID of the event to modify.
    - summary: (Optional) The new summary/title for the event.
    - description: (Optional) The new description for the event.
    - start_time_iso: (Optional) The new start time in ISO 8601 format (e.g., "2026-05-27T10:00:00+03:00").
    - end_time_iso: (Optional) The new end time in ISO 8601 format.

    Returns:
    - A message indicating the result of the modification or a link to the updated event.
    """
    return modify_an_event(get_calendar_service(), event_id, summary, description, start_time_iso, end_time_iso)

editing_agent=create_agent(
    model="gpt-4o-mini",
    system_prompt=editing_prompt(),
    tools=[modify_event]
)