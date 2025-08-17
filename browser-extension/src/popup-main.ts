// Main popup entry point - Functional approach
import { StorageService } from './services/storage-service';
import { initializePopup } from './services/popup-service';

// Initialize popup with functional approach
document.addEventListener('DOMContentLoaded', () => {
  const storageService = new StorageService();
  initializePopup(storageService);
});