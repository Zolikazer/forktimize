<script>
    import {mealPlanStore, MealPlanStatus} from "$lib/stores/mealPlanStore.js";

</script>

{#if $mealPlanStore.status === MealPlanStatus.SUCCESS}
    <div class="notification is-success has-text-centered">
        <strong>Your meal plan is ready. ✅</strong>
    </div>
{:else if $mealPlanStore.status === MealPlanStatus.FAILURE}
    <div class="notification is-danger has-text-centered">
        Sorry, we could not find a meal plan that meets your needs. 😔 <strong>Adjust your input and try again!</strong>
        👍
    </div>
{:else if $mealPlanStore.status === MealPlanStatus.IN_PROGRESS}
    <div class="notification is-primary has-text-centered">
        <span class="spinner"></span>
        <strong> Generating your meal plan... Please wait!</strong>
    </div>
{:else}
    <div class="notification is-primary has-text-centered">
        No meal plan generated yet. Click <strong>"Generate Meal Plan"</strong> to get started! 🚀
    </div>
{/if}

<style>
    .spinner {
        display: inline-block;
        width: 1.4em;
        height: 1.4em;
        border: 5px solid #ddd;
        border-top: 3px solid #007bff; /* Blue spinner */
        border-radius: 50%;
        animation: spin 1s linear infinite;
        vertical-align: middle; /* ✅ Aligns with text */
        margin-right: 8px; /* ✅ Adds space between spinner and text */
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

</style>
