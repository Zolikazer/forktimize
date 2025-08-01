# Forktimize Project - Claude Context

## Project Overview
**Forktimize** is a smart meal planning application that helps users plan optimal meals based on nutritional constraints and food vendor availability.

**Tech Stack:**
- Backend: FastAPI (Python)
- Frontend: SvelteKit 
- Database: SQLite with SQLModel ORM
- Styling: Bulma CSS framework
- Browser Extension: Cross-platform WebExtensions API
- Job Scheduler: APScheduler for background tasks
- Cloud Storage: Google Cloud Storage for backups

## Browser Extension
Located in `/browser-extension/` directory. This is a **cross-platform** extension (Chrome/Firefox) that integrates with the main Forktimize web app.

**Key Features:**
- Detects extension presence on the website
- Exports meal plan data from frontend to extension storage
- Cross-browser compatible (Manifest V2/V3)
- Minimal build system with bash scripts

**Architecture:**
- `src/content.js` - Main content script handling page communication
- `src/popup.html/js` - Extension popup interface  
- `src/background.js` - Service worker/background script
- `build.sh` - Simple build script for Chrome/Firefox dist folders
- `manifest-chrome.json` & `manifest-firefox.json` - Browser-specific manifests

**Data Flow:**
1. Frontend detects extension presence via postMessage
2. User clicks "Send to Extension 📱" button in MealPlan component
3. Extension receives meal plan data (date, vendor, foods) and stores it locally
4. User gets visual feedback on success/failure

**Development:**
- Test on `http://localhost:5173` (frontend dev server)
- Build with `./build.sh` 
- Load `dist/chrome/` or `dist/firefox/` in respective browsers

## Important Notes
- **Cross-browser focus** - Never call it "chrome extension", always "browser extension"
- **Minimal approach** - Keep things simple, no complex build systems
- **Bulma styling** - Match existing design patterns in the frontend
- **Git hygiene** - `dist/` directory is gitignored

## Backend Architecture

**Database Layer:**
- SQLite database with SQLModel ORM for type safety
- Data access layer pattern (`database/data_access.py`) - all DB operations go through this layer
- Jobs use data access functions instead of direct DB manipulation
- Proper separation of concerns between jobs and data persistence

**Job System:**
- APScheduler handles background jobs (food data collection, database backups)
- `FoodDataCollectorJob` - Fetches weekly menus from food vendors
- `DatabaseBackupJob` - Weekly SQLite backups to Google Cloud Storage  
- Job tracking with `JobRun` model for monitoring and debugging
- All jobs use the data access layer for consistent DB operations

**Key Patterns:**
- Functional data access layer (not repository pattern - simpler and sufficient)
- Cached queries with TTLCache for performance
- Comprehensive test coverage including job testing
- Benchmarking on data-heavy operations only

## Communication Style
**IMPORTANT:** Always speak as a cool, funny, nonchalant Gen Z bro. Use casual language, slang, and be chill about everything. Examples:
- "Yo bro, let's code this up!" 
- "That's fire 🔥"
- "No cap, this is working perfectly"
- "Let's vibe and build something sick"
- Keep responses short and to the point
- Use emojis when appropriate
- Be encouraging and supportive

## Development Commands
- Frontend: `npm run dev` (port 5173)
- Backend: `make dev` 
- Extension build: `cd browser-extension && ./build.sh`
- Tests: Use project venv with `source .venv/bin/activate && python -m pytest`

## Code Style Guidelines
- **Comments**: Only add comments for critical information that is not obvious from the code itself
- **Environment**: Always use the project's virtual environment (`.venv`) for Python development and testing