import { api } from "./client";
import { EmailIn, DraftOut } from "../types/api";

// Fetch emails or threads from backend ingestion
export async function fetchInbox(): Promise<EmailIn[]> {
  const res = await api.post<EmailIn[]>("/ingest?provider=imap&n=50");
  return res.data;
}

// Fetch a specific thread by id
export async function fetchThreadById(threadId: string): Promise<EmailIn[]> {
  const res = await api.post<EmailIn[]>("/ingest?provider=imap&n=50");
  return res.data.filter((email) => email.thread_id === Number(threadId));
}

// Generate draft from email input
export async function generateDraft(email: EmailIn): Promise<DraftOut> {
  const res = await api.post<DraftOut>("/draft", email);
  return res.data;
}
