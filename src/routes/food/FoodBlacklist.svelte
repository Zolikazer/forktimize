<script>
    import { onMount } from "svelte";

    let dislikedFoods = [];
    let newFood = "";
    let inputRef; // Reference to input field

    function addFood() {
        if (newFood.trim() && !dislikedFoods.includes(newFood.trim())) {
            dislikedFoods = [...dislikedFoods, newFood.trim()];
            newFood = "";
        }
    }

    function removeFood(food) {
        dislikedFoods = dislikedFoods.filter(f => f !== food);
    }

    function handleClickOutside(event) {
        if (inputRef && !inputRef.contains(event.target)) {
            addFood(); // Add the food if user clicks outside
        }
    }

    // Attach and remove event listener when component is mounted/unmounted
    onMount(() => {
        document.addEventListener("click", handleClickOutside);
        return () => document.removeEventListener("click", handleClickOutside);
    });
</script>

<div class="field">
    <label class="label">Foods You Dislike 🤮</label>
    <div class="control" bind:this={inputRef}>
        <input
                type="text"
                bind:value={newFood}
                on:keydown={(e) => e.key === 'Enter' && addFood()}
                class="input"
                placeholder="Type a food and press Enter">
    </div>

    <div class="tags mt-2">
        {#each dislikedFoods as food}
            <span class="tag is-danger is-light">
                {food}
                <button class="delete is-small" on:click={() => removeFood(food)}></button>
            </span>
        {/each}
    </div>
</div>
