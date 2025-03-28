class ConfigManager {
    constructor() {
        this.baseConfig = {
            API: {
                URL: import.meta.env.VITE_API_URL || "https://forktimize.xyz/api",
                ENDPOINT: {
                    DATES: "dates",
                    MENU: "menu",
                }
            },
            RUN_MOCK_BACKEND: false,
            MODE: "production"
        };

        this.isDev = import.meta.env.MODE === "development";

        this.config = this.createConfig();
    }

    createConfig() {
        if (this.isDev) {
            return {
                ...this.baseConfig,
                MODE: "development",
                API: {
                    ...this.baseConfig.API,
                    URL: import.meta.env.VITE_DEV_API_URL || "http://localhost:8000/api"
                },
                RUN_MOCK_BACKEND:
                    import.meta.env.VITE_RUN_MOCK_BACKEND === "true" || false
            };
        }

        return this.baseConfig;
    }
}

export const CONFIG = new ConfigManager().config;

