export const FoodVendor = {
    CITY_FOOD: {label: "Cityfood", value: "cityfood"},
    INTER_FOOD: {label: "Interfood", value: "interfood"},
};
export const foodVendorList = Object.values(FoodVendor);

export function getVendorLabel(value) {
    const match = foodVendorList.find(
        (entry) => entry?.value === value
    );
    return match?.label ?? "Unknown";
}
