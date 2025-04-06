const isDev = import.meta.env.MODE !== "production";

export const CONFIG = {
    MODE: isDev ? "development" : "production",
    API: {
        URL: import.meta.env.VITE_API_URL ?? (
            isDev
                ? "http://localhost:8000/api"
                : "https://forktimize.xyz/api"),
        ENDPOINT: {
            DATES: "dates",
            MEAL_PLAN: "meal-plan",
        },
    },
    RUN_MOCK_BACKEND: isDev
        ? import.meta.env.VITE_RUN_MOCK_BACKEND === "true"
        : false,
    DEFAULT_LOCALE: import.meta.env.VITE_DEFAULT_LOCALE ?? (isDev ? "en" : "hu")
};
