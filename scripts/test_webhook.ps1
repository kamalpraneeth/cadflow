$headers = @{
    "Content-Type" = "application/json"
    "X-GitHub-Event" = "pull_request"
}
$body = @{
    pull_request = @{
        number = 42
        head = @{
            sha = "a1b2c3d4e5f6g7h8i9j0"
        }
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/webhook/github" -Headers $headers -Body $body
