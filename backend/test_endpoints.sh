#!/usr/bin/env bash
# ============================================================
# Comandi curl per testare gli endpoint del backend FastAPI
# ============================================================
# Nota: sostituisci HOST se il backend non gira in locale.
HOST="http://127.0.0.1:8001"

# -------------------------
# ROOT
# -------------------------
curl -X GET "$HOST/" -H "accept: application/json"

# -------------------------
# INGESTION
# -------------------------
# Ingest da IMAP
curl -X POST "$HOST/ingest?provider=imap" -H "accept: application/json"

# Ingest da Gmail
curl -X POST "$HOST/ingest?provider=gmail" -H "accept: application/json"

# -------------------------
# DRAFT GENERATION
# -------------------------
# Bozza con thread_id esistente
curl -X POST "$HOST/draft" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": 1,
    "subject": "Re: Richiesta informazioni",
    "body": "Buongiorno, vorrei sapere i tempi di consegna.",
    "from_addr": "cliente@example.com",
    "to_addrs": ["support@example.com"],
    "cc_addrs": ["cc@example.com"],
    "bcc_addrs": []
  }'

# Bozza con nuovo thread (senza thread_id)
curl -X POST "$HOST/draft" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Domanda sui prezzi",
    "body": "Potete confermarmi il prezzo aggiornato?",
    "from_addr": "cliente2@example.com",
    "to_addrs": ["vendite@example.com"]
  }'

# -------------------------
# KNOWLEDGE BASE
# -------------------------
# Indicizzare documenti multipli
curl -X POST "$HOST/kb/index" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"id": "doc1", "title": "Policy Resi", "text": "Resi possibili entro 30 giorni con scontrino."},
      {"id": "doc2", "title": "Listino prezzi", "text": "Prezzo base prodotto X = 100€."}
    ]
  }'

# -------------------------
# PREFERENCES
# -------------------------
# Impostare preferenze utente
curl -X POST "$HOST/preferences" \
  -H "Content-Type: application/json" \
  -d '{
    "tone": "formale",
    "signature": "Cordiali saluti,\nIl team",
    "language": "it"
  }'

# Leggere preferenze utente
curl -X GET "$HOST/preferences" -H "accept: application/json"

# -------------------------
# FEEDBACK
# -------------------------
# Log feedback: bozza accettata
curl -X POST "$HOST/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "draft_accepted",
    "metadata": {"email_id": 1, "variant": 0}
  }'

# Log feedback: bozza rifiutata
curl -X POST "$HOST/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "draft_rejected",
    "metadata": {"email_id": 2, "reason": "non rilevante"}
  }'

# Log feedback: bozza modificata
curl -X POST "$HOST/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "draft_edited",
    "metadata": {"email_id": 3, "diff": "aggiunto saluto finale"}
  }'
