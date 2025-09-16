# ============================================================
# Comandi PowerShell per testare gli endpoint del backend FastAPI
# ============================================================
# Nota: modifica $host se il backend non gira in locale
$backendHost = "http://127.0.0.1:8001"

# -------------------------
# ROOT
# -------------------------
Invoke-RestMethod -Uri "$backendHost/" -Method GET

# -------------------------
# INGESTION
# -------------------------
# Ingest da IMAP
Invoke-RestMethod -Uri "$backendHost/ingest?provider=imap" -Method POST

# Ingest da Gmail
Invoke-RestMethod -Uri "$backendHost/ingest?provider=gmail" -Method POST

# -------------------------
# DRAFT GENERATION
# -------------------------
# Bozza con thread_id esistente
Invoke-RestMethod -Uri "$backendHost/draft" -Method POST -ContentType "application/json" -Body '{
  "thread_id": 1,
  "subject": "Re: Richiesta informazioni",
  "body": "Buongiorno, vorrei sapere i tempi di consegna.",
  "from_addr": "cliente@example.com",
  "to_addrs": ["support@example.com"],
  "cc_addrs": ["cc@example.com"],
  "bcc_addrs": []
}'

# Bozza con nuovo thread (senza thread_id)
Invoke-RestMethod -Uri "$backendHost/draft" -Method POST -ContentType "application/json" -Body '{
  "subject": "Domanda sui prezzi",
  "body": "Potete confermarmi il prezzo aggiornato?",
  "from_addr": "cliente2@example.com",
  "to_addrs": ["vendite@example.com"]
}'

# -------------------------
# KNOWLEDGE BASE
# -------------------------
# Indicizzare documenti multipli
Invoke-RestMethod -Uri "$backendHost/kb/index" -Method POST -ContentType "application/json" -Body '{
  "documents": [
    {"id": "doc1", "title": "Policy Resi", "text": "Resi possibili entro 30 giorni con scontrino.", "source": "documento interno"},
    {"id": "doc2", "title": "Listino prezzi", "text": "Prezzo base prodotto X = 100 euro.", "source": "documento interno"}
  ]
}'

# -------------------------
# PREFERENCES
# -------------------------
# Impostare preferenze utente
Invoke-RestMethod -Uri "$backendHost/preferences" -Method POST -ContentType "application/json" -Body '{
  "tone": "formale",
  "signature": "Cordiali saluti,\nIl team",
  "language": "it"
}'

# Leggere preferenze utente
Invoke-RestMethod -Uri "$backendHost/preferences" -Method GET

# -------------------------
# FEEDBACK
# -------------------------
# Log feedback: bozza accettata
Invoke-RestMethod -Uri "$backendHost/feedback" `
  -Method POST -ContentType "application/json" `
  -Body (@{
    event_type = "draft_accepted"
    metadata   = @{ email_id = 1; variant = 0 }
  } | ConvertTo-Json -Depth 3)

# Log feedback: bozza rifiutata
Invoke-RestMethod -Uri "$backendHost/feedback" `
  -Method POST -ContentType "application/json" `
  -Body (@{
    event_type = "draft_rejected"
    metadata   = @{ email_id = 2; reason = "non rilevante" }
  } | ConvertTo-Json -Depth 3)

# Log feedback: bozza modificata
Invoke-RestMethod -Uri "$backendHost/feedback" `
  -Method POST -ContentType "application/json" `
  -Body (@{
    event_type = "draft_edited"
    metadata   = @{ email_id = 3; diff = "aggiunto saluto finale" }
  } | ConvertTo-Json -Depth 3)
