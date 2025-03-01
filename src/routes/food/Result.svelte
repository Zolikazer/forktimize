<script>
    export let menu = [];
</script>

<style>
    /* Stylish box for the entire results section */

    /* Box for summary totals */
    .summary-box {
        margin-top: 1.5rem;
        padding: 1rem;
        border-radius: 12px;
        background: #f8f9fa;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }

    /* Flexbox for inline totals */
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
    .title {
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
</style>

{#if menu.length}
<!--        <div class="container">-->
            <!-- Boxed Results Section -->
            <div class="box">
                <h2 class="title has-text-centered">Your Custom Menu</h2>

                <table class="table is-fullwidth is-striped is-hoverable">
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

                <!-- Inline Summary Box -->
                <div class="summary-box">
                    <div class="summary-flex">
                        <div class="summary-item">📊 <strong>Total Calories:</strong> {menu.reduce((sum, food) => sum + food.calories, 0)} kcal</div>
                        <div class="summary-item">💪 <strong>Total Protein:</strong> {menu.reduce((sum, food) => sum + food.protein, 0)} g</div>
                        <div class="summary-item">🥖 <strong>Total Carbs:</strong> {menu.reduce((sum, food) => sum + food.carbs, 0)} g</div>
                        <div class="summary-item">🛢️ <strong>Total Fats:</strong> {menu.reduce((sum, food) => sum + food.fats, 0)} g</div>
                        <div class="summary-item">💰 <strong>Total Cost:</strong> ${menu.reduce((sum, food) => sum + food.price, 0).toFixed(2)}</div>
                    </div>
                </div>
            </div>
<!--        </div>-->
{/if}
