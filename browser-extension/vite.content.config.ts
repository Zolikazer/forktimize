import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'dist-vite',
    emptyOutDir: false, // Don't clean directory so main build files are preserved
    rollupOptions: {
      input: {
        'content-main': resolve(__dirname, 'src/content-main.ts')
      },
      output: {
        entryFileNames: '[name].js',
        format: 'iife', // IIFE format for content script browser compatibility
        manualChunks: undefined
      },
      external: []
    },
    minify: false,
    sourcemap: true
  }
});