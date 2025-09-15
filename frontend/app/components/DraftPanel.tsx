"use client";

import { useState } from "react";
import { generateDraft } from "../api/emails";
import { EmailIn, DraftOut } from "../types/api";

export default function DraftPanel() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [drafts, setDrafts] = useState<DraftOut | null>(null);

  async function handleGenerate() {
    const email: EmailIn = {
      subject,
      body,
      from_addr: "me@example.com",
      to_addrs: ["you@example.com"],
    };
    const result = await generateDraft(email);
    setDrafts(result);
  }

  return (
    <div className="p-4 border rounded-xl shadow-md space-y-4">
      <h2 className="text-xl font-bold">Genera bozza AI</h2>
      <input
        type="text"
        placeholder="Oggetto"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        className="w-full p-2 border rounded"
      />
      <textarea
        placeholder="Corpo email..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
        className="w-full p-2 border rounded"
      />
      <button
        onClick={handleGenerate}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Genera
      </button>

      {drafts && (
        <div className="mt-4">
          <h3 className="font-semibold">Bozze generate:</h3>
          <ul className="list-disc pl-6">
            {drafts.variants.map((d, i) => (
              <li key={i} className="mt-2">{d}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
