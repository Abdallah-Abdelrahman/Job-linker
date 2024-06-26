import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "tailwindcss";

const env = {
  development: "http://127.0.0.1:5000",
  test: "http://0.0.0.0:5000",
  production: "https://www.eduresource.tech",
};
// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: env[process.env.NODE_ENV],
        changeOrigin: true,
      },
    },
  },
});
