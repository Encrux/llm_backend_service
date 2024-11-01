# app.py
from dataclasses import asdict

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from backend.jira_ticket_creator import JiraTicketCreator
from backend.meeting_processor import MeetingProcessor
from backend.llm_client.ollama_client import OllamaClient
import uvicorn

app = FastAPI()
llm_client = OllamaClient()


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
