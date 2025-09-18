"use client";

import { useEffect, useState } from "react";
import { fetchInbox } from "../api/emails";
import { EmailIn } from "../types/api";
import EmailCard from "./EmailCard";
import Loader from "./Loader";
import Link from "next/link";

export default function InboxList() {
  const [emails, setEmails] = useState<EmailIn[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchInbox();
        setEmails(data);

        // OPTIONAL: cache inbox so thread page can try to rebuild if needed
        try {
          sessionStorage.setItem("ai_inbox_cache", JSON.stringify(data));
        } catch (e) {
          // sessionStorage may not be available in certain environments
          console.warn("sessionStorage not available:", e);
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <Loader />;

  return (
    <div className="space-y-4">
      {emails.map((email) => {
        const storageKey = `ai_selected_email_${email.thread_id}`;
        const storeEmail = () => {
          try {
            sessionStorage.setItem(storageKey, JSON.stringify(email));
          } catch (e) {
            console.warn("Unable to write to sessionStorage:", e);
          }
        };

        return (
          <Link
            key={email.id}
            href={`/threads/${email.thread_id}`}
            onMouseDown={storeEmail}
            onClick={storeEmail} // double write for robustness
          >
            <EmailCard email={email} />
          </Link>
        );
      })}
    </div>
  );
}
