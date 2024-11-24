import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import dotenv from "dotenv";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "https://www.koreaexim.go.kr", // 대상 API 서버
        changeOrigin: true, // CORS 우회
        rewrite: (path) => path.replace(/^\/api/, ""), // "/api" 경로 제거
      },
    },
  },

  plugins: [vue()],
});
