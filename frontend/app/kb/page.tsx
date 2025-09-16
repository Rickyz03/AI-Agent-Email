"use client";

import KBUploader from "../components/KBUploader";

export default function KnowledgeBasePage() {
  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">Knowledge Base</h2>
      <p className="mb-4 text-gray-700">
        Upload and manage documents that will be used as a knowledge base for draft generation.
      </p>
      <KBUploader />
    </div>
  );
}
