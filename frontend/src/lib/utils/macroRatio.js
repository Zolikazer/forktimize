export function calculateMacroRatio({ protein, carbs, fat }) {
    const proteinKcals = protein * 4;
    const carbsKcals = carbs * 4;
    const fatKcals = fat * 9;

    const totalMacroKcals = proteinKcals + carbsKcals + fatKcals;

    const safePercentage = (kcal) =>
        totalMacroKcals > 0 ? ((kcal / totalMacroKcals) * 100).toFixed(0) : 0;

    return {
        proteinRatio: safePercentage(proteinKcals),
        carbRatio: safePercentage(carbsKcals),
        fatRatio: safePercentage(fatKcals)
    };
}
