<script>
    import FoodCard from "$lib/components/meal-plan/FoodCard.svelte";
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import {t} from "$lib/stores/localeStore.js";
    import {vendorListStore} from "$lib/stores/foodVendorStore.js";
    import {onMount} from 'svelte';

    let extensionPresent = false;

    onMount(() => {
        window.postMessage({type: 'FORKTIMIZE_EXTENSION_CHECK'}, '*');

        window.addEventListener('message', (event) => {
            if (event.data.type === 'FORKTIMIZE_EXTENSION_PRESENT') {
                extensionPresent = true;
            }
        });
    });

    function handleExportClick() {
        const mealPlanData = {
            date: $mealPlanStore.date,
            foodVendor: $mealPlanStore.foodVendor,
            foods: $mealPlanStore.foods,
            exportedAt: new Date().toISOString()
        };
        
        window.postMessage({
            type: 'FORKTIMIZE_MEAL_PLAN_DATA',
            data: mealPlanData
        }, '*');
    }

    $: vendorName =
        $vendorListStore.find(v => v.type === $mealPlanStore.foodVendor)
            ?.name ?? 'Forktimize';

    $: vendorLink =
        $vendorListStore.find(v => v.type === $mealPlanStore.foodVendor)
            ?.menuUrl ?? '#';

    $: subtitleHtml = `🛵 ${$t.mealPlan.orderTheseFoods()}
        <a href=${vendorLink} target="_blank" rel="noopener noreferrer" class="has-text-link">${vendorName}</a>`;

</script>


<div class="card">
    <SectionHeader title={$t.mealPlan.yourMealPlan()}
                   subTitle={subtitleHtml}>
        <div slot="tags" class="tags">
            <span class="tag is-light is-success bigger-tag">
                <img src="meal-plan.webp" alt="Protein" width="30" height="30"
                     class="mr-2"/> {$mealPlanStore.foods.length} {$t.mealPlan.items()}
            </span>
            {#if extensionPresent}
                <button class="tag is-light is-success bigger-tag extension-button has-text-weight-bold"
                        on:click={handleExportClick}>
                    📲 Send to Extension
                </button>
            {/if}
        </div>
    </SectionHeader>
    <div class="is-flex is-flex-wrap-wrap mt-5 p-3">
        {#each $mealPlanStore.foods as food}
            <FoodCard food={food}/>
        {/each}
    </div>
</div>

<style>
    .extension-button {
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }

    .extension-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(72, 199, 142, 0.4);
        border-color: #48c78e;
        filter: brightness(1.1);
    }

    .extension-button:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(72, 199, 142, 0.3);
        filter: brightness(0.95);
    }

    .extension-button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(72, 199, 142, 0.25);
    }
</style>
