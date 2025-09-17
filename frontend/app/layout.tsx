import "./globals.css";
import Sidebar from "./components/Sidebar";

export const metadata = {
  title: "AI Agent Email",
  description: "Email assistant with AI draft generation and knowledge base",
};


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen gap-4">
          <Sidebar />
          <main className="flex-1 p-6 overflow-y-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
