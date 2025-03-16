import {worker} from "./mocks/browser.js";
import {SETTINGS} from "./settings.js";

console.log(import.meta.env.VITE_RUN_MOCK_BACKEND);

if (SETTINGS.MODE === "development" && SETTINGS.RUN_MOCK_BACKEND === "true") {
    console.log("Starting mock backend worker...");
    console.log(SETTINGS.RUN_MOCK_BACKEND);
    await worker.start();
}
