from backend.meeting_processor import MeetingProcessor
from backend.llm_client.ollama_client import OllamaClient
from dataclasses import asdict
from backend.jira_ticket_creator import JiraTicketCreator


llm_client = OllamaClient()
meeting_processor = MeetingProcessor(llm_client)


with open('backend/example_log.txt') as f:
    meeting_log = f.read()

tickets = meeting_processor.generate_tickets(meeting_log)


for ticket in tickets:
    print(asdict(ticket))

jira_ticket_creator = JiraTicketCreator()

jira_ticket_creator.create_ticket(tickets[0])
