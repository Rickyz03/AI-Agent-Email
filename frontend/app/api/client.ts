import axios from "axios";

// Axios client for backend API calls
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8001",
  headers: {
    "Content-Type": "application/json",
  },
});
