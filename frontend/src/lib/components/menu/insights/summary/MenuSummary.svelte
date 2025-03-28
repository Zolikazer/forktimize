<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import MacroStat from "$lib/components/menu/insights/summary/MacroStat.svelte";
    import MacroRatio from "$lib/components/menu/insights/summary/MacroRatio.svelte";


    $: proteinKcals = $menuStore.totalProtein * 4;
    $: carbsKcals = $menuStore.totalCarbs * 4;
    $: fatKcals = $menuStore.totalFat * 9;
    $: totalMacroKcals = proteinKcals + carbsKcals + fatKcals;

    $: proteinPercentage =
        totalMacroKcals > 0 ? ((proteinKcals / totalMacroKcals) * 100).toFixed(0) : 0;
    $: carbsPercentage =
        totalMacroKcals > 0 ? ((carbsKcals / totalMacroKcals) * 100).toFixed(0) : 0;
    $: fatPercentage =
        totalMacroKcals > 0 ? ((fatKcals / totalMacroKcals) * 100).toFixed(0) : 0;


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
                        icon="💪"
                        label="Protein"
                        value={`${$menuStore.totalProtein} g`}
                        subValue={`${proteinPercentage}%`}
                        colorClass="danger"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="🥖"
                        label="Carbs"
                        value={`${$menuStore.totalCarbs} g`}
                        subValue={`${carbsPercentage}%`}
                        colorClass="success"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="🧈"
                        label="Fat"
                        value={`${$menuStore.totalFat} g`}
                        subValue={`${fatPercentage}%`}
                        colorClass="link"
                />
            </div>

        </div>
        <MacroRatio
                proteinPercentage={proteinPercentage}
                carbsPercentage={carbsPercentage}
                fatPercentage={fatPercentage}
                title="Macronutrient Ratio"
        />

    </div>
</div>

