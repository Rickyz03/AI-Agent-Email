import DraftPanel from "./components/DraftPanel";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-8">
      <h1 className="text-3xl font-bold mb-6">AI Agent Email Dashboard</h1>
      <DraftPanel />
    </main>
  );
}
