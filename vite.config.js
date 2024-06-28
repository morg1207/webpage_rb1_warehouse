import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: 'https://i-01ebf83cc257f3d4a.robotigniteacademy.com/dc2e8c83-4da7-4efa-aadf-a7a9bd362123/webpage/', // Ajusta esto según tu subdirectorio
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
