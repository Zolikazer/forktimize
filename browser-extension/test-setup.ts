// Test setup - silence console logs during tests
import { beforeEach, vi } from 'vitest';

beforeEach(() => {
  // Mock console methods to avoid cluttering test output
  vi.spyOn(console, 'error').mockImplementation(() => {});
  vi.spyOn(console, 'warn').mockImplementation(() => {});
  vi.spyOn(console, 'log').mockImplementation(() => {});
});