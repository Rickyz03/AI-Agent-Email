// Formatters for dates, strings, etc.

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function truncateText(text: string, maxLength = 120): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
}
