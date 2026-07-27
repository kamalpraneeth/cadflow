import httpx

url = "https://cadflow.onrender.com/webhook/github"
payload = {
    "pull_request": {
        "number": 46,
        "head": {
            "sha": "cloud_commit_42"
        }
    }
}

print(f"Triggering webhook at {url}...")
try:
    response = httpx.post(url, json=payload, timeout=10.0)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
