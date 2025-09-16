"use client";

import { useEffect, useState } from "react";
import { getPreferences, updatePreferences } from "../api/preferences";
import { PreferenceIn, PreferenceOut } from "../types/api";

export default function PreferencesForm() {
  const [prefs, setPrefs] = useState<PreferenceIn>({
    tone_default: "formal",
    sign_off: "Best regards",
    signature_block: "AI Agent Email",
  });

  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data: PreferenceOut = await getPreferences();
        setPrefs(data);
      } catch {
        // If no preferences exist yet, keep defaults
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const result = await updatePreferences(prefs);
    setPrefs(result);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  if (loading) return <p>Loading preferences...</p>;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <label className="block">
        <span className="text-sm font-medium">Default Tone</span>
        <input
          type="text"
          value={prefs.tone_default}
          onChange={(e) =>
            setPrefs({ ...prefs, tone_default: e.target.value })
          }
          className="w-full p-2 border rounded mt-1"
        />
      </label>

      <label className="block">
        <span className="text-sm font-medium">Sign-off</span>
        <input
          type="text"
          value={prefs.sign_off}
          onChange={(e) =>
            setPrefs({ ...prefs, sign_off: e.target.value })
          }
          className="w-full p-2 border rounded mt-1"
        />
      </label>

      <label className="block">
        <span className="text-sm font-medium">Signature Block</span>
        <textarea
          value={prefs.signature_block}
          onChange={(e) =>
            setPrefs({ ...prefs, signature_block: e.target.value })
          }
          className="w-full p-2 border rounded mt-1 min-h-[80px]"
        />
      </label>

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Save
      </button>

      {saved && <p className="text-green-600">Preferences saved!</p>}
    </form>
  );
}
