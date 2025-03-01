<script>
    import Help from "./Help.svelte";

    export let menu = [];
</script>

<div class="box">
    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Custom Menu</h2>
    {#if menu.length}

        <table class="table is-fullwidth is-hoverable">
            <thead>
            <tr>
                <th>Food</th>
                <th>Calories</th>
                <th>Protein (g)</th>
                <th>Carbs (g)</th>
                <th>Fats (g)</th>
                <th>Price ($)</th>
            </tr>
            </thead>
            <tbody>
            {#each menu as food}
                <tr>
                    <td>{food.name}</td>
                    <td>{food.calories}</td>
                    <td>{food.protein}</td>
                    <td>{food.carbs}</td>
                    <td>{food.fats}</td>
                    <td>${food.price.toFixed(2)}</td>
                </tr>
            {/each}
            </tbody>
        </table>

        <div class="box-has-shadow has-background-white-ter p-4 is-rounded shadow mt-4 has-text-centered is-size-5 has-text-weight-bold">
            <section class="summary-flex mb-3 border-bottom">
                <div class="summary-item">💰 <strong>Total Cost:</strong>
                    ${menu.reduce((sum, food) => sum + food.price, 0).toFixed(2)}</div>
                <div class="summary-item">📊 <strong>Total
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
                <div class="summary-item">🛢️ <strong>Total
                    Fats:</strong> {menu.reduce((sum, food) => sum + food.fats, 0)} g
                </div>
            </section>
        </div>
    {:else}
        <div class="notification is-info has-text-centered">
            No menu generated yet. Click <strong>"Generate My Menu"</strong> to get started! 🚀
        </div>
        <Help/>
    {/if}
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
