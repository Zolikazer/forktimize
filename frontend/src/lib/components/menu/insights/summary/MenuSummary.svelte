<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import MacroStat from "$lib/components/menu/insights/summary/MacroStat.svelte";
    import MacroRatio from "$lib/components/menu/insights/summary/MacroRatio.svelte";
    import {calculateMacroRatio} from "$lib/utils/macroRatio.js";


    $: macroRatios = calculateMacroRatio({
        protein: $menuStore.totalProtein,
        carbs: $menuStore.totalCarbs,
        fat: $menuStore.totalFat
    });

    $: proteinRatio = macroRatios.proteinRatio;
    $: carbRatio = macroRatios.carbRatio;
    $: fatRatio = macroRatios.fatRatio;

</script>

<div class="card">
    <SectionHeader title="Your Meal Plan Summary" subTitle={"📅" + new Date($menuStore.date).toLocaleDateString("hu-HU", {
            weekday: "long",
            month: "long",
            day: "numeric",
            year: "numeric"
        })}>
        <div class="tags" slot="tags">
            <span class="tag is-success is-light bigger-tag">
                💸 {$menuStore.totalPrice.toLocaleString("fr-FR")} Ft
              </span>
            <span class="tag is-success is-light bigger-tag">
                🔥 {$menuStore.totalCalories.toLocaleString("fr-FR")} calories
              </span>
        </div>
    </SectionHeader>

    <div class="card-content">
        <div class="columns is-mobile is-multiline is-justify-content-center mb-1">
            <div class="column is-one-third">
                <MacroStat
                        icon="protein.png"
                        label="Protein"
                        value={`${$menuStore.totalProtein} g`}
                        subValue={`${proteinRatio}%`}
                        colorClass="danger"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="carb.png"
                        label="Carbs"
                        value={`${$menuStore.totalCarbs} g`}
                        subValue={`${carbRatio}%`}
                        colorClass="success"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="fat.png"
                        label="Fat"
                        value={`${$menuStore.totalFat} g`}
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

