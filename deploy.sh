#!/bin/bash

# Stop and remove the running container defined in docker-compose
docker-compose down

# Pull the latest changes from the git repository
git pull

# Build the Docker images
docker-compose build

# Start the Docker containers
docker-compose up -d