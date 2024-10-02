import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from 'tailwindcss';
import terser from '@rollup/plugin-terser';

const env: Record<'development' | 'test' | 'production', string> = {
  development: 'http://127.0.0.1:5000',
  test: 'http://0.0.0.0:5000',
  production: 'https://www.eduresource.tech',
};
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: env[mode as 'development' | 'test' | 'production'],
        changeOrigin: true,
      },
    },
  },
  build: {
    assetsInlineLimit: 4096,
    sourcemap: mode !== 'production',
    rollupOptions: {
      plugins:
        mode === 'production'
          ? [
              terser({
                compress: {
                  drop_console: true,
                  drop_debugger: true,
                },
                output: {
                  comments: false,
                },
                mangle: {
                  toplevel: true,
                },
              }),
            ]
          : [],
    },
  },
}));
