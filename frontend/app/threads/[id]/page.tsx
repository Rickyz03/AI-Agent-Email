"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import DraftPanel from "../../components/DraftPanel";
import EmailCard from "../../components/EmailCard";
import Loader from "../../components/Loader";
import { EmailIn } from "../../types/api";

export default function ThreadDetailPage() {
  const { id } = useParams();
  const [emails, setEmails] = useState<EmailIn[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    function loadFromSession() {
      try {
        // 1) Try directly the single email saved on click
        const raw = typeof window !== "undefined"
          ? sessionStorage.getItem(`ai_selected_email_${id}`)
          : null;

        if (raw) {
          try {
            const email = JSON.parse(raw) as EmailIn;
            setEmails([email]);
            return;
          } catch (e) {
            console.error("Parsing selected email failed:", e);
          }
        }

        // 2) Fallback: try to reconstruct from inbox cache (optional)
        const inboxRaw = typeof window !== "undefined" ? sessionStorage.getItem("ai_inbox_cache") : null;
        if (inboxRaw) {
          try {
            const inbox = JSON.parse(inboxRaw) as EmailIn[];
            const filtered = inbox.filter((em) => String(em.thread_id) === String(id));
            setEmails(filtered);
            return;
          } catch (e) {
            console.warn("Parsing inbox cache failed:", e);
          }
        }

        // 3) If everything fails, we remain with an empty array
        setEmails([]);
      } finally {
        setLoading(false);
      }
    }

    loadFromSession();
  }, [id]);

  if (loading) return <Loader />;

  if (!emails.length) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-bold">Thread #{id}</h2>
        <p className="text-sm text-gray-500">
          No emails available for this thread. Go back to the Inbox and select the email from which you want to generate a draft.
        </p>
      </div>
    );
  }

  const latestEmail = emails[emails.length - 1];

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Thread #{id}</h2>
      <div className="space-y-4">
        {emails.map((email) => (
          <EmailCard key={email.id} email={email} interactive={false} />
        ))}
      </div>

      <DraftPanel key={latestEmail?.id ?? "no-email"} email={latestEmail} />
    </div>
  );
}
