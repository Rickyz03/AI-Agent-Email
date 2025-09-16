import { api } from "./client";

// Log user feedback to the backend
export async function sendFeedback(eventType: string, metadata: object) {
  await api.post("/feedback", { event_type: eventType, metadata });
}
