<script>
    export let minCalories = 1500;
    export let maxCalories = 2500;
    export let protein = 100;
    export let carbs = 200;
    export let fats = 50;
    export let allergies = "";
    export let hatedFoods = "";
    export let generateMenu;
</script>

<section class="section">
    <div class="container">
        <div class="input-card">
            <h2 class="input-card-header">Set Your Nutritional Goals</h2>

            <div class="columns is-multiline">
                <div class="column is-half form-group">
                    <label class="label">Min Calories</label>
                    <input type="number" bind:value={minCalories} class="input">
                </div>
                <div class="column is-half form-group">
                    <label class="label">Max Calories</label>
                    <input type="number" bind:value={maxCalories} class="input">
                </div>

                <div class="column is-one-third form-group">
                    <label class="label">Protein (g)</label>
                    <input type="number" bind:value={protein} class="input">
                </div>
                <div class="column is-one-third form-group">
                    <label class="label">Carbs (g)</label>
                    <input type="number" bind:value={carbs} class="input">
                </div>
                <div class="column is-one-third form-group">
                    <label class="label">Fats (g)</label>
                    <input type="number" bind:value={fats} class="input">
                </div>

                <div class="column is-half form-group">
                    <label class="label">Allergies / Dietary Restrictions</label>
                    <input type="text" bind:value={allergies} class="input">
                </div>
                <div class="column is-half form-group">
                    <label class="label">Hated Foods</label>
                    <input type="text" bind:value={hatedFoods} class="input">
                </div>
            </div>

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

    .form-group {
        margin-bottom: 1rem;
    }

    .input {
        border: 2px solid #ddd;
        border-radius: 8px;
        transition: 0.2s ease-in-out;
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
