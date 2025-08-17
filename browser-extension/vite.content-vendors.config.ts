import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'dist',
    emptyOutDir: false,
    rollupOptions: {
      input: resolve(__dirname, 'src/content-vendors.ts'),
      output: {
        entryFileNames: 'content-vendors.js',
        format: 'iife',
        manualChunks: undefined
      },
      external: []
    },
    minify: false,
    sourcemap: true
  }
});