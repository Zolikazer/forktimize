<script>
    import {t} from '$lib/stores/localeStore.js';

    export let label;
    export let minValue;
    export let maxValue;
    export let unit = "";
    export let emoji = "";
    let isValid = true;

    function resetInvalidInput(value) {
        return isPositiveInteger(value) ? value : undefined;
    }

    $: isValid = minValue === undefined || maxValue === undefined || maxValue > minValue;

    function isPositiveInteger(value) {
        return Number.isInteger(value) && value > 0;
    }

</script>

<div class="input-group has-background-white-ter mx-auto mb-3 p-3 has-radius-large has-text-centered">
    <p class="has-text-weight-bold has-text-grey-darker is-size-6 mb-2">{label} ({unit}) {emoji}</p>

    <div class="is-flex is-justify-content-center gap-2">
        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label for="min-input" class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Min</label>
            <div class="tooltip-container" data-tooltip="Max should be greater than or equal to Min"
                 class:has-tooltip={!isValid}>
                <input
                        id="min-input"
                        type="number"
                        bind:value={minValue}
                        on:blur={() => { minValue = resetInvalidInput(minValue)}}
                        class="input is-small has-text-centered is-rounded"
                        placeholder={$t.requestForm.optional()}
                        class:is-danger={!isValid}
                >
            </div>
        </div>

        <div class="is-flex is-flex-direction-column is-align-items-center is-flex-grow-1">
            <label for="max-input" class="has-text-grey-darker has-text-weight-bold is-size-7 mb-1">Max</label>
            <div class="tooltip-container" data-tooltip="Max should be greater than or equal to Min"
                 class:has-tooltip={!isValid}>
                <input id="max-input"
                       type="number"
                       bind:value={maxValue}
                       on:blur={() => {maxValue = resetInvalidInput(maxValue) }}
                       class="input is-small has-text-centered is-rounded"
                       placeholder={$t.requestForm.optional()}
                       class:is-danger={!isValid}>
            </div>

        </div>
    </div>
</div>


<style>
    .input-group {
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
        width: 200px;
    }

    .tooltip-container {
        position: relative;
    }

    .tooltip-container.has-tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: red;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
    }

    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    input[type="number"] {
        -moz-appearance: textfield;
    }
</style>
