import {worker} from "./lib/mocks/browser.js";
import {CONFIG} from "./lib/config/config.js";

console.log(import.meta.env.VITE_RUN_MOCK_BACKEND);

if (CONFIG.MODE === "development" && CONFIG.RUN_MOCK_BACKEND === "true") {
    console.log("Starting mock backend worker...");
    await worker.start();
}

export function handleError({ error, event }) {
    console.error('CLIENT error happened:', error);
}

export function init() {
    console.log('Client app initializing...');
}
