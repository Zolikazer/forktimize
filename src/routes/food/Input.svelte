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

<section class="section">
    <div class="container">
        <div class="input-card">
            <h2 class="input-card-header">Set Your Nutritional Goals</h2>

            <InputGroup label="Calories" bind:minValue={minCalories} bind:maxValue={maxCalories} unit="kcal" />
            <InputGroup label="Protein" bind:minValue={minProtein} bind:maxValue={maxProtein} unit="g" />
            <InputGroup label="Carbs" bind:minValue={minCarbs} bind:maxValue={maxCarbs} unit="g" />
            <InputGroup label="Fats" bind:minValue={minFats} bind:maxValue={maxFats} unit="g" />

            <div class="has-text-centered">
                <button class="button generate-button" on:click={generateMenu}>Generate My Menu 🍽️</button>
            </div>
        </div>
    </div>
</section>

<style>
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        max-width: 1000px;
        margin: auto;
    }

    .input-card-header {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: black;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }

    .generate-button {
        width: 100%;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 50px;
        background: #00d1b2;
        color: white;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }

    .generate-button:hover {
        background: #009e8e;
        transform: scale(1.05);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
    }
</style>
