import requests

# Read the content of example_log.txt
with open("backend/example_log.txt", "r") as file:
    conversation_log = file.read()

# Define the URL of the API endpoint
url = "http://0.0.0.0:8000/summarize_log/"

# Make the POST request
response = requests.post(url, data={"conversation_log": conversation_log})

# Print the response
print(response.json())