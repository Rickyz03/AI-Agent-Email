"use client";

import { useState, useEffect } from "react";
import { generateDraft } from "../api/emails";
import { EmailIn, DraftOut } from "../types/api";

// Custom hook for drafts
export function useDrafts(email: EmailIn | null) {
  const [drafts, setDrafts] = useState<DraftOut | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!email) return;

    async function load() {
      setLoading(true);
      try {
        const result = await generateDraft(email);
        setDrafts(result);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [email]);

  return { drafts, loading };
}

// Custom hook for threads placeholder (to be expanded when backend has dedicated endpoint)
export function useThreads() {
  const [threads, setThreads] = useState<any[]>([]);

  // In future: call backend endpoint /threads
  useEffect(() => {
    setThreads([]); // placeholder
  }, []);

  return { threads };
}
