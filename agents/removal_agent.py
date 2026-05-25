from langchain.agents import create_agent
from langchain.tools import tool
from tools.calendar_tools import remove_event,get_calendar_service
from prompts.prompts import deleting_prompt


@tool("remove_event", return_direct=False)
def delete_event(event_id: str):
    """
    Removes/deletes an event from the user's Google Calendar
    using the provided event ID.

    This tool permanently deletes the specified calendar event
    from the user's primary Google Calendar.

    Parameters:
    - event_id (str):
        The unique Google Calendar event ID of the event
        that should be deleted.

    Returns:
    - dict:
        A JSON response indicating whether the deletion
        was successful.

        Example:
        {
            "success": True,
            "message": "Event deleted successfully."
        }

    Raises:
    - HttpError:
        If the event does not exist or the Google Calendar
        API request fails.
    """
    return remove_event(get_calendar_service(),event_id)


removal_agent= create_agent(
    model="gpt-4o-mini",
    system_prompt=deleting_prompt(),
    tools=[delete_event]
)