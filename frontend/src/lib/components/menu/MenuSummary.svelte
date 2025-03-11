<script>
    import {menu} from "$lib/stores/menuStore.js";

    $: totals = ($menu || []).reduce(
        (acc, food) => {
            acc.cost += food.price || 0;
            acc.calories += food.calories || 0;
            acc.protein += food.protein || 0;
            acc.carbs += food.carb || 0;
            acc.fats += food.fat || 0;
            return acc;
        },
        { cost: 0, calories: 0, protein: 0, carbs: 0, fats: 0 }
    );

    $: formattedCost = totals.cost.toLocaleString("fr-FR");

</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Menu Summary</h2>

    <div class="box-has-shadow has-background-white-ter p-4 is-rounded shadow mt-4 has-text-centered is-size-5 has-text-weight-bold">
        <section class="summary-flex mb-3 border-bottom">
            <div class="summary-item">💰 <strong>Total Cost:</strong> {formattedCost} Ft</div>
            <div class="summary-item">🔥 <strong>Total Calories:</strong> {totals.calories.toLocaleString("fr-FR")} kcal</div>
        </section>
        <section class="summary-flex">
            <div class="summary-item">💪 <strong>Total Protein:</strong> {totals.protein} g</div>
            <div class="summary-item">🥖 <strong>Total Carbs:</strong> {totals.carbs} g</div>
            <div class="summary-item">🧈️ <strong>Total Fats:</strong> {totals.fats} g</div>
        </section>
    </div>
</div>


<style>
    .summary-flex {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .summary-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .border-bottom {
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
