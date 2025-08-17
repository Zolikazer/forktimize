# Forktimize Browser Extension - Claude Context

## Overview
Cross-platform browser extension (Chrome/Firefox) that integrates with the main Forktimize web app for meal planning workflow optimization.

## 🚀 Architecture Vision

### Service Layer Architecture (TypeScript)
**Philosophy**: Clean separation of concerns using ES6 classes with explicit dependencies and pure utility functions.

**Service Structure:**
```
src/services/
├── storage-service.ts       # ✅ Meal plan storage abstraction
├── storage-service.test.ts  # ✅ Co-located tests
├── dom-service.ts           # 🚧 DOM utilities (find, click, validate)
├── cart-service.ts          # 🚧 Cart automation business logic
└── browser-messaging.ts       # 🚧 Popup ↔ content communication
```

**Dependency Flow:**
```
MessageService (orchestrator)
    ↓
CartService (business logic)
    ↓ uses
DomService + StorageService (utilities)
```

**Technology Stack:**
- **TypeScript** for type safety and better developer experience
- **Vite** for modern build pipeline with hot reload
- **Vitest** for fast unit testing with mocking
- **ES6 Classes** for services with private methods
- **Pure functions** for utilities (validation, DOM queries)

### 🎯 Current Implementation Status

#### ✅ Completed Features
- **Multi-day storage**: Extension stores meal plans by date instead of overriding
- **Cross-browser compatibility**: Works on both Chrome and Firefox  
- **Frontend integration**: "Send to Extension 📱" button in MealPlan component
- **Auto-cart functionality**: Working CityFood cart automation with validation
- **Clean popup UI**: Displays meal plans with auto-cart buttons
- **Real-time updates**: Popup refreshes automatically when new plans are added
- **Modern build system**: Vite + TypeScript with testing setup
- **Service architecture**: StorageService with comprehensive tests

#### 🚧 Legacy JavaScript (Working, but needs migration)
- **content.js**: Message handling & auto-cart logic (needs service extraction)
- **popup.js**: UI management with ButtonStateManager (partially refactored)
- **constants.js**: Shared constants (migrated to TypeScript)

### 🔄 Migration Strategy

**Phase 1: Service Layer** *(Current)*
1. ✅ `storage-service.ts` - Clean storage abstraction
2. 🚧 `dom-service.ts` - Extract DOM utilities from content.js
3. 🚧 `cart-service.ts` - Extract auto-cart business logic
4. 🚧 `browser-messaging.ts` - Clean popup ↔ content communication

**Phase 2: Integration**
- Gradually replace legacy JS with TypeScript services
- Maintain backward compatibility during transition
- Keep dual build system (bash + Vite) until migration complete

**Phase 3: Multi-vendor Support**
- Vendor abstraction layer for different food sites
- InterFood, Teletal, eFood support

## 🛠️ Development Commands

### Legacy Build (JavaScript)
```bash
./build.sh                    # Cross-browser extension build
npm run dev:firefox          # Test in Firefox
npm run dev:chrome           # Instructions for Chrome
```

### Modern Build (TypeScript)
```bash
npm run build:vite           # TypeScript compilation
npm run dev                  # Watch mode for development
npm run test                 # Run all tests in watch mode
npm run test:run             # Run tests once
npm run type-check           # TypeScript validation
```

## 📋 Development Standards

### File Naming
- **Services**: `kebab-case.ts` (e.g., `storage-service.ts`)
- **Tests**: Co-located with `.test.ts` suffix (e.g., `storage-service.test.ts`)
- **Classes**: ES6 classes with `private` methods and parameter properties
- **Types**: Export interfaces for public APIs

### Code Style
- **Explicit dependencies**: Services inject dependencies via constructor
- **Pure utilities**: Functions with no side effects for DOM/validation
- **Type safety**: Full TypeScript coverage with proper interfaces
- **Test coverage**: Comprehensive tests for all service methods

### Communication Style
- Casual, friendly Gen Z tone with emojis 🔥
- Short, direct responses  
- Focus on getting things done
- Use "bro" and casual language

### Commit Message Guidelines
- Keep commit messages concise: maximum 7 lines total
- Focus on what changed, not why (unless critical)
- Avoid overly detailed explanations in commit messages

## 🎯 Next Steps
1. **dom-service.ts** - Extract DOM utilities from content.js
2. **cart-service.ts** - Extract auto-cart business logic  
3. **browser-messaging.ts** - Clean popup ↔ content communication
4. **Integration** - Replace legacy JS with TypeScript services
5. **Multi-vendor** - Add InterFood, Teletal, eFood support
