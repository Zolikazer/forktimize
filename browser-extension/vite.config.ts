import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'dist-vite',
    rollupOptions: {
      input: {
        'popup-main': resolve(__dirname, 'src/popup-main.ts'),
        'background': resolve(__dirname, 'src/background.ts')
      },
      output: {
        entryFileNames: '[name].js',
        format: 'es', // ES modules for MV3
        manualChunks: undefined
      },
      external: []
    },
    minify: false,
    sourcemap: true
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./test-setup.ts']
  }
});
