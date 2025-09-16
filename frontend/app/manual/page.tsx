"use client";

import DraftPanel from "../components/DraftPanel";

export default function ManualDraftPage() {
  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">Manual Draft Generation</h2>
      <p className="mb-4 text-gray-700">
        Enter subject and body manually to generate drafts with AI assistance.
      </p>
      <DraftPanel />
    </div>
  );
}
