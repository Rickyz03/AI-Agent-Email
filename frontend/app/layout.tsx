import "./styles/globals.css";
import Link from "next/link";

export const metadata = {
  title: "AI Agent Email",
  description: "Email assistant with AI draft generation and knowledge base",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <div className="flex h-screen gap-4">
          {/* Sidebar */}
          <aside className="w-64 bg-gradient-to-b from-primary-dark to-primary p-6 text-white flex flex-col shadow-lg">
            <h1 className="text-2xl font-extrabold mb-8 tracking-tight">📧 AI Agent</h1>
            <nav className="flex flex-col space-y-3">
              <Link href="/" className="hover:bg-primary-light/20 p-2 rounded-md">📥 Inbox</Link>
              <Link href="/manual" className="hover:bg-primary-light/20 p-2 rounded-md">✍️ Manual Draft</Link>
              <Link href="/settings" className="hover:bg-primary-light/20 p-2 rounded-md">⚙️ Preferences</Link>
              <Link href="/kb" className="hover:bg-primary-light/20 p-2 rounded-md">📚 Knowledge Base</Link>
            </nav>
          </aside>

          {/* Main content */}
          <main className="flex-1 p-6 overflow-y-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
