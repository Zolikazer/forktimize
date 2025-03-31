export const FoodProvider = {
    CITY_FOOD: {label: "Cityfood", value: "cityfood"},
    INTER_FOOD: {label: "Interfood", value: "interfood"},
};
export const foodProviderList = Object.values(FoodProvider);

export function getProviderLabel(value) {
    const match = foodProviderList.find(
        (entry) => entry?.value === value
    );
    return match?.label ?? "Unknown";
}
