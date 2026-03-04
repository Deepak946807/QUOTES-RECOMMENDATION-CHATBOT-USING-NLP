import requests, json

sender='debug123'
print('sending message')
resp = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'sender': sender, 'message': 'inspiration'})
print('response', resp.text)
tracker = requests.get(f'http://localhost:5005/conversations/{sender}/tracker').json()
print('tracker', json.dumps(tracker, indent=2))
