"use client";

import { useState } from "react";
import { indexDocuments } from "../api/kb";

export default function KBUploader() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");

  async function handleUpload() {
    if (!title || !text) return;
    try {
      await indexDocuments([{ id: Date.now().toString(), title, text }]);
      setStatus("Document uploaded successfully!");
      setTitle("");
      setText("");
    } catch {
      setStatus("Upload failed.");
    }
  }

  return (
    <div className="space-y-4">
      <input
        type="text"
        placeholder="Document title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full p-2 border rounded"
      />
      <textarea
        placeholder="Document text..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full p-2 border rounded min-h-[120px]"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload
      </button>
      {status && <p className="text-sm text-gray-700">{status}</p>}
    </div>
  );
}
