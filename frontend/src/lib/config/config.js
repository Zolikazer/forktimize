const isDev = import.meta.env.MODE === "development";

export const CONFIG = {
    MODE: isDev ? "development" : "production",
    API: {
        URL: isDev
            ? import.meta.env.VITE_API_URL || "http://localhost:8000/api"
            : import.meta.env.VITE_API_URL || "https://forktimize.xyz/api",
        ENDPOINT: {
            DATES: "dates",
            MENU: "menu",
        },
    },
    RUN_MOCK_BACKEND: isDev
        ? import.meta.env.VITE_RUN_MOCK_BACKEND === "true"
        : false,
};
