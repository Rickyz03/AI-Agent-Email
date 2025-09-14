$backendHost = "http://127.0.0.1:8001"

# Log feedback: bozza accettata
Invoke-RestMethod -Uri "$backendHost/feedback?event_type=draft_accepted" `
  -Method POST -ContentType "application/json" `
  -Body (@{ metadata = @{ email_id = 1; variant = 0 } } | ConvertTo-Json -Depth 3)
