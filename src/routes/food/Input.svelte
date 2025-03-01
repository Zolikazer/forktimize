<script>
    import InputGroup from "./InputGroup.svelte";

    export let minCalories = 1500;
    export let maxCalories = 2500;
    export let minProtein = 50;
    export let maxProtein = 150;
    export let minCarbs = 100;
    export let maxCarbs = 300;
    export let minFats = 20;
    export let maxFats = 80;
    export let generateMenu;
</script>

<div class="box">
    <h2 class="input-card-header">Set Your Nutritional Goals</h2>

    <div class="input-row">
        <InputGroup label="Calories" bind:minValue={minCalories} bind:maxValue={maxCalories} unit="kcal"/>
        <InputGroup label="Protein" bind:minValue={minProtein} bind:maxValue={maxProtein} unit="g"/>
        <InputGroup label="Carbs" bind:minValue={minCarbs} bind:maxValue={maxCarbs} unit="g"/>
        <InputGroup label="Fats" bind:minValue={minFats} bind:maxValue={maxFats} unit="g"/>
    </div>

    <div class="has-text-centered">
        <button class="button generate-button" on:click={generateMenu}>Generate My Menu 🍽️</button>
    </div>
</div>

<style>
    .input-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.4);
        max-width: 800px; /* Reduced width */
        margin: auto;
    }

    .input-card-header {
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: black;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }

    /* FLEXBOX for aligning inputs in one row */
    .input-row {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    .generate-button {
        width: 100%;
        font-size: 1rem;
        font-weight: bold;
        padding: 0.8rem;
        border-radius: 30px;
        background: #00d1b2;
        color: white;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.03);
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.3);
    }
</style>
