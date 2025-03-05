<script>
    import {onMount} from "svelte";
    import {dislikedFoods} from "$lib/stores/dislikedFoodsStore.js";

    let newFood = "";
    let inputRef; // Reference to input field

    function blacklistFood() {
        if (newFood.trim()) {
            dislikedFoods.update(foods => [...foods, newFood.trim()]);
            newFood = "";
        }
    }
    function removeFoodFromBlacklist(food) {
        dislikedFoods.update(foods => foods.filter(f => f !== food));
    }

    function addFoodIfUserClickedOutside(event) {
        if (inputRef && !inputRef.contains(event.target)) {
            blacklistFood();
        }
    }

    onMount(() => {
        document.addEventListener("click", addFoodIfUserClickedOutside);
        return () => document.removeEventListener("click", addFoodIfUserClickedOutside);
    });

    function shortenText(text, length = 8) {
        return text.length > length ? text.slice(0, length) + "..." : text;
    }
</script>

<div class="field">
    <label class="label">Foods You Dislike 🤮</label>
    <div class="control" bind:this={inputRef}>
        <input
                type="text"
                bind:value={newFood}
                on:keydown={(e) => e.key === 'Enter' && blacklistFood()}
                class="input"
                placeholder="Type a food and press Enter">
    </div>

    <div class="tags mt-2">
        {#each $dislikedFoods as food}
            <span class="tag is-danger is-light" data-tooltip={food}>
                {shortenText(food)}
                <button class="delete is-small" on:click={() => removeFoodFromBlacklist(food)}></button>
            </span>
        {/each}
    </div>
</div>

<style>
    .tag[data-tooltip] {
        position: relative;
        cursor: pointer;
    }

    .tag[data-tooltip]:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
    }
</style>
