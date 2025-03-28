<script>
    import {onMount} from "svelte";
    import {menuRequestStore} from "$lib/stores/menuRequestStore.js";

    let newFood = "";
    let inputRef;
    const truncateLength = 8;


    function blacklistFood() {
        const trimmedFood = newFood.trim();

        if (trimmedFood) {
            menuRequestStore.addDislikedFood(trimmedFood);
        }

        newFood = "";
    }

    function removeFoodFromBlacklist(food) {
        menuRequestStore.removeDislikedFood(food);
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

    function shortenText(text, length = truncateLength) {
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
        {#each $menuRequestStore.dislikedFoods as food}
            <span class="tag is-danger is-light" data-tooltip={food}>
                {shortenText(food)}
                <button class="delete is-small"
                        on:click={() => removeFoodFromBlacklist(food)}
                        aria-label="Remove {food}">

                </button>
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
