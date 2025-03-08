import {worker} from "./mocks/browser.js";

console.log(import.meta.env.VITE_RUN_MOCK_BACKEND);

if (import.meta.env.MODE === "development" && import.meta.env.VITE_RUN_MOCK_BACKEND === "true") {
    console.log("Starting mock backend worker...");
    console.log(import.meta.env.VITE_RUN_MOCK_BACKEND);
    await worker.start();
}
