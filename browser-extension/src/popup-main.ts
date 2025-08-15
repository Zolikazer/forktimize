// Main popup entry point - TypeScript version
import { StorageService } from './services/storage-service';
import { MessageService } from './services/message-service';
import { PopupService } from './services/popup-service';

// Initialize services and start popup
document.addEventListener('DOMContentLoaded', () => {
  const storageService = new StorageService();
  const messageService = new MessageService();
  const popupService = new PopupService(storageService, messageService);
  
  popupService.initialize();
});