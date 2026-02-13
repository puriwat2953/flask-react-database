import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true, 
    environment: 'jsdom',                   // รันเทสแบบไม่มี browser
    setupFiles: './src/setupTests.js',      // ระบุโค้ดสำหรับเตรียมต่าง ๆ
  },
})
