#!/bin/bash

# Change to the backend directory
cd "$(dirname "$0")"

# Create a virtual environment (if it doesn't exist)
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate the virtual environment
. venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Run the FastAPI application using Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
