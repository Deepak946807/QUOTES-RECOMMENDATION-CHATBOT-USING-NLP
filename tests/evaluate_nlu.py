import requests
import yaml
import os

RASA_URL = os.environ.get("RASA_URL", "http://localhost:5005")


def load_tests(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    examples = []
    for entry in data.get('nlu', []):
        intent = entry.get('intent')
        for line in entry.get('examples','').split('\n'):
            line = line.strip().lstrip('-').strip()
            if line:
                examples.append((line, intent))
    return examples


def evaluate(examples):
    correct = 0
    total = len(examples)
    details = []
    for text, intent in examples:
        resp = requests.post(f"{RASA_URL}/model/parse", json={"text": text})
        result = resp.json()
        pred = result.get('intent', {}).get('name')
        conf = result.get('intent', {}).get('confidence')
        correct += (pred == intent)
        details.append((text, intent, pred, conf))
    accuracy = correct / total if total else 0
    return accuracy, details


if __name__ == "__main__":
    tests = load_tests(os.path.join(os.path.dirname(__file__), 'test_nlu.yml'))
    acc, det = evaluate(tests)
    print(f"Evaluated {len(tests)} examples, accuracy {acc:.2%}")
    for text, gold, pred, conf in det:
        print(f"{text!r}: gold={gold} pred={pred} ({conf:.2f})")
