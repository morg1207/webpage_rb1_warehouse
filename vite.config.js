import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: 'https://i-029db135d8e4b81d2.robotigniteacademy.com/742935e8-3664-44ec-978c-1b07a3c4b185/webpage/', // Ajusta esto según tu subdirectorio
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
