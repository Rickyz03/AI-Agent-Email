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
        className="bg-blue-600 text-white px-5 py-2 rounded-lg font-semibold shadow-md 
                  hover:bg-blue-700 hover:cursor-pointer disabled:opacity-50 transition-colors"
      >
        {loading ? "Generating..." : "✨ Generate Draft"}
      </button>

      {loading && <Loader />}

      {drafts && (
        <div className="mt-4 space-y-3">
          <h3 className="font-semibold">Generated Drafts</h3>
          <ul className="space-y-3">
            {drafts.variants.map((d, i) => (
              <li
                key={i}
                className="p-3 bg-gray-50 rounded-lg border hover:bg-white hover:shadow-md transition"
              >
                <span className="inline-block px-2 py-0.5 mb-2 text-xs rounded-full bg-accent-light text-white">
                  Draft {i + 1}
                </span>
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
