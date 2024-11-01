from backend.jira_ticket_creator import JiraTicket
from backend.llm_client.llm_client import LLMClient


class MeetingProcessor:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def summarize(self, meeting_log: str) -> str:
        summary = self.llm_client.prompt(
            "Summarize the meeting log. Identify open tasks in a bullet-point list. "
            "Identify the"
            "types of the tasks" + meeting_log
        )
        print(summary)
        return summary['response']

    def generate_tickets(self, meeting_log: str, default_proj='SCRUM') -> list[JiraTicket]:
        """
        Generate JIRA-like tickets from the meeting log.
        :return: list of JiraTicket objects
        """

        jira_ticket_type_description = JiraTicket.__init__.__annotations__

        res = self.llm_client.prompt(
            f"Summary: {meeting_log}"
            f"Read the meeting_log and identify potential To-Dos. Your task is to return a list of valid JIRA tickets"
            f"formatted as follows: {jira_ticket_type_description}"
            f"fill in the fields with the appropriate information."
            f"The project field should be set to {default_proj}."
            f"leave the fields empty if the information is not available."
            f"Make sure it's formatted as a python list of dictionaries, as your answer will be parsed directly."
        )['response']

        # Find the start and end indices of the list within the string
        start_index = res.index('[')
        # last square bracket in the string
        end_index = res.rindex(']') + 1

        # Extract the substring containing the list
        list_string = res[start_index:end_index]

        ticket_list = eval(list_string)

        try:
            return [JiraTicket(**ticket) for ticket in ticket_list]
        except Exception as e:
            # write ticket_list to a file for debugging
            with open('backend/dbg_logs/ticket_list.md', 'w') as f:
                f.write(list_string)
            raise e
