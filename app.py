import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from groq import Groq
from dotenv import load_dotenv
from tickets.jira_ticket import router as jira_router

from rate_limiter import RateLimiter

load_dotenv()
app = FastAPI()

app.include_router(jira_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://spacey.dns.army",
    "https://encrux.github.io",
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

rate_limiter = RateLimiter(10, 1)


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)