<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import {menuRequestStore} from "$lib/stores/menuRequestStore.js";
    import {FoodProvider} from "$lib/constants/foodProviders.js";

    const MAX_FOOD_LENGTH = 42;

    export let food;
    console.log($menuStore)

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

</script>

<div class="card food-card mx-auto is-flex is-flex-direction-column">
    <div class="card-image">
        <figure class="image is-16by9">
            {#if $menuStore.foodProvider === FoodProvider.CITY_FOOD.value}
                <img alt="Placeholder image"
                     src={`https://ca.cityfood.hu/api/v1/i?menu_item_id=${food.foodId}&width=425&height=425`}/>
            {:else if $menuStore.foodProvider === FoodProvider.INTER_FOOD.value}
                <img alt="Placeholder image"
                     src={`https://ia.interfood.hu/api/v1/i?menu_item_id=${food.foodId}&width=425&height=425`}/>
            {:else}
                <img alt="Placeholder image"
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

        <div class="columns is-centered">
            <div class="column is-flex is-flex-wrap-wrap">
                <div class="subtitle is-7 mb-1"><strong>🔥 {food.calories}</strong> kcal</div>
                <div class="subtitle is-7"><strong>💪 {food.protein}</strong> g fehérje</div>
            </div>
            <div class="column is-flex is-flex-wrap-wrap">
                <div class="subtitle is-7 mb-1"><strong>🥖 {food.carb}</strong> g szénhidrát</div>
                <div class="subtitle is-7"><strong>🧈️ {food.fat}</strong> g zsír</div>
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

</style>
