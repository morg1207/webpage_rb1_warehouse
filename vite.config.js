import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: 'https://i-0f893e6d62e302604.robotigniteacademy.com/32eaba10-6d44-44e7-8ddc-4d07498616e7/webpage/', // Ajusta esto según tu subdirectorio
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/launch': {
        target: 'http://127.0.0.1:7000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/launch/, '/launch')
      },
      '/stop': {
        target: 'http://127.0.0.1:7000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/stop/, '/stop')
      },
    },
  },
})
