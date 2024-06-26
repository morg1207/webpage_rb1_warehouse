import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  //base: 'https://i-02df1cb82257f6d78.robotigniteacademy.com/e3127762-2c05-4387-9eb2-56d21cbf0ec3/webpage/', // Ajusta esto según tu subdirectorio
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
