// TypeScript content script - functional orchestration with dependency injection
import { StorageService } from './services/storage-service';
import { MessageService } from './services/message-service';
import { CartService } from './services/cart-service';
import { DomService } from './services/dom-service';
import { setupContentScript } from './content-orchestrator';

// Inline constants for content script IIFE build (matching working JS version)
const CITYFOOD_SELECTORS = {
  FOOD_TITLE: '.food-top-title',
  FOOD_CONTAINER: '.food',
  CATEGORY: '.category',
  DATE_BUTTON: '.date-button',
  ADD_BUTTON: 'button[aria-label*="Kosárhoz adás:"]'
} as const;

const VENDOR_SITES = {
  cityfood: 'rendel.cityfood.hu'
} as const;

console.log('TypeScript content script loaded on:', window.location.hostname);

// Create service instances
const storageService = new StorageService();
const messageService = new MessageService();
const domService = new DomService(CITYFOOD_SELECTORS);
const cartService = new CartService(
  domService, 
  storageService, 
  {
    hostname: VENDOR_SITES.cityfood,
    selectors: CITYFOOD_SELECTORS,
    name: 'CityFood'
  }
);

// Setup content script with dependency injection
setupContentScript(cartService, messageService, storageService);