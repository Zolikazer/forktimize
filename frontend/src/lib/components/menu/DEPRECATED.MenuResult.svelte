<script>
    import {dislikedFoods} from "$lib/stores/dislikedFoodsStore.js";

    export let menu = [];

    function removeFood(foodName) {
        menu = menu.filter(food => food.name !== foodName); // Remove from menu
        dislikedFoods.update(foods => [...foods, foodName]); // Add to disliked foods
    }
</script>

<h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Custom Menu</h2>

<table class="table is-fullwidth is-hoverable">
    <thead>
    <tr>
        <th>Food</th>
        <th>Calories</th>
        <th>Protein</th>
        <th>Carbs</th>
        <th>Fats</th>
        <th>Price</th>
<!--        <th>Nem Szereted?</th>-->
    </tr>
    </thead>
    <tbody>
    {#each menu as food}
        <tr>
            <td>{food.name}</td>
            <td>{food.calories} kcal</td>
            <td>{food.protein} g</td>
            <td>{food.carbs} g</td>
            <td>{food.fats} g</td>
            <td>{food.price} Ft</td>
<!--            <td>-->
<!--                <button class="button is-small is-danger is-light delete-button"-->
<!--                        on:click={() => removeFood(food.name)}><span class="emoji">🤮</span>-->
<!--                </button></td>-->
        </tr>
    {/each}
    </tbody>
</table>

<div class="box-has-shadow has-background-white-ter p-4 is-rounded shadow mt-4 has-text-centered is-size-5 has-text-weight-bold">
    <section class="summary-flex mb-3 border-bottom">
        <div class="summary-item">💰 <strong>Total Cost:</strong>
            ${menu.reduce((sum, food) => sum + food.price, 0).toFixed(2)}</div>
        <div class="summary-item">🔥 <strong>Total
            Calories:</strong> {menu.reduce((sum, food) => sum + food.calories, 0)} kcal
        </div>
    </section>
    <section class="summary-flex">
        <div class="summary-item">💪 <strong>Total
            Protein:</strong> {menu.reduce((sum, food) => sum + food.protein, 0)} g
        </div>
        <div class="summary-item">🥖 <strong>Total
            Carbs:</strong> {menu.reduce((sum, food) => sum + food.carbs, 0)} g
        </div>
        <div class="summary-item">🧈️ <strong>Total
            Fats:</strong> {menu.reduce((sum, food) => sum + food.fats, 0)} g
        </div>
    </section>
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

    .delete-button:hover {
        transform: scale(1.4);
    }

    .emoji {
        font-size: 0.7rem; /* Slightly larger emoji */
    }
</style>
