<script>
    export let label;
    export let minValue;
    export let maxValue;
    export let unit = "";

    function validateNumber(value) {
        return (value < 0 || isNaN(value)) ? "" : value; // Return corrected value
    }

</script>

<div class="input-group has-background-white-ter mx-auto mb-3">
    <p class="has-text-weight-bold has-text-grey-darker is-size-7 mb-2">{label} ({unit})</p>

    <div class="is-flex is-justify-content-center gap-2">
        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Min</label>
            <input type="number"
                   bind:value={minValue}
                   on:blur={() => minValue = validateNumber(minValue)}
                   class="input is-small has-text-centered is-rounded"
                   placeholder="Optional"
            >
        </div>
        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Max</label>
            <input type="number"
                   bind:value={maxValue}
                   on:blur={() => maxValue = validateNumber(maxValue)}
                   class="input is-small has-text-centered is-rounded"
                   placeholder="Optional">
        </div>
    </div>
</div>


<style>
    .input-group {
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.45);
        text-align: center;
        font-size: 0.9rem;
        width: 200px; /* Adjusted width to fit inline */
    }

    /* Remove spinner/arrows for Chrome, Safari, Edge, Opera */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    /* Remove spinner/arrows for Firefox */
    input[type="number"] {
        -moz-appearance: textfield;
    }
</style>
