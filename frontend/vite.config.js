import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    // fake browser so components can render in tests
    environment: 'jsdom',
    // lets testing library clean up the page after each test
    globals: true,
  },
})
