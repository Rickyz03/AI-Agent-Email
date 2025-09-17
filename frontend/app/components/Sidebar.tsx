"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "📥 Inbox" },
  { href: "/manual", label: "✍️ Manual Draft" },
  { href: "/settings", label: "⚙️ Preferences" },
  { href: "/kb", label: "📚 Knowledge Base" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-gray-900 p-6 text-white flex flex-col shadow-lg">
      <h1 className="text-2xl font-extrabold mb-8 tracking-tight">📧 AI Agent Email</h1>
      <nav className="flex flex-col space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`p-2 rounded-md transition-colors cursor-pointer ${
                isActive
                  ? "bg-blue-600 text-white font-semibold"
                  : "text-gray-300 hover:bg-gray-700 hover:text-white"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
