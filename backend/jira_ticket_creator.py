import os
from typing import Optional, Dict
from jira import JIRA
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class JiraTicket:
    project_key: str
    summary: str
    description: str
    issue_type: str
    assignee: str
    labels: list[str]

    def __init__(self, project_key: str, summary: str, description: str, issue_type: str, assignee: str,
                 labels: list[str]):
        self.project_key = project_key
        self.summary = summary
        self.description = description
        self.issue_type = issue_type
        self.assignee = assignee
        self.labels = labels


class JiraTicketCreator:
    def __init__(self):
        """
        Initialize Jira ticket creator

        Args:
            domain: Your Jira domain (e.g., 'your-domain.atlassian.net')
            api_key: Your Jira API key
            email: Email associated with the API key
        """

        load_dotenv()

        domain = os.getenv("JIRA_DOMAIN")
        api_key = os.getenv("API_KEY")
        email = os.getenv("EMAIL")
        self.project_key = os.getenv("PROJECT_KEY")

        self.jira = JIRA(
            server=f"https://{domain}",
            basic_auth=(email, api_key)
        )

    def create_ticket(self, ticket: JiraTicket) -> Dict:
        """
        Create a new Jira ticket

        Args:
            ticket: JiraTicket object containing the ticket details

        Returns:
            Dict containing the response from Jira API
        """
        project_key = ticket.project_key if ticket.project_key else self.project_key

        issue_dict = {
            'project': {'key': project_key},
            'summary': ticket.summary,
            'description': ticket.description,
            'issuetype': {'name': ticket.issue_type},
        }

        if ticket.assignee:
            issue_dict['assignee'] = {'name': ticket.assignee}

        if ticket.labels:
            issue_dict['labels'] = ticket.labels

        try:
            new_issue = self.jira.create_issue(fields=issue_dict)
            return new_issue.raw
        except Exception as e:
            raise Exception(f"Error creating Jira ticket: {str(e)}")


def main():
    # apply .env to the environment
    load_dotenv()

    # Create ticket creator instance
    jira = JiraTicketCreator()

    # Create a new ticket
    try:
        new_ticket = jira.create_ticket(
            project_key="SCRUM",
            summary="Test Ticket",
            description="This is a test ticket created via API",
            issue_type="Task",
            labels=["automated", "test"]
        )
        print(f"Successfully created ticket: {new_ticket['key']}")
    except Exception as e:
        print(f"Failed to create ticket: {str(e)}")


if __name__ == "__main__":
    main()
