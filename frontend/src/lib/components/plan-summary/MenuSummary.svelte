<script>
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import MacroStat from "$lib/components/plan-summary/MacroStat.svelte";
    import MacroRatio from "$lib/components/plan-summary/MacroRatio.svelte";
    import {calculateMacroRatio} from "$lib/utils/macroRatio.js";


    $: macroRatios = calculateMacroRatio({
        protein: $mealPlanStore.totalProtein,
        carbs: $mealPlanStore.totalCarbs,
        fat: $mealPlanStore.totalFat
    });

    $: proteinRatio = macroRatios.proteinRatio;
    $: carbRatio = macroRatios.carbRatio;
    $: fatRatio = macroRatios.fatRatio;

</script>

<div class="card">
    <SectionHeader title="Your Meal Plan Summary" subTitle={"📅" + new Date($mealPlanStore.date).toLocaleDateString("hu-HU", {
            weekday: "long",
            month: "long",
            day: "numeric",
            year: "numeric"
        })}>
        <div class="tags" slot="tags">
            <span class="tag is-success is-light bigger-tag">
                💸 {$mealPlanStore.totalPrice.toLocaleString("fr-FR")} Ft
              </span>
            <span class="tag is-success is-light bigger-tag">
                🔥 {$mealPlanStore.totalCalories.toLocaleString("fr-FR")} calories
              </span>
        </div>
    </SectionHeader>

    <div class="card-content">
        <div class="columns is-mobile is-multiline is-justify-content-center mb-1">
            <div class="column is-one-third">
                <MacroStat
                        icon="protein.png"
                        label="Protein"
                        value={`${$mealPlanStore.totalProtein} g`}
                        subValue={`${proteinRatio}%`}
                        colorClass="danger"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="carb.png"
                        label="Carbs"
                        value={`${$mealPlanStore.totalCarbs} g`}
                        subValue={`${carbRatio}%`}
                        colorClass="success"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="fat.png"
                        label="Fat"
                        value={`${$mealPlanStore.totalFat} g`}
                        subValue={`${fatRatio}%`}
                        colorClass="link"
                />
            </div>

        </div>
        <MacroRatio
                proteinPercentage={proteinRatio}
                carbsPercentage={carbRatio}
                fatPercentage={fatRatio}
                title="Macronutrient Ratio"
        />

    </div>
</div>

