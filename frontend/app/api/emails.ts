import { api } from "./client";
import { EmailIn, DraftOut } from "../types/api";

// Config da env (con fallback ai default)
const PROVIDER = process.env.NEXT_PUBLIC_EMAIL_PROVIDER || "imap";
const UNREAD = process.env.NEXT_PUBLIC_EMAIL_UNREAD === "true"; // bool
const N = Number(process.env.NEXT_PUBLIC_EMAIL_N || "50");

// Fetch emails or threads from backend ingestion
export async function fetchInbox(): Promise<EmailIn[]> {
  const res = await api.post<EmailIn[]>(
    `/ingest?provider=${PROVIDER}&unread=${UNREAD}&n=${N}`
  );
  return res.data;
}

// Generate draft from email input
export async function generateDraft(email: EmailIn): Promise<DraftOut> {
  const res = await api.post<DraftOut>("/draft", email);
  return res.data;
}
