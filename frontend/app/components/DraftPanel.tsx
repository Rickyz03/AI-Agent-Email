"use client";

import { useState } from "react";
import { generateDraft } from "../api/emails";
import { EmailIn, DraftOut } from "../types/api";
import Loader from "./Loader";
import FeedbackButtons from "./FeedbackButtons";

export default function DraftPanel() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [drafts, setDrafts] = useState<DraftOut | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    setLoading(true);
    try {
      const email: EmailIn = {
        subject,
        body,
        from_addr: "me@example.com",
        to_addrs: ["you@example.com"],
      };
      const result = await generateDraft(email);
      setDrafts(result);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-4 border rounded-xl shadow-md space-y-4 bg-white">
      <h2 className="text-xl font-bold">AI Draft Generator</h2>

      <input
        type="text"
        placeholder="Subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        className="w-full p-2 border rounded"
      />

      <textarea
        placeholder="Body..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
        className="w-full p-2 border rounded min-h-[120px]"
      />

      <button
        onClick={handleGenerate}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      {loading && <Loader />}

      {drafts && (
        <div className="mt-4 space-y-3">
          <h3 className="font-semibold">Generated Drafts</h3>
          <ul className="list-disc pl-6 space-y-2">
            {drafts.variants.map((d, i) => (
              <li key={i} className="bg-gray-50 p-2 rounded">
                <p>{d}</p>
                <FeedbackButtons draftText={d} />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
