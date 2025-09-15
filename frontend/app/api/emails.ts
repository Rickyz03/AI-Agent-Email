import { api } from "./client";
import { EmailIn, DraftOut } from "../types/api";

export async function generateDraft(email: EmailIn): Promise<DraftOut> {
  const res = await api.post<DraftOut>("/draft", email);
  return res.data;
}
