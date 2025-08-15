import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'dist-vite',
    rollupOptions: {
      input: {
        content: resolve(__dirname, 'src/content.ts'),
        'popup-main': resolve(__dirname, 'src/popup-main.ts'),
        background: resolve(__dirname, 'src/background.ts'),
        constants: resolve(__dirname, 'src/constants.ts')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    },
    minify: false, // Keep readable for debugging
    sourcemap: true
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./test-setup.ts']
  }
});