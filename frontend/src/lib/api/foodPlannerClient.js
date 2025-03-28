import {SETTINGS} from "../../settings.js";
import ky from "ky";


const api = ky.create({
    prefixUrl: SETTINGS.API.URL,
    headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    },
    timeout: 10000,
    retry: 2
});

export const getDates = async () => {
    try {
        return await api.get(SETTINGS.API.ENDPOINT.DATES).json();
    } catch (error) {
        console.error("❌ Failed to fetch dates:", error.message);
        return [];
    }
};

export const getMenuPlan = async (menuRequestParams) => {
    try {
        return await api.post(SETTINGS.API.ENDPOINT.MENU, {json: menuRequestParams}).json();
    } catch (error) {
        console.error("❌ Failed to fetch menu:", error.message);
        throw error;
    }
};

