import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

const env = {
  development: 'http://0.0.0.0:5000',
  test: 'http://0.0.0.0:5000',
  production: ''
}
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: env[process.env.NODE_ENV],
        changeOrigin: true,
      },
    },
  },
});
