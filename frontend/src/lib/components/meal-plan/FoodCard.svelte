<script>
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
    import Macro from "$lib/components/meal-plan/Macro.svelte";
    import {calculateMacroRatio} from "$lib/utils/macroRatio.js";
    import {t} from "$lib/stores/localeStore.js";


    export let food;

    const maxFoodLength = 42;
    $: imageSrc = getImageUrl(food.foodId, $mealPlanStore.foodVendor);
    const fallbackImageSrc = "fallback-food-image.png";

    let triedImageFallback = false;

    function removeFood(foodName) {
        updateDislikedFoods(foodName);
        updateMealPlan(foodName);
    }

    function updateDislikedFoods(foodName) {
        mealPlanRequestStore.addDislikedFood(foodName);
    }

    function updateMealPlan(foodName) {
        mealPlanStore.removeFood(foodName);
    }


    function getShortenedName(name) {
        return name.length > maxFoodLength ? name.substring(0, maxFoodLength) + "..." : name;
    }

    function getImageUrl(foodId, vendor) {
        return `https://forktimize.xyz/images/${vendor}_${foodId}`
    }

    function handleImageError() {
        if (!triedImageFallback) {
            imageSrc = fallbackImageSrc;
            triedImageFallback = true;
        }
    }

    $: macroRatios = calculateMacroRatio({
        protein: $mealPlanStore.totalProtein,
        carbs: $mealPlanStore.totalCarbs,
        fat: $mealPlanStore.totalFat
    });

    $: proteinRatio = macroRatios.proteinRatio;
    $: carbRatio = macroRatios.carbRatio;
    $: fatRatio = macroRatios.fatRatio;


</script>

<div class="card food-card mx-auto is-flex is-flex-direction-column has-radius-large">
    <div class="card-image">
        <figure class="image is-16by9">
            <img alt={food.name}
                 src={imageSrc}
                 on:error={handleImageError}
            />
        </figure>
    </div>
    <div class="card-content">
        <div class="media mb-1">
            <div class="media-content m-0">
                <p class="title food-name is-6 is-inline-block is-relative is-clickable"
                   data-tooltip={food.name}>{getShortenedName(food.name)}</p>
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
                <Macro macroName={$t.macro.protein()}
                       macroValue={food.protein}
                       macroRatio={proteinRatio}
                       ratioColorClass="has-background-info"/>
                <Macro macroName={$t.macro.carbohydrate()}
                       macroValue={food.carb}
                       macroRatio={carbRatio}
                       ratioColorClass="has-background-danger"/>
                <Macro macroName={$t.macro.fat()}
                       macroValue={food.fat}
                       macroRatio={fatRatio}
                       ratioColorClass="has-background-warning"/>

            </div>
        </div>
    </div>
    <button class="button is-danger is-light mt-auto mb-3 custom-button" on:click={() => removeFood(food.name)}>
        🚫 {$t.mealPlan.dontLike()}
    </button>
</div>

<style>
    .food-card {
        width: 30%;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out;
        min-width: 200px;
    }

    .food-card:hover {
        transform: scale(1.03);
    }

    .custom-button {
        width: auto;
        min-width: 150px;
        align-self: center;
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
</style>
