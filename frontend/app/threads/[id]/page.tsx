"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import DraftPanel from "../../components/DraftPanel";
import EmailCard from "../../components/EmailCard";
import Loader from "../../components/Loader";
import { EmailIn } from "../../types/api";
import { fetchThreadById } from "../../api/emails";

export default function ThreadDetailPage() {
  const { id } = useParams();
  const [emails, setEmails] = useState<EmailIn[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchThreadById(id as string);
        setEmails(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) return <Loader />;

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Thread #{id}</h2>
      <div className="space-y-4">
        {emails.map((email) => (
          <EmailCard key={email.id} email={email} />
        ))}
      </div>
      <DraftPanel />
    </div>
  );
}
