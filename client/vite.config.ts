import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [react(), VitePWA({
    includeManifestIcons: true,
    manifest: {
      name: "Office Lights",
      short_name: "Office Lights",
      icons: [
        {
          "src": "icon-256.png",
          "sizes": "256x256",
          "type": "image/png"
        },
        {
          "src": "icon-120.png",
          "sizes": "120x120",
          "type": "image/png"
        },
        {
          "src": "icon-180.png",
          "sizes": "180x180",
          "type": "image/png"
        },
        {
          "src": "icon-192.png",
          "sizes": "192x192",
          "type": "image/png"
        },
        {
          "src": "icon-64.png",
          "sizes": "64x64",
          "type": "image/png"
        }
      ],
    }
  })],
  server: {
    proxy: {
      "/api": "http://192.168.2.102:80/",
    },
  },
});
