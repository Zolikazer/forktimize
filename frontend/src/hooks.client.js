
import {worker} from "./mocks/browser.js";

console.log("anyad");

if (import.meta.env.MODE === "development") {
    worker.start();
    console.log("Mock service worker started");
}
