import os
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
        model=os.environ.get("GROQ_MODEL"),
    )
    return chat_completion.choices[0].message.content


@app.post('/v1/chat/completions')
async def proxy_chat_completions(request: Request):
    """OpenAI-compatible proxy — forwards to Groq with rate limiting and API key injection."""
    if not proxy_rate_limiter.allow_request():
        wait_time = proxy_rate_limiter.wait_time()
        return JSONResponse(
            status_code=429,
            content={"error": {"message": f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.", "type": "rate_limit"}},
        )

    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{GROQ_BASE_URL}/v1/chat/completions",
            content=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}",
            },
            timeout=60.0,
        )

    return JSONResponse(status_code=resp.status_code, content=resp.json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
