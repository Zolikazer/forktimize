const PROD_SETTINGS = {
    API: {
        URL: "https://forktimize.xyz/api",
        ENDPOINT: {
            DATES: "dates",
            MENU: "menu",
        },
    },
    RUN_MOCK_BACKEND: false,
    MODE: "production",
};

const DEV_SETTINGS = {
    ...PROD_SETTINGS,
    MODE: "development",
    URL: "http://localhost:8000",
    RUN_MOCK_BACKEND: import.meta.env.VITE_RUN_MOCK_BACKEND || false
}

const isDev = import.meta.env.MODE === "development";
export const SETTINGS = isDev ? DEV_SETTINGS : PROD_SETTINGS;
console.log(SETTINGS);

