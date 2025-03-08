import {worker} from "./mocks/browser.js";


if (import.meta.env.MODE === "development") {
    await worker.start();
}
