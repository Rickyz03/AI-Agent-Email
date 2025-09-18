"use client";

import { sendFeedback } from "../api/feedback";

export default function FeedbackButtons({ draftText }: { draftText: string }) {
  async function handleFeedback(type: "accepted" | "edited" | "rejected") {
    await sendFeedback(`draft_${type}`, { draft: draftText });
  }

  return (
    <div className="flex space-x-2 mt-2">
      <button
        onClick={() => handleFeedback("accepted")}
        className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm cursor-pointer"
      >
        Accept
      </button>
      <button
        onClick={() => handleFeedback("edited")}
        className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 text-sm cursor-pointer"
      >
        Edit
      </button>
      <button
        onClick={() => handleFeedback("rejected")}
        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 text-sm cursor-pointer"
      >
        Reject
      </button>
    </div>
  );
}
