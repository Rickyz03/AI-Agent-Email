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
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <Loader />;

  return (
    <div className="space-y-4">
      {emails.map((email) => (
        <Link key={email.id} href={`/threads/${email.thread_id}`}>
          <EmailCard email={email} />
        </Link>
      ))}
    </div>
  );
}
