import InboxList from "./components/InboxList";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Inbox</h2>
      {/* Email/threads list */}
      <InboxList />
    </div>
  );
}
