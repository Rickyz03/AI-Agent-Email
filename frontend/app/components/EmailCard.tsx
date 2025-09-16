"use client";

import { EmailIn } from "../types/api";

export default function EmailCard({ email }: { email: EmailIn }) {
  return (
    <div className="p-4 bg-white rounded-xl shadow-card hover:shadow-lg hover:scale-[1.01] cursor-pointer transition">
        <h3 className="font-bold text-lg text-gray-900">{email.subject || "(No subject)"}</h3>
        <p className="text-sm text-gray-500 mt-1">
            From: <span className="font-medium">{email.from_addr}</span>
        </p>
        <p className="text-gray-700 mt-2 line-clamp-3">{email.body}</p>
        <div className="flex justify-between items-center text-xs text-gray-400 mt-3">
            <span>Thread: {email.thread_id}</span>
            <span className="bg-primary-light text-white px-2 py-0.5 rounded-full text-xs">
            {email.language?.toUpperCase()}
            </span>
        </div>
    </div>
  );
}
