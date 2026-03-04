# Quotes Recommendation Chatbot — Run & Deploy

Quick steps to test and deploy the chatbot locally.

Prerequisites:

- Python 3.8+ and virtual environment
- Rasa installed in the project's virtual environment

1. Activate your venv (Windows PowerShell):

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

2. (Optional) Install web UI deps:

```powershell
pip install -r requirements.txt
```

3. Start the actions server (in project root):

```powershell
rasa run actions
```

4. Start the Rasa server with API enabled (CORS is no longer required since the UI talks to the Flask proxy):

```powershell
rasa run --enable-api --port 5005
```

5. Serve the web UI (in project root):

```powershell
# install backend dependencies if not already done
pip install -r requirements.txt

# start the Flask UI & proxy
$env:FLASK_APP = "web.app"; flask run --port 8080
```

6. Open the web UI at `http://localhost:8080` and chat. The modern front-end includes avatars, a typing spinner, and clickable suggestion buttons (motivation, inspiration, love, success, funny) to speed up testing. It posts to the local Flask endpoint `/api/message`, which forwards requests to Rasa; set the `RASA_URL` environment variable to point elsewhere if needed.

### Running automated tests

We use `pytest` for simple integration tests and Rasa's built‑in test runners for NLU/stories. After you train the model (step 4 above):

```powershell
# run the custom Python tests (requires the Rasa server to be running)
python -m pytest tests/test_feedback.py

# run the story/intent tests
rasa test
```

The `requirements.txt` now pins `pytest` and `packaging<21.0` so that training works reliably with Rasa 3.x.

> Behind the scenes the custom actions are now more efficient: a single base class handles all categories, so adding a new quote type requires only a few lines of configuration.

If you need help wiring production deployment or adding HTTPS, I can add a simple Nginx + systemd example.
# QUOTES-RECOMMENDATION-CHATBOT-USING-NLP
# QUOTES-RECOMMENDATION-CHATBOT-USING-NLP
# QUOTES-RECOMMENDATION-CHATBOT-USING-NLP
