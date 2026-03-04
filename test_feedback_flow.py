#!/usr/bin/env python
import requests
import json

# Test feedback flow
BASE_URL = "http://localhost:5005/webhooks/rest/webhook"
SENDER_ID = "test_user_feedback"

def send_message(message_text):
    """Send a message and get bot response"""
    payload = {
        "sender": SENDER_ID,
        "message": message_text
    }
    response = requests.post(BASE_URL, json=payload)
    responses = response.json()
    print(f"\nUser: {message_text}")
    if responses:
        for r in responses:
            print(f"Bot: {r.get('text', r)}")
    else:
        print("Bot: [No response]")
    return responses

print("=" * 60)
print("Testing Feedback Flow")
print("=" * 60)

# Test flow 1: Request funny quote -> affirm
print("\n--- Flow 1: Funny quote + Affirmation ---")
send_message("funny quotes")  # Should trigger utter_funny + utter_helpful
send_message("yes")  # Should trigger utter_happy (feedback acknowledgement)

# Test flow 2: Request motivation quote -> deny
print("\n--- Flow 2: Motivation quote + Denial ---")
send_message("motivation")  # Should trigger utter_motivation + utter_helpful
send_message("no")  # Should trigger utter_ask (ask for another quote)

# Test flow 3: Greet + request inspiration + affirm
print("\n--- Flow 3: Full conversation with greeting ---")
send_message("hello")  # Greet
send_message("inspiration")  # Request inspiration quote
send_message("yes")  # Affirm the quote

print("\n" + "=" * 60)
