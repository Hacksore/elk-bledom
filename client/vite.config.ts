import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      includeManifestIcons: true,
      manifest: {
        name: "Office Lights",
        short_name: "Office Lights",
        icons: [
          {
            src: "icon-64.png",
            type: "image/png",
            sizes: "64x64",
          },
          {
            src: "icon-120.png",
            type: "image/png",
            sizes: "120x120",
          },
          {
            src: "icon-180.png",
            type: "image/png",
            sizes: "180x180",
          },
        ],
      },
    }),
  ],
  server: {
    proxy: {
      "/api": "http://192.168.2.102:80/",
    },
  },
});
