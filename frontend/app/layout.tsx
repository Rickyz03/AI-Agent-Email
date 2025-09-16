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
        <div className="flex h-screen">
          {/* Sidebar */}
          <aside className="w-64 bg-white border-r shadow-sm p-4 flex flex-col">
            <h1 className="text-xl font-bold mb-6">AI Agent Email</h1>
            <nav className="flex flex-col space-y-2">
              <Link href="/" className="hover:text-blue-600">
                Inbox
              </Link>
              <Link href="/manual" className="hover:text-blue-600">
                Manual Draft
              </Link>
              <Link href="/settings" className="hover:text-blue-600">
                Preferences
              </Link>
              <Link href="/kb" className="hover:text-blue-600">
                Knowledge Base
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
