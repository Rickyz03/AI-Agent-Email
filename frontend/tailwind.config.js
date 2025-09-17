/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        primary: {
          light: "#60a5fa",
          DEFAULT: "#3b82f6",
          dark: "#1d4ed8",
        },
        accent: {
          light: "#34d399",
          DEFAULT: "#10b981",
          dark: "#047857",
        },
      },
      boxShadow: {
        card: "0 4px 10px rgba(0, 0, 0, 0.05)",
      },
    },
  },
  plugins: [],
};
