export const FoodProvider = {
    CITY_FOOD: {label: "CityFood", value: "CITY_FOOD"},
    INTER_FOOD: {label: "Interfood", value: "INTER_FOOD"},
};
export const foodProviderList = Object.values(FoodProvider);

export function getProviderLabel(value) {
    const match = foodProviderList.find(
        (entry) => entry?.value === value
    );
    return match?.label ?? "Unknown";
}
