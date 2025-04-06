<script>
    import {mealPlanStore, MealPlanStatus} from "$lib/stores/mealPlanStore.js";
    import {t} from '$lib/stores/localeStore.js';

</script>

{#if $mealPlanStore.status === MealPlanStatus.SUCCESS}
    <div class="notification is-success has-text-centered">
        <strong>{$t.feedback.ready()} ✅</strong>
    </div>
{:else if $mealPlanStore.status === MealPlanStatus.FAILURE}
    <div class="notification is-danger has-text-centered">
        {@html $t.feedback.failed()}
        👍
    </div>
{:else if $mealPlanStore.status === MealPlanStatus.IN_PROGRESS}
    <div class="notification is-primary has-text-centered">
        <span class="spinner"></span>
        <strong>{$t.feedback.inProgress()}</strong>
    </div>
{:else}
    <div class="notification is-primary has-text-centered">
        {@html $t.feedback.notStarted()} 🚀
    </div>
{/if}

<style>
    .spinner {
        display: inline-block;
        width: 1.4em;
        height: 1.4em;
        border: 5px solid #ddd;
        border-top: 3px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        vertical-align: middle;
        margin-right: 8px;
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
