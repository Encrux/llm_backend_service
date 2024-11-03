import json
from dataclasses import asdict
from fastapi import FastAPI, Form
from starlette.responses import JSONResponse
from backend.meeting_processor import MeetingProcessor
from backend.llm_client.ollama_client import OllamaClient
from fastapi.middleware.cors import CORSMiddleware
from backend.jira_ticket_creator import JiraTicketCreator, JiraTicket
import uvicorn

app = FastAPI()
llm_client = OllamaClient()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/summarize/")
async def summarize_log(conversation_log: str = Form(...)):
    meeting_processor = MeetingProcessor(llm_client=llm_client)
    summary = meeting_processor.summarize(conversation_log)
    return JSONResponse(content={"summary": summary})


@app.post("/generate_tickets/")
async def generate_tickets(conversation_log: str = Form(...)):
    meeting_processor = MeetingProcessor(llm_client=llm_client)
    tickets = [asdict(ticket) for ticket in meeting_processor.generate_tickets(conversation_log)]
    return JSONResponse(content={"tickets": tickets})


@app.post("/push_ticket_to_jira/")
async def push_ticket_to_jira(ticket: str = Form(...)):
    ticket_data = json.loads(ticket)
    ticket_creator = JiraTicketCreator()
    response = ticket_creator.create_ticket(JiraTicket(**ticket_data))
    return JSONResponse(content={"response": response})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
