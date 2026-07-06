#!/usr/bin/env bash
set -e

# Start the Rasa action server in the background
rasa run actions --port 5055 &

# Start the Rasa NLU/core server in the background (uses the existing trained model)
rasa run --enable-api --port 5005 &

# Give Rasa time to load the trained model before the web UI starts
sleep 25

# Start the Flask web UI in the foreground — this is what Render exposes publicly
export FLASK_APP=web.app
python -m flask run --host 0.0.0.0 --port "$PORT"