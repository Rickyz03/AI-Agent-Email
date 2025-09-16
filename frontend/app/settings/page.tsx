"use client";

import PreferencesForm from "../components/PreferencesForm";

export default function SettingsPage() {
  return (
    <div className="max-w-xl">
      <h2 className="text-2xl font-bold mb-6">User Preferences</h2>
      <PreferencesForm />
    </div>
  );
}
