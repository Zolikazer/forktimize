<script>
    export let proteinPercentage = 0;
    export let carbsPercentage = 0;
    export let fatPercentage = 0;
    export let title = "Macronutrient Ratio";
</script>
<div class="mb-2">
    <p class="is-size-7 has-text-grey has-text-weight-semibold mb-2">
        Macronutrient Ratio
    </p>
    <div class="macro-ratio-bar">
        <div
                class="ratio-segment ratio-protein"
                style="width: {proteinPercentage}%;"
        >
            {proteinPercentage > 10 ? proteinPercentage + '%' : ''}
        </div>
        <div
                class="ratio-segment ratio-carbs"
                style="width: {carbsPercentage}%;"
        >
            {carbsPercentage > 10 ? carbsPercentage + '%' : ''}
        </div>
        <div
                class="ratio-segment ratio-fat"
                style="width: {fatPercentage}%;"
        >
            {fatPercentage > 10 ? fatPercentage + '%' : ''}
        </div>
    </div>


    <div class="is-flex is-gap-1 mt-2 is-size-7 has-text-grey">
        <div class="is-flex is-align-items-center">
            <div class="legend-dot protein-dot"></div>
            <span>Protein</span>
        </div>
        <div class="is-flex is-align-items-center">
            <div class="legend-dot carbs-dot"></div>
            <span>Carbs</span>
        </div>
        <div class="is-flex is-align-items-center">
            <div class="legend-dot fat-dot"></div>
            <span>Fat</span>
        </div>
    </div>
</div>

<style>
    .macro-ratio {
        margin-bottom: 1rem; /* or whatever suits your layout */
    }

    /* The bar container */
    .macro-ratio-bar {
        display: flex;
        height: 1.25rem;
        border-radius: 999px;
        overflow: hidden;
        background-color: #e0e0e0;
    }

    /* Each colored segment */
    .ratio-segment {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        color: #fff;
        white-space: nowrap;
    }

    .ratio-protein {
        background-color: #f14668; /* bulma "danger" shade */
    }

    .ratio-carbs {
        background-color: #48c78e; /* bulma "success" shade */
    }

    .ratio-fat {
        background-color: #3273dc; /* bulma "link" shade */
    }

    /* Legend dots */
    .legend-dot {
        width: 0.75rem;
        height: 0.75rem;
        border-radius: 50%;
        margin-right: 0.25rem;
    }

    .protein-dot {
        background-color: #f14668;
    }

    .carbs-dot {
        background-color: #48c78e;
    }

    .fat-dot {
        background-color: #3273dc;
    }
</style>
