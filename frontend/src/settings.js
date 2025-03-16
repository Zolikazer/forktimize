const PROD_SETTINGS = {
    API: {
        URL: import.meta.env.VITE_API_URL || "https://forktimize.duckdns.org",
        ENDPOINT: {
            DATES: "dates",
            MENU: "menu",
        },
    },
    RUN_MOCK_BACKEND: import.meta.env.VITE_RUN_MOCK_BACKEND || false,
    MODE: "production",
};

const DEV_SETTINGS = {
    ...PROD_SETTINGS,
    MODE: "development",
    URL: "http://localhost:8000",
}

const isProd = import.meta.env.MODE === "production";
export const SETTINGS = isProd ? PROD_SETTINGS : DEV_SETTINGS;
console.log(SETTINGS);

