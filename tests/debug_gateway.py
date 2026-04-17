
import requests
import json

def test_gateway():
    base_url = "http://127.0.0.1:8045"
    api_key = "sk-4e549191a32c4fac8f47643de92e66e1"
    model = "gemini-3-flash-agent"

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": model,
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Merhaba, orada mısın?"}
        ]
    }

    print(f"Testing {base_url}/v1/messages...")
    try:
        response = requests.post(f"{base_url}/v1/messages", headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gateway()
