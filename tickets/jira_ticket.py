import asyncio
from urllib.error import HTTPError

from fastapi import APIRouter, HTTPException
from jira import JIRA
from typing import Dict, Any
from pydantic import BaseModel

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

class CreateJiraTicketRequest(BaseModel):
    data: Dict[str, Any]
    jira_domain: str
    email: str
    jira_api_key: str
    board_id: str

@router.post("/create_ticket")
async def create_jira_ticket(request: CreateJiraTicketRequest):
    jira = JIRA(server=request.jira_domain, basic_auth=(request.email, request.jira_api_key))

    try:
        response = jira.create_issue(
            project=request.board_id,
            summary=request.data["summary"],
            description=request.data["description"],
            issuetype={"name": "Task"}
        )
        # Return the created ticket details
        return {
            "id": response.id,
            "key": response.key,
            "self": response.self
        }

    except HTTPError as e:
        print(f"HTTP Error creating ticket: {e.response.text}")
        raise
    except Exception as e:
        print(f"Error creating ticket: {str(e)}")
        raise