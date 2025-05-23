import { fileURLToPath, URL } from 'url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: '', 
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '^/api/.*': {
        target: 'http://127.0.0.1:8080', 
        changeOrigin: true,
        rewrite: (path) => path, 
      }
    }
  },
  build: {
    outDir: 'app/static',
    emptyOutDir: true
  }
});
