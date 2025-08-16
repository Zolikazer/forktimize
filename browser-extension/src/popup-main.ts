// Main popup entry point - TypeScript version
import { StorageService } from './services/storage-service';
import { PopupService } from './services/popup-service';

// Initialize services and start popup
document.addEventListener('DOMContentLoaded', () => {
  const storageService = new StorageService();
  const popupService = new PopupService(storageService);
  
  popupService.initialize();
});