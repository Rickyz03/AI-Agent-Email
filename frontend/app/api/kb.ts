import { api } from "./client";

export interface KBDocument {
  id: string;
  title: string;
  text: string;
  source?: string;
}

export async function indexDocuments(docs: KBDocument[]): Promise<void> {
  await api.post("/kb/index", { documents: docs });
}
