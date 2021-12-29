import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

//

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://192.168.2.102:8080/",
    },
  },
});
