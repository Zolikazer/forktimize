<script>
    import InputGroup from "./MacroConstraint.svelte";
    import DateSelector from "./DateSelector.svelte";
    import FoodBlacklist from "./FoodBlacklist.svelte";

    export let minCalories = 1500;
    export let maxCalories = 2500;
    export let minProtein ;
    export let maxProtein ;
    export let minCarbs ;
    export let maxCarbs ;
    export let minFats ;
    export let maxFats;
    export let generateMenu;
</script>

<div class="box">
    <h2 class="title is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Set Your Nutritional Goals</h2>

    <div class="is-flex is-justify-content-center is-flex-wrap-wrap gap-2">
        <InputGroup label="Calories" bind:minValue={minCalories} bind:maxValue={maxCalories} unit="kcal"/>
        <InputGroup label="Protein" bind:minValue={minProtein} bind:maxValue={maxProtein} unit="g"/>
        <InputGroup label="Carbs" bind:minValue={minCarbs} bind:maxValue={maxCarbs} unit="g"/>
        <InputGroup label="Fats" bind:minValue={minFats} bind:maxValue={maxFats} unit="g"/>
    </div>

    <div class="columns is-centered mt-3">
        <div class="column">
            <DateSelector/>
        </div>
        <div class="column">
            <FoodBlacklist/>
        </div>
    </div>


    <div class="has-text-centered">
        <button class="button generate-button is-fullwidth has-text-weight-bold is-rounded is-medium p-3  is-size-5 "
                on:click={generateMenu}>Generate My Menu 🍽️
        </button>
    </div>
</div>

<style>
    .generate-button {
        font-size: 1rem;
        background: #00d1b2;
        /*color: white;*/
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.03);
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.3);
    }
</style>
