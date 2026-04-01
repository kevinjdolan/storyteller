import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["frontend", "localhost", "127.0.0.1"],
    host: "0.0.0.0",
    port: 8566,
    proxy: {
      "/api": {
        target: process.env.VITE_DEV_PROXY_TARGET || "http://localhost:8565",
        changeOrigin: true,
      },
    },
  },
});
