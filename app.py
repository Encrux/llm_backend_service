import json
import os
from datetime import datetime
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from groq import Groq
from dotenv import load_dotenv
from tickets.jira_ticket import router as jira_router

from rate_limiter import RateLimiter

load_dotenv()
app = FastAPI()

app.include_router(jira_router)

origins = [
    "https://llm-trajectory.boesch.dev",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b")

rate_limiter = RateLimiter(10, 1)
proxy_rate_limiter = RateLimiter(20, 1)


@app.post('/post/')
async def post_query(query: str = Form(...)):
    print(query)
    if not rate_limiter.allow_request():
        wait_time = rate_limiter.wait_time()
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.")

    chat_completion = llm_client.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model=GROQ_MODEL,
    )
    return chat_completion.choices[0].message.content


@app.get('/config')
async def get_config():
    """Model the proxy is configured with. Clients display this instead of hardcoding a model."""
    return {"model": GROQ_MODEL}


@app.post('/v1/chat/completions')
async def proxy_chat_completions(request: Request):
    """OpenAI-compatible proxy — forwards to Groq with rate limiting and API key injection."""
    if not proxy_rate_limiter.allow_request():
        wait_time = proxy_rate_limiter.wait_time()
        return JSONResponse(
            status_code=429,
            content={"error": {"message": f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.", "type": "rate_limit"}},
        )

    try:
        body = json.loads(await request.body())
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": {"message": "Request body must be JSON.", "type": "invalid_request_error"}},
        )

    # The proxy owns the model choice — clients don't get to pick (and stale builds
    # shouldn't be able to request a model that's since been retired).
    body["model"] = GROQ_MODEL

    # Log the user's task for analytics
    try:
        for msg in body.get("messages", []):
            if msg.get("role") == "system":
                lines = msg["content"].split("\n")
                task = next((l.replace("Task: ", "") for l in lines if l.startswith("Task: ")), None)
                if task:
                    print(f"[prompt] {datetime.now().strftime('%H:%M:%S')} {task}")
                break
    except Exception:
        pass

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{GROQ_BASE_URL}/v1/chat/completions",
            json=body,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            timeout=60.0,
        )

    return JSONResponse(status_code=resp.status_code, content=resp.json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
