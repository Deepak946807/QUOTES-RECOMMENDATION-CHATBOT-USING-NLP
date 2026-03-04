from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

# URL of the Rasa server's REST webhook. Can be overridden with env var.
RASA_URL = os.environ.get("RASA_URL", "http://localhost:5005/webhooks/rest/webhook")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/message", methods=["POST"])
def message():
    """Proxy a chat message to the Rasa assistant and return the bot's response.

    Expected JSON payload: { "sender": "optional_user_id", "message": "text" }
    """
    data = request.get_json(force=True, silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Message text required."}), 400

    sender = data.get("sender", "web_user")
    try:
        resp = requests.post(RASA_URL, json={"sender": sender, "message": data["message"]}, timeout=10)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": "Unable to contact Rasa server.", "details": str(e)}), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
