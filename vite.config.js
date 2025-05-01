import { fileURLToPath, URL } from 'url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Directly set the Render API URL
const API_URL = 'https://https://info3180-project-lof1.onrender.com/'; // Your deployed Render backend URL

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '^/api/.*': {
        target: API_URL,  // Directly use the Render API URL
        changeOrigin: true,
        rewrite: (path) => path, 
      }
    }
  }
});
