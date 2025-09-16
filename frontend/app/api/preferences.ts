import { api } from "./client";
import { PreferenceIn, PreferenceOut } from "../types/api";

// Get user preferences
export async function getPreferences(): Promise<PreferenceOut> {
  const res = await api.get<PreferenceOut>("/preferences");
  return res.data;
}

// Update user preferences
export async function updatePreferences(
  prefs: PreferenceIn
): Promise<PreferenceOut> {
  const res = await api.post<PreferenceOut>("/preferences", prefs);
  return res.data;
}
