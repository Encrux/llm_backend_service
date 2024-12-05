# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy SSL certificate and key
COPY /etc/letsencrypt/live/spacey.dns.army/fullchain.pem /app/fullchain.pem
COPY /etc/letsencrypt/live/spacey.dns.army/privkey.pem /app/privkey.pem

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 and 443 available to the world outside this container
EXPOSE 8000
EXPOSE 443

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/app/privkey.pem", "--ssl-certfile", "/app/fullchain.pem"]