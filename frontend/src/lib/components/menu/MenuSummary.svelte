<script>
    import {menu} from "$lib/stores/menuStore.js";

</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Menu Summary</h2>

    <div class="box-has-shadow has-background-white-ter p-4 is-rounded shadow mt-4 has-text-centered is-size-5 has-text-weight-bold">
        <section class="summary-flex mb-3 border-bottom">
            <div class="summary-item">💰 <strong>Total Cost:</strong>
                {$menu.reduce((sum, food) => sum + food.price, 0).toLocaleString('fr-FR')} Ft</div>
            <div class="summary-item">🔥 <strong>Total
                Calories:</strong> {$menu.reduce((sum, food) => sum + food.kcal, 0).toLocaleString('fr-FR')} kcal
            </div>
        </section>
        <section class="summary-flex">
            <div class="summary-item">💪 <strong>Total
                Protein:</strong> {$menu.reduce((sum, food) => sum + food.protein, 0)} g
            </div>
            <div class="summary-item">🥖 <strong>Total
                Carbs:</strong> {$menu.reduce((sum, food) => sum + food.carbs, 0)} g
            </div>
            <div class="summary-item">🧈️ <strong>Total
                Fats:</strong> {$menu.reduce((sum, food) => sum + food.fat, 0)} g
            </div>
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
