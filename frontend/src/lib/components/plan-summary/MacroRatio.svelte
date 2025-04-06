<script>
    import {t} from '$lib/stores/localeStore.js';

    export let proteinPercentage;
    export let carbsPercentage;
    export let fatPercentage;
</script>
<div class="mb-2">
    <p class="is-size-7 has-text-grey has-text-weight-semibold mb-2">
        {$t.summary.macroRatio()}
    </p>
    <div class="macro-ratio-bar">
        <div
                class="ratio-segment has-background-info"
                style="width: {proteinPercentage}%;"
        >
            {proteinPercentage > 10 ? proteinPercentage + '%' : ''}
        </div>
        <div
                class="ratio-segment has-background-danger"
                style="width: {carbsPercentage}%;"
        >
            {carbsPercentage > 10 ? carbsPercentage + '%' : ''}
        </div>
        <div
                class="ratio-segment has-background-warning"
                style="width: {fatPercentage}%;"
        >
            {fatPercentage > 10 ? fatPercentage + '%' : ''}
        </div>
    </div>


    <div class="is-flex is-gap-1 mt-2 is-size-7 has-text-grey">
        <div class="is-flex is-align-items-center">
            <div class="legend-dot has-background-info"></div>
            <span>{$t.macro.protein()}</span>
        </div>
        <div class="is-flex is-align-items-center">
            <div class="legend-dot has-background-danger"></div>
            <span>{$t.macro.carb()}</span>
        </div>
        <div class="is-flex is-align-items-center">
            <div class="legend-dot has-background-warning"></div>
            <span>{$t.macro.fat()}</span>
        </div>
    </div>
</div>

<style>

    .macro-ratio-bar {
        display: flex;
        height: 1.25rem;
        border-radius: 999px;
        overflow: hidden;
        background-color: #e0e0e0;
    }

    .ratio-segment {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        color: #fff;
        white-space: nowrap;
    }

    .legend-dot {
        width: 0.75rem;
        height: 0.75rem;
        border-radius: 50%;
        margin-right: 0.25rem;
    }

</style>
