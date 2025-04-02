<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import {menuRequestStore} from "$lib/stores/menuRequestStore.js";
    import {FoodProvider} from "$lib/forktimize/foodProviders.js";

    const MAX_FOOD_LENGTH = 42;

    export let food;

    function removeFood(foodName) {
        updateDislikedFoods(foodName);
        updateMenu(foodName);
    }

    function updateDislikedFoods(foodName) {
        menuRequestStore.addDislikedFood(foodName);
    }

    function updateMenu(foodName) {
        menuStore.removeFood(foodName);
    }


    function getShortenedName(name) {
        return name.length > MAX_FOOD_LENGTH ? name.substring(0, MAX_FOOD_LENGTH) + "..." : name;
    }

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

<div class="card food-card mx-auto is-flex is-flex-direction-column">
    <div class="card-image">
        <figure class="image is-16by9">
            {#if $menuStore.foodProvider === FoodProvider.CITY_FOOD.value}
                <img alt={food.name}
                     src={`https://ca.cityfood.hu/api/v1/i?menu_item_id=${food.foodId}&width=425&height=425`}/>
            {:else if $menuStore.foodProvider === FoodProvider.INTER_FOOD.value}
                <img alt={food.name}
                     src={`https://ia.interfood.hu/api/v1/i?menu_item_id=${food.foodId}&width=425&height=425`}/>
            {:else}
                <img alt={food.name}
                     src={`https://ia.interfood.hu/api/v1/i?menu_item_id=98529&width=425&height=425`}/>
            {/if}
        </figure>
    </div>
    <div class="card-content">
        <div class="media mb-1">
            <div class="media-content">
                <p class="title is-6 food-name" data-tooltip={food.name}>{getShortenedName(food.name)}</p>
                <p class="subtitle is-7">{food.price} Ft</p>
            </div>
        </div>

        <div class="is-flex mt-3 pt-3" style="border-top: 1px solid rgba(0, 0, 0, 0.1);">
            <div class="is-flex is-justify-content-center is-align-items-center" style="width: 70px;">
                <div class="calories-circle">
                    <span class="has-text-weight-bold" style="font-size: 1.1rem; line-height: 1;">{food.calories}</span>
                    <span style="font-size: 0.7rem; opacity: 0.9;">kcal</span>
                </div>
            </div>

            <div class="is-flex-grow-1 ml-3 is-flex is-flex-direction-column is-justify-content-space-between">
                <div class="mb-2">
                    <div class="is-flex is-align-items-center mb-1">
                        <span class="mr-1">💪</span>
                        <span class="is-flex-grow-1 is-size-7">Fehérje</span>
                        <span class="has-text-weight-bold is-size-7">{food.protein}g</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill has-background-info" style="width: {proteinPercentage}%"></div>
                    </div>
                </div>

                <div class="mb-2">
                    <div class="is-flex is-align-items-center mb-1">
                        <span class="mr-1">🥖</span>
                        <span class="is-flex-grow-1 is-size-7">Szénhidrát</span>
                        <span class="has-text-weight-bold is-size-7">{food.carb}g</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill has-background-danger" style="width: {carbsPercentage}%"></div>
                    </div>
                </div>

                <div class="mb-2">
                    <div class="is-flex is-align-items-center mb-1">
                        <span class="mr-1">🧈</span>
                        <span class="is-flex-grow-1 is-size-7">Zsír</span>
                        <span class="has-text-weight-bold is-size-7">{food.fat}g</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill has-background-warning" style="width: {fatPercentage}%"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <button class="button is-danger is-light mt-auto mb-3 custom-button" on:click={() => removeFood(food.name)}>
        🤮 Nem szeretem
    </button>
</div>

<style>
    .food-card {
        width: 30%;
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out;
        min-width: 200px;
    }

    .food-card:hover {
        transform: scale(1.03);
    }

    .media-content p {
        margin: 0;
    }

    .custom-button {
        width: auto;
        min-width: 150px;
        align-self: center;
    }

    .food-name {
        cursor: pointer;
        position: relative;
        display: inline-block;
    }

    .food-name:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        left: 50%;
        bottom: 120%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        white-space: normal;
        width: max-content;
        max-width: 250px;
        text-align: center;
        z-index: 10;
        opacity: 1;
        transition: opacity 0.2s ease-in-out;
        line-height: 1.4;
        word-break: normal;
        overflow-wrap: break-word;
    }

    .macro-container {
        display: flex;
        margin-top: 0.75rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    .calories-display {
        width: 70px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .calories-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d1b2, #4adbc5);
        color: black;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .calories-value {
        font-size: 1.1rem;
        font-weight: bold;
        line-height: 1;
    }

    .calories-unit {
        font-size: 0.7rem;
        opacity: 0.9;
    }

    .macro-details {
        flex: 1;
        margin-left: 0.75rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .macro-item {
        margin-bottom: 0.5rem;
    }

    .macro-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.2rem;
    }

    .macro-icon {
        margin-right: 0.3rem;
        font-size: 0.9rem;
    }

    .macro-label {
        flex: 1;
        font-size: 0.8rem;
    }

    .macro-value {
        font-weight: bold;
        font-size: 0.8rem;
    }

    .progress-bar {
        height: 6px;
        background-color: #f0f0f0;
        border-radius: 3px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 3px;
    }
</style>
