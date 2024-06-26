import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: 'https://i-0ff0db19ba20cbe8c.robotigniteacademy.com/0cb5f084-6a48-452c-a23e-26ce4be72f7e/webpage/', // Ajusta esto según tu subdirectorio
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
