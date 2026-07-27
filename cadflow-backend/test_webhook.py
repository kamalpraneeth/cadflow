import httpx
payload = {
    "pull_request": {
        "number": 1,
        "head": {"sha": "1234567890abcdef"}
    }
}
resp = httpx.post("http://127.0.0.1:8050/webhook/github", json=payload)
print(resp.status_code, resp.text)
