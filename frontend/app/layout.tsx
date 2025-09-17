import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "AI Agent Email",
  description: "Email assistant with AI draft generation and knowledge base",
};


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <div className="flex h-screen gap-6">
          {/* Sidebar */}
          <aside className="w-64 bg-gray-900 p-6 text-white flex flex-col shadow-lg">
            <h1 className="text-2xl font-extrabold mb-8 tracking-tight">📧 AI Agent</h1>
            <nav className="flex flex-col space-y-3">
              <Link
                href="/"
                className="p-2 rounded-md hover:bg-primary-light/20 hover:cursor-pointer transition-colors"
              >
                📥 Inbox
              </Link>
              <Link
                href="/manual"
                className="p-2 rounded-md hover:bg-primary-light/20 hover:cursor-pointer transition-colors"
              >
                ✍️ Manual Draft
              </Link>
              <Link
                href="/settings"
                className="p-2 rounded-md hover:bg-primary-light/20 hover:cursor-pointer transition-colors"
              >
                ⚙️ Preferences
              </Link>
              <Link
                href="/kb"
                className="p-2 rounded-md hover:bg-primary-light/20 hover:cursor-pointer transition-colors"
              >
                📚 Knowledge Base
              </Link>
            </nav>
          </aside>

          {/* Main content */}
          <main className="flex-1 p-6 overflow-y-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
