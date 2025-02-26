# Simple Groq wrapper

This is a simple wrapper for the Groq API to hide api key from the client side.

It implements basic rate limiting so that the API key is not abused.


## Example curl requests
local development
```bash
curl -X POST "http://localhost:8000/post/" -H "Content-Type: application/x-www-form-urlencoded" -d "query=Can you provide me with a cake recipe?"
```

example for deployed service @ spacey.dns.army
```bash
curl -X POST "https://spacey.dns.army/post/" -H "Content-Type: application/x-www-form-urlencoded" -d "query=Can you provide me with a cake recipe?"
```


-------
example call to create jira ticket at jira:

```bash
curl -D- \
  -u mail:jira_api_key \
  -X POST \
  --data @test/data/jira_api.json \
  -H "Content-Type: application/json" \
  https://neainfinity.atlassian.net/rest/api/2/issue/
```

example call to the proxy:

```bash
curl -X POST \
     --data @test/data/proxy.json \
     -H "Content-Type: application/json" \
     http://localhost:8000/tickets/create_ticket   
```


## Deployment
To deploy, just run deploy.sh. Make sure docker is installed and wokring.

Also, provide a .env file with the following content:
```bash
GROQ_API_KEY="your-api-key-here"
GROQ_MODEL="a-model-available-on-groq"
```
