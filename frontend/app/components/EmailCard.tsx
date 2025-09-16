"use client";

import { EmailIn } from "../types/api";

export default function EmailCard({ email }: { email: EmailIn }) {
  return (
    <div className="p-4 border rounded-lg shadow-sm hover:shadow-md transition cursor-pointer bg-white">
      <h3 className="font-semibold text-lg">{email.subject || "(No subject)"}</h3>
      <p className="text-sm text-gray-600 mt-1">
        From: {email.from_addr} → To: {email.to_addrs?.join(", ")}
      </p>
      <p className="text-gray-800 mt-2 line-clamp-3">{email.body}</p>
      <div className="text-xs text-gray-500 mt-2">
        Thread: {email.thread_id} | Language: {email.language}
      </div>
    </div>
  );
}
