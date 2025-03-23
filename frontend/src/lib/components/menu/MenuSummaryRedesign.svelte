<script>
    import SummaryHeader from "$lib/components/menu/summary/SummaryHeader.svelte";
    import MacroRatio from "$lib/components/menu/summary/MacroRatio.svelte";
    import MacroStat from "$lib/components/menu/summary/MacroStat.svelte";
    import {menuStore} from "$lib/stores/menuStore.js";
    import {menuFormStore, selectedDateStore} from "$lib/stores/menuFormStore.js";

    $: totals = ($menuStore.foods || []).reduce(
        (acc, food) => {
            acc.cost += food.price || 0;
            acc.calories += food.calories || 0;
            acc.protein += food.protein || 0;
            acc.carbs += food.carb || 0;
            acc.fats += food.fat || 0;
            return acc;
        },
        {cost: 0, calories: 0, protein: 0, carbs: 0, fats: 0}
    );


    $: proteinKcals = totals.protein * 4;
    $: carbsKcals = totals.carbs * 4;
    $: fatKcals = totals.fats * 9;
    $: totalMacroKcals = proteinKcals + carbsKcals + fatKcals;

    $: formattedCost = totals.cost.toLocaleString("fr-FR");

    $: proteinPercentage =
        totalMacroKcals > 0 ? ((proteinKcals / totalMacroKcals) * 100).toFixed(0) : 0;
    $: carbsPercentage =
        totalMacroKcals > 0 ? ((carbsKcals / totalMacroKcals) * 100).toFixed(0) : 0;
    $: fatPercentage =
        totalMacroKcals > 0 ? ((fatKcals / totalMacroKcals) * 100).toFixed(0) : 0;


</script>

<div class="card">
    <SummaryHeader
            title="Your Menu Summary"
            planDate={$selectedDateStore}
            totalCalories={totals.calories}
            totalPrice={totals.cost}
    />
    <div class="card-content">
        <div class="columns is-mobile is-multiline is-justify-content-center mb-1">
            <div class="column is-one-third">
                <MacroStat
                        icon="💪"
                        label="Protein"
                        value={`${totals.protein} g`}
                        subValue={`${proteinPercentage}%`}
                        colorClass="danger"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="🥖"
                        label="Carbs"
                        value={`${totals.carbs} g`}
                        subValue={`${carbsPercentage}%`}
                        colorClass="success"
                />
            </div>

            <div class="column is-one-third">
                <MacroStat
                        icon="🧈"
                        label="Fat"
                        value={`${totals.fats} g`}
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
